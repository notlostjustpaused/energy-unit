# Build Instructions for Energy Unit (EU) Ledger

This is the master prompt that can be given to an AI to rebuild or extend the system correctly.

---

You are to build a clean, correct implementation of an Energy Unit (EU) currency system.

CORE DEFINITION
- 1 EU = 1 kWh of verified, deliverable electrical energy.
- EUs are digital claims on real energy. They are not arbitrary tokens.

FUNDAMENTAL RULES (must never be violated)
1. EUs can only be created (minted) against verified energy production or against energy discharged from storage that was previously charged.
2. Circulating supply of EUs must never exceed total verified production (in kWh).
3. Redemption burns EUs and represents actual delivery of energy.
4. Storage has real efficiency losses (default round-trip ~88%). Energy is not created by storage; it is only time-shifted.
5. Only authorized producer or storage accounts may mint.

MINIMUM VIABLE FEATURES (implement in this order)

Step 1 – Core Ledger
- Accounts with balances in EU.
- Ability to create producer accounts and ordinary holder accounts.
- Global state: total_verified_production_kwh, total_minted, total_redeemed, circulating.
- Invariant check after every state-changing operation.

Step 2 – Minting (Production)
- A producer reports a positive quantity of verified kWh.
- That quantity is added to total_verified_production.
- The corresponding EUs are credited to the producer (minus any protocol fee).

Step 3 – Transfer
- Any account can send EUs to any other account (atomic, no negative balances).

Step 4 – Redemption
- A holder burns EUs.
- total_redeemed increases and circulating decreases.
- This represents energy having been delivered.

Step 5 – Storage (Charge / Discharge)
- Storage accounts have capacity and a round-trip efficiency (e.g. 0.88).
- Charge: consume EUs → increase internal stored_kwh (apply part of efficiency loss).
- Discharge: decrease stored_kwh → mint new EUs equal to the effective energy delivered after remaining efficiency loss.
- Storage never creates net new energy; it only moves it in time.

Step 6 – Protocol Fee & Treasury (recommended)
- On every mint (production or storage discharge), take a small fee (default 1%).
- Send the fee to a dedicated Treasury account.
- Transfers can remain free or also carry a small fee.

Step 7 – Observability
- Clear snapshot of all balances, total verified production, circulating supply, backing ratio, and treasury balance.
- Event log that can be exported (e.g. CSV).

IMPLEMENTATION GUIDANCE
- Start with a simple in-memory Python simulation. Do not begin with a blockchain.
- Use clear classes or modules.
- Enforce invariants with explicit checks that raise errors if broken.
- Prefer readability and correctness over premature optimization.
- Keep EUs fungible in the first version.

SUCCESS CRITERIA
- A multi-day simulation can run in which producers mint, storage cycles, consumers redeem, and circulating supply stays ≤ verified production at every step.
- The code is easy for a human to read and extend.

Do not add governance tokens, complex oracles, cross-chain bridges, or regulatory wrappers until the core ledger above is solid and tested.
