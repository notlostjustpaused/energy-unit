# Energy Unit (EU)

**1 Energy Unit = 1 kWh of verified electrical energy.**

A working simulation of an energy-backed digital system.  
Digital claims are only created against real (or simulated) measured electricity, and the number of units in circulation is never allowed to exceed verified production.

---

## Quick Start

```bash
git clone https://github.com/notlostjustpaused/energy-unit.git
cd energy-unit
python -m src.simulate_v2
```

For the Stage 2 signed-measurement demo:

```bash
python -m src.demo_signed_measurement
```

---

## What This Is

- A clear set of rules linking digital units to physical energy
- A working Python simulation that enforces those rules
- A deliberate path from simulation → trusted measurement → small pilot
- Documentation written for both technical and non-technical readers

## What This Is Not

- Not a live token or cryptocurrency
- Not connected to real electricity meters yet
- Not ready for commercial use
- Not a claim that energy should replace all other forms of money

---

## Key Documents

| Document | Who it’s for | Purpose |
|----------|--------------|---------|
| [HOW_IT_WORKS.md](HOW_IT_WORKS.md) | Anyone | Plain-English explanation of the idea |
| [FOR_ENERGY_OPERATORS.md](FOR_ENERGY_OPERATORS.md) | Producers & storage operators | Why this might matter to people who control real energy |
| [ROADMAP.md](ROADMAP.md) | Everyone | Stages from simulation to real-world use |
| [TRUSTED_MEASUREMENT.md](TRUSTED_MEASUREMENT.md) | Technical readers | How real meter data could enter the system |
| [SIGNED_MEASUREMENT_DESIGN.md](SIGNED_MEASUREMENT_DESIGN.md) | Technical readers | Concrete design for signed measurements |
| [docs/SPEC.md](docs/SPEC.md) | Technical readers | Precise rules and invariants |
| [QUICK_START.md](QUICK_START.md) | New users | How to run the simulation |
| [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) | Developers / AIs | How to rebuild the system correctly |

---

## Core Rules (Never Violated)

1. Energy Units can only be created against verified production or storage discharge.
2. Circulating units can never exceed total verified production.
3. Redemption burns units when energy is delivered.
4. Storage has real efficiency losses — it does not create energy.

---

## Current Status

| Stage | Status |
|-------|--------|
| 1. Simulation | Working |
| 2. Trusted Measurement | Design + first code version complete |
| 3. Small Pilot | Not started |
| 4. Broader Use | Future |

---

## Design Stance

Digital claims should stay tightly linked to real, verified energy.  
That principle comes first. Everything else is secondary.

---

## License

MIT License — see [LICENSE](LICENSE)
