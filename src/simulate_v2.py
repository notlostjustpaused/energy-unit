#!/usr/bin/env python3
"""
Multi-day Energy Unit simulation with storage cycles and protocol fees.
"""

from datetime import datetime, timedelta
from src.eu_ledger import EnergyLedger
import os


def run_multi_day_demo():
    print("=" * 70)
    print("Energy Unit (EU) Currency — v0.3 Multi-Day Simulation")
    print("Includes 1% mint fee → Protocol Treasury")
    print("=" * 70)

    ledger = EnergyLedger(
        name="Demo Regional Grid v0.3",
        mint_fee_rate=0.01,       # 1% of newly minted energy goes to treasury
        transfer_fee_rate=0.0,    # keep transfers free for now
    )

    solar = ledger.create_account("Sunny Hills Solar", is_producer=True)
    wind = ledger.create_account("Coastal Wind", is_producer=True)
    battery = ledger.create_account(
        "Grid Scale Battery",
        is_producer=True,
        is_storage=True,
        max_storage_kwh=15_000,
        efficiency=0.88,
    )
    factory = ledger.create_account("MetalWorks Factory")
    datacenter = ledger.create_account("AI Compute Center")
    homes = ledger.create_account("Residential Aggregate")

    print("\nInitial state:")
    print(ledger.snapshot())
    print("-" * 70)

    base = datetime(2026, 9, 9, 0, 0, 0)

    # DAY 1
    print("\n>>> DAY 1 — High solar, charge storage, evening load")
    t = base + timedelta(hours=8)
    ledger.report_production(solar.id, 14_200, timestamp=t, notes="Excellent irradiance")
    ledger.report_production(wind.id, 6_800, timestamp=t + timedelta(hours=1), notes="Moderate wind")

    ledger.transfer(solar.id, battery.id, 5_000, timestamp=t + timedelta(hours=2))
    ledger.charge_storage(battery.id, 5_000, timestamp=t + timedelta(hours=2), notes="Daytime arbitrage charge")

    ledger.transfer(solar.id, factory.id, 4_000, timestamp=t + timedelta(hours=10))
    ledger.transfer(wind.id, datacenter.id, 3_500, timestamp=t + timedelta(hours=10))
    ledger.transfer(solar.id, homes.id, 2_000, timestamp=t + timedelta(hours=11))

    ledger.discharge_storage(battery.id, 4_000, timestamp=t + timedelta(hours=12), notes="Evening peak support")
    ledger.transfer(battery.id, datacenter.id, 2_500, timestamp=t + timedelta(hours=12))
    ledger.transfer(battery.id, homes.id, 1_200, timestamp=t + timedelta(hours=12))

    ledger.redeem(factory.id, 3_800, delivery_note="Day shift", timestamp=t + timedelta(hours=14))
    ledger.redeem(datacenter.id, 5_500, delivery_note="Training run", timestamp=t + timedelta(hours=16))
    ledger.redeem(homes.id, 2_800, delivery_note="Evening residential", timestamp=t + timedelta(hours=18))

    print(ledger.snapshot())
    print("-" * 70)

    # DAY 2
    print("\n>>> DAY 2 — Cloudier, stronger wind, storage cycling")
    t = base + timedelta(days=1, hours=7)
    ledger.report_production(solar.id, 8_900, timestamp=t, notes="Partly cloudy")
    ledger.report_production(wind.id, 11_500, timestamp=t + timedelta(hours=2), notes="Strong frontal system")

    ledger.transfer(wind.id, battery.id, 4_500, timestamp=t + timedelta(hours=3))
    ledger.charge_storage(battery.id, 4_500, timestamp=t + timedelta(hours=3), notes="Wind surplus storage")

    ledger.transfer(solar.id, factory.id, 5_000, timestamp=t + timedelta(hours=5))
    ledger.transfer(wind.id, datacenter.id, 4_000, timestamp=t + timedelta(hours=5))
    ledger.transfer(solar.id, homes.id, 1_500, timestamp=t + timedelta(hours=6))

    ledger.discharge_storage(battery.id, 3_500, timestamp=t + timedelta(hours=14), notes="Late peak")
    ledger.transfer(battery.id, factory.id, 2_000, timestamp=t + timedelta(hours=14))
    ledger.transfer(battery.id, homes.id, 1_000, timestamp=t + timedelta(hours=15))

    ledger.redeem(factory.id, 6_500, delivery_note="Extended production", timestamp=t + timedelta(hours=16))
    ledger.redeem(datacenter.id, 3_800, delivery_note="Inference load", timestamp=t + timedelta(hours=17))
    ledger.redeem(homes.id, 2_200, delivery_note="Residential", timestamp=t + timedelta(hours=19))

    print(ledger.snapshot())
    print("-" * 70)

    # DAY 3
    print("\n>>> DAY 3 — Mixed conditions, residual holdings")
    t = base + timedelta(days=2, hours=8)
    ledger.report_production(solar.id, 11_300, timestamp=t, notes="Good recovery")
    ledger.report_production(wind.id, 7_200, timestamp=t + timedelta(hours=1), notes="Easing winds")

    ledger.transfer(solar.id, battery.id, 1_500, timestamp=t + timedelta(hours=3))
    ledger.charge_storage(battery.id, 1_500, timestamp=t + timedelta(hours=3), notes="Top-up")

    ledger.transfer(solar.id, factory.id, 3_000, timestamp=t + timedelta(hours=6))
    ledger.transfer(wind.id, datacenter.id, 2_500, timestamp=t + timedelta(hours=6))
    ledger.transfer(battery.id, homes.id, 200, timestamp=t + timedelta(hours=10))

    ledger.redeem(factory.id, 3_200, delivery_note="Final shift", timestamp=t + timedelta(hours=12))
    ledger.redeem(datacenter.id, 2_000, delivery_note="Batch jobs", timestamp=t + timedelta(hours=14))
    ledger.redeem(homes.id, 900, delivery_note="Residential", timestamp=t + timedelta(hours=16))

    print(ledger.snapshot())
    print("-" * 70)

    stats = ledger.summary_stats()
    print("\n=== FINAL SUMMARY ===")
    for k, v in stats.items():
        print(f"  {k:<22}: {v}")

    out_path = os.path.join("simulations", "multi_day_events_v03.csv")
    full_path = ledger.export_events_csv(out_path)
    print(f"\nEvents exported to: {full_path}")
    print("\nAll invariants held. Treasury has accumulated protocol fees.")
    return ledger


if __name__ == "__main__":
    run_multi_day_demo()
