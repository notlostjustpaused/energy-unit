"""
Energy Unit (EU) Ledger — Simulation
1 EU ≈ 1 kWh of verified electrical energy.

v0.3 additions:
- Protocol fee on mint (and optionally transfer)
- Dedicated treasury account that accumulates fees
- Cleaner stats and fee reporting
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid
import csv
import os


@dataclass
class Account:
    id: str
    name: str
    balance_eu: float = 0.0
    is_producer: bool = False
    is_storage: bool = False
    is_treasury: bool = False
    stored_kwh: float = 0.0
    max_storage_kwh: float = 0.0
    efficiency: float = 0.90

    def __post_init__(self):
        if self.balance_eu < -1e-9:
            raise ValueError("Balance cannot be negative")


@dataclass
class ProductionEvent:
    event_id: str
    producer_id: str
    kwh: float
    fee_eu: float
    net_minted: float
    timestamp: datetime
    location: str = "default"
    notes: str = ""
    event_type: str = "production"


@dataclass
class TransferEvent:
    event_id: str
    from_id: str
    to_id: str
    amount: float
    fee_eu: float
    timestamp: datetime
    event_type: str = "transfer"


@dataclass
class RedemptionEvent:
    event_id: str
    holder_id: str
    amount: float
    timestamp: datetime
    delivery_note: str = ""
    event_type: str = "redemption"


@dataclass
class StorageEvent:
    event_id: str
    storage_id: str
    action: str
    kwh_requested: float
    kwh_effective: float
    timestamp: datetime
    notes: str = ""
    event_type: str = "storage"


class EnergyLedger:
    """
    In-memory ledger for Energy Units.
    Enforces physical scarcity + optional protocol fees that flow to a treasury.
    """

    def __init__(
        self,
        name: str = "Regional EU Ledger",
        mint_fee_rate: float = 0.01,
        transfer_fee_rate: float = 0.0,
    ):
        if not (0.0 <= mint_fee_rate < 0.5):
            raise ValueError("mint_fee_rate should be between 0 and 0.5")
        if not (0.0 <= transfer_fee_rate < 0.1):
            raise ValueError("transfer_fee_rate should be between 0 and 0.1")

        self.name = name
        self.mint_fee_rate = mint_fee_rate
        self.transfer_fee_rate = transfer_fee_rate

        self.accounts: Dict[str, Account] = {}
        self.total_verified_production_kwh: float = 0.0
        self.total_minted_eu: float = 0.0
        self.total_redeemed_eu: float = 0.0
        self.total_fees_collected: float = 0.0

        self.production_events: List[ProductionEvent] = []
        self.transfer_events: List[TransferEvent] = []
        self.redemption_events: List[RedemptionEvent] = []
        self.storage_events: List[StorageEvent] = []
        self.created_at = datetime.utcnow()

        self.treasury = self.create_account("Protocol Treasury", is_treasury=True)

    @property
    def circulating_eu(self) -> float:
        return round(self.total_minted_eu - self.total_redeemed_eu, 6)

    def create_account(
        self,
        name: str,
        is_producer: bool = False,
        is_storage: bool = False,
        is_treasury: bool = False,
        max_storage_kwh: float = 0.0,
        efficiency: float = 0.90,
    ) -> Account:
        acc_id = str(uuid.uuid4())[:8]
        account = Account(
            id=acc_id,
            name=name,
            is_producer=is_producer,
            is_storage=is_storage,
            is_treasury=is_treasury,
            max_storage_kwh=max_storage_kwh,
            efficiency=efficiency,
        )
        self.accounts[acc_id] = account
        return account

    def get_account(self, account_id: str) -> Account:
        if account_id not in self.accounts:
            raise KeyError(f"Account {account_id} not found")
        return self.accounts[account_id]

    def report_production(
        self,
        producer_id: str,
        kwh: float,
        timestamp: Optional[datetime] = None,
        location: str = "default",
        notes: str = "",
    ) -> ProductionEvent:
        if kwh <= 0:
            raise ValueError("Production must be positive")
        producer = self.get_account(producer_id)
        if not (producer.is_producer or producer.is_storage):
            raise PermissionError(f"Account {producer.name} is not authorized to mint")

        ts = timestamp or datetime.utcnow()
        fee = round(kwh * self.mint_fee_rate, 6)
        net = round(kwh - fee, 6)

        event = ProductionEvent(
            event_id=str(uuid.uuid4())[:8],
            producer_id=producer_id,
            kwh=kwh,
            fee_eu=fee,
            net_minted=net,
            timestamp=ts,
            location=location,
            notes=notes,
        )

        producer.balance_eu += net
        self.treasury.balance_eu += fee
        self.total_verified_production_kwh += kwh
        self.total_minted_eu += kwh
        self.total_fees_collected += fee
        self.production_events.append(event)

        self._check_invariants()
        return event

    def transfer(
        self,
        from_id: str,
        to_id: str,
        amount: float,
        timestamp: Optional[datetime] = None,
    ) -> TransferEvent:
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        sender = self.get_account(from_id)
        receiver = self.get_account(to_id)

        fee = round(amount * self.transfer_fee_rate, 6)
        total_debit = amount + fee

        if sender.balance_eu < total_debit - 1e-9:
            raise ValueError(
                f"Insufficient balance: {sender.name} has {sender.balance_eu:.4f} EU, "
                f"needs {total_debit:.4f} (incl. fee)"
            )

        ts = timestamp or datetime.utcnow()
        event = TransferEvent(
            event_id=str(uuid.uuid4())[:8],
            from_id=from_id,
            to_id=to_id,
            amount=amount,
            fee_eu=fee,
            timestamp=ts,
        )

        sender.balance_eu -= total_debit
        receiver.balance_eu += amount
        if fee > 0:
            self.treasury.balance_eu += fee
            self.total_fees_collected += fee

        self.transfer_events.append(event)
        return event

    def redeem(
        self,
        holder_id: str,
        amount: float,
        delivery_note: str = "",
        timestamp: Optional[datetime] = None,
    ) -> RedemptionEvent:
        if amount <= 0:
            raise ValueError("Redemption amount must be positive")
        holder = self.get_account(holder_id)
        if holder.balance_eu < amount - 1e-9:
            raise ValueError(
                f"Insufficient balance for redemption: {holder.name} has {holder.balance_eu:.4f} EU"
            )

        ts = timestamp or datetime.utcnow()
        event = RedemptionEvent(
            event_id=str(uuid.uuid4())[:8],
            holder_id=holder_id,
            amount=amount,
            timestamp=ts,
            delivery_note=delivery_note,
        )

        holder.balance_eu -= amount
        self.total_redeemed_eu += amount
        self.redemption_events.append(event)

        self._check_invariants()
        return event

    def charge_storage(
        self,
        storage_id: str,
        kwh: float,
        timestamp: Optional[datetime] = None,
        notes: str = "",
    ) -> StorageEvent:
        if kwh <= 0:
            raise ValueError("Charge amount must be positive")
        storage = self.get_account(storage_id)
        if not storage.is_storage:
            raise PermissionError(f"{storage.name} is not a storage account")

        if storage.balance_eu < kwh - 1e-9:
            raise ValueError(
                f"Storage {storage.name} needs {kwh} EU to charge but only has {storage.balance_eu:.4f}"
            )

        effective_stored = kwh * (storage.efficiency ** 0.5)
        if storage.stored_kwh + effective_stored > storage.max_storage_kwh + 1e-6:
            raise ValueError("Storage capacity exceeded")

        ts = timestamp or datetime.utcnow()
        event = StorageEvent(
            event_id=str(uuid.uuid4())[:8],
            storage_id=storage_id,
            action="charge",
            kwh_requested=kwh,
            kwh_effective=effective_stored,
            timestamp=ts,
            notes=notes,
        )

        storage.balance_eu -= kwh
        storage.stored_kwh += effective_stored
        self.storage_events.append(event)
        return event

    def discharge_storage(
        self,
        storage_id: str,
        kwh_requested: float,
        timestamp: Optional[datetime] = None,
        notes: str = "",
    ) -> StorageEvent:
        if kwh_requested <= 0:
            raise ValueError("Discharge amount must be positive")
        storage = self.get_account(storage_id)
        if not storage.is_storage:
            raise PermissionError(f"{storage.name} is not a storage account")

        if storage.stored_kwh < kwh_requested - 1e-9:
            raise ValueError(
                f"Not enough stored energy. Have {storage.stored_kwh:.4f}, requested {kwh_requested}"
            )

        effective_out = kwh_requested * (storage.efficiency ** 0.5)
        fee = round(effective_out * self.mint_fee_rate, 6)
        net = round(effective_out - fee, 6)

        ts = timestamp or datetime.utcnow()
        event = StorageEvent(
            event_id=str(uuid.uuid4())[:8],
            storage_id=storage_id,
            action="discharge",
            kwh_requested=kwh_requested,
            kwh_effective=effective_out,
            timestamp=ts,
            notes=notes,
        )

        storage.stored_kwh -= kwh_requested
        storage.balance_eu += net
        self.treasury.balance_eu += fee
        self.total_verified_production_kwh += effective_out
        self.total_minted_eu += effective_out
        self.total_fees_collected += fee
        self.storage_events.append(event)

        self._check_invariants()
        return event

    def _check_invariants(self):
        if self.circulating_eu > self.total_verified_production_kwh + 1e-5:
            raise RuntimeError(
                f"INVARIANT BROKEN: circulating {self.circulating_eu:.4f} > "
                f"verified production {self.total_verified_production_kwh:.4f}"
            )
        for acc in self.accounts.values():
            if acc.balance_eu < -1e-6:
                raise RuntimeError(f"Negative balance on {acc.name}: {acc.balance_eu}")

    def snapshot(self) -> str:
        lines = [
            f"=== {self.name} Snapshot ===",
            f"UTC: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Verified production : {self.total_verified_production_kwh:>12,.2f} kWh",
            f"Total minted (gross): {self.total_minted_eu:>12,.2f}",
            f"Total redeemed      : {self.total_redeemed_eu:>12,.2f}",
            f"Circulating EU      : {self.circulating_eu:>12,.2f}",
            f"Fees collected      : {self.total_fees_collected:>12,.2f}",
            f"Backing ratio       : {self.circulating_eu / max(self.total_verified_production_kwh, 1):.4f}",
            f"Mint fee rate       : {self.mint_fee_rate:.2%}",
            "",
            "Accounts:",
        ]
        for acc in sorted(self.accounts.values(), key=lambda a: a.name):
            roles = []
            if acc.is_treasury:
                roles.append("Treasury")
            if acc.is_producer:
                roles.append("Producer")
            if acc.is_storage:
                roles.append(f"Storage({acc.stored_kwh:.0f}/{acc.max_storage_kwh:.0f})")
            role_str = f" [{', '.join(roles)}]" if roles else ""
            lines.append(f"  {acc.name:<28}{role_str}: {acc.balance_eu:>10,.2f} EU")
        return "\n".join(lines)

    def summary_stats(self) -> Dict[str, Any]:
        return {
            "total_verified_kwh": round(self.total_verified_production_kwh, 2),
            "total_minted_gross": round(self.total_minted_eu, 2),
            "total_redeemed": round(self.total_redeemed_eu, 2),
            "circulating": round(self.circulating_eu, 2),
            "fees_collected": round(self.total_fees_collected, 2),
            "treasury_balance": round(self.treasury.balance_eu, 2),
            "backing_ratio": round(self.circulating_eu / max(self.total_verified_production_kwh, 1), 4),
            "mint_fee_rate": self.mint_fee_rate,
            "num_accounts": len(self.accounts),
            "num_production_events": len(self.production_events),
            "num_transfers": len(self.transfer_events),
            "num_redemptions": len(self.redemption_events),
            "num_storage_events": len(self.storage_events),
        }

    def export_events_csv(self, path: str) -> str:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        rows = []

        for e in self.production_events:
            rows.append({
                "event_type": "production",
                "event_id": e.event_id,
                "timestamp": e.timestamp.isoformat(),
                "account_id": e.producer_id,
                "amount": e.kwh,
                "fee_eu": e.fee_eu,
                "net": e.net_minted,
                "location": e.location,
                "notes": e.notes,
            })
        for e in self.transfer_events:
            rows.append({
                "event_type": "transfer",
                "event_id": e.event_id,
                "timestamp": e.timestamp.isoformat(),
                "from_id": e.from_id,
                "to_id": e.to_id,
                "amount": e.amount,
                "fee_eu": e.fee_eu,
            })
        for e in self.redemption_events:
            rows.append({
                "event_type": "redemption",
                "event_id": e.event_id,
                "timestamp": e.timestamp.isoformat(),
                "account_id": e.holder_id,
                "amount": e.amount,
                "notes": e.delivery_note,
            })
        for e in self.storage_events:
            rows.append({
                "event_type": f"storage_{e.action}",
                "event_id": e.event_id,
                "timestamp": e.timestamp.isoformat(),
                "account_id": e.storage_id,
                "amount_requested": e.kwh_requested,
                "amount_effective": e.kwh_effective,
                "notes": e.notes,
            })

        fieldnames = [
            "event_type", "event_id", "timestamp", "account_id",
            "from_id", "to_id", "amount", "fee_eu", "net",
            "amount_requested", "amount_effective", "location", "notes"
        ]
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for row in sorted(rows, key=lambda r: r["timestamp"]):
                writer.writerow(row)
        return path
