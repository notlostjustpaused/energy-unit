# Energy Unit (EU) Currency — Specification

**Version:** 0.3  
**Date:** 2026-09-09  
**Status:** Working simulation + storage cycles + protocol fees

## Core Idea

1 EU represents a claim on **1 kWh of verified, deliverable electrical energy**.  
The digital token is a transparent, transferable claim; the physical energy is the ultimate backing.

## Design Principles

1. **Physical scarcity** — EUs can only be created against verified meter data (production or efficient storage discharge).
2. **No arbitrary issuance** — Only authorized producers / storage operators can mint.
3. **Redeemability** — Holders can burn EUs to take delivery of real energy.
4. **Time-shifting via storage** — Batteries and other storage can charge (consume EUs) and later discharge (mint time-shifted EUs), subject to real efficiency losses.
5. **Conservatism** — Circulating supply must never exceed cumulative verified production.

## Units & Fungibility

- Base unit: 1 EU = 1 kWh.
- Currently treated as fungible “average regional” claims.
- Future versions can introduce time-of-use and location tags (semi-fungible or NFT-style).

## Actors

| Actor              | Can Mint? | Notes                                      |
|--------------------|-----------|--------------------------------------------|
| Generator          | Yes       | Solar, wind, hydro, nuclear, etc.          |
| Storage Operator   | Yes (on discharge) | Must first charge; efficiency loss applies |
| Consumer / Holder  | No        | Can hold, transfer, redeem                 |
| Protocol / Ledger  | —         | Enforces invariants, records events, collects fees |

## Key Operations

### Report Production → Mint
Authorized party submits verified kWh → EUs are credited to their account (minus protocol fee) and total verified production increases.

### Transfer
Any holder can send EUs to any other account (atomic balance update).

### Redeem
Holder burns EUs; the system records delivery of that quantity of energy. Circulating supply falls.

### Storage Charge
Storage account spends EUs to increase its internal `stored_kwh`.  
Partial efficiency loss applied on the way in.

### Storage Discharge
Storage reduces its `stored_kwh` and mints new EUs equal to the effective energy delivered after remaining efficiency loss.  
This is how energy is time-shifted while remaining honest about physics.

## Invariants (Strictly Enforced)

- `circulating_eu ≤ total_verified_production_kwh`
- No account may have a negative EU balance
- Storage cannot exceed its declared capacity
- Only flagged producer/storage accounts may mint

## Efficiency Model (Storage)

Round-trip efficiency η (default 0.88 for modern batteries).  
Loss is split approximately evenly between charge and discharge legs using √η.  
This keeps the economics realistic without requiring perfect physical modeling.

## Protocol Fee

Default 1% of newly minted energy (production or storage discharge) is sent to a dedicated Protocol Treasury account.

## Explicitly Out of Scope (for now)

- Real-time grid physics / power flow
- Transmission losses & congestion pricing
- Multi-party decentralized oracles
- Governance tokens
- Cross-chain bridges
- Regulatory wrappers
