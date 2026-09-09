# Energy Currency MVP — Energy Units (EU)

**1 EU ≈ 1 kWh of verified, deliverable electrical energy.**

Working simulation of a practical energy-backed digital currency.

## Current Version: 0.3

- Mint / transfer / redeem with physical scarcity invariants
- Storage charge & discharge (realistic round-trip efficiency)
- **Protocol fee (default 1% on mint) that accumulates in a Treasury account**
- Multi-day demonstration + CSV event export

## Quick Start

```bash
cd energy_currency_mvp
python -m src.simulate_v2
```

## What v0.3 Adds

A small protocol fee on newly minted energy flows to a dedicated Treasury.  
This is the first economic primitive that can later fund development, governance, or alignment.

## Project Layout

```
energy_currency_mvp/
├── README.md
├── docs/SPEC.md
├── src/
│   ├── eu_ledger.py      # Core ledger + fees + storage
│   ├── simulate.py       # Short demo
│   └── simulate_v2.py    # Multi-day + fees demo
└── simulations/          # CSV exports
```

## Design Stance

Money works best when it is scarce and useful. Energy is both.  
This prototype makes the relationship explicit, programmable, and auditable.
