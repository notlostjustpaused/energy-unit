# Trusted Measurement — Stage 2

This document describes how the Energy Unit system can move from pure simulation to accepting real-world energy data in a way that is difficult to fake.

The goal is simple but hard:

> The ledger should only create new Energy Units when it has strong evidence that real electricity was actually produced or discharged.

---

## Why This Stage Matters

In the current simulation, minting happens when a program simply says “this much energy was produced.”

That is fine for testing rules.  
It is not fine for the real world.

If anyone can claim production without proof, they can create Energy Units out of nothing.  
That would break the core promise of the system: digital claims must stay linked to real, verified energy.

Solving this problem is often called the “oracle problem” — connecting a digital system to the physical world without creating an easy point of failure or fraud.

---

## What “Trusted” Means Here

For a measurement to be accepted by the ledger, three conditions should be met:

1. **A real measurement occurred**  
   An electricity meter (or equivalent device) recorded production, consumption, or storage discharge.

2. **The measurement is hard to alter**  
   The data should be digitally signed so that changing the numbers would be detectable.

3. **The ledger verifies before acting**  
   The system checks the signature and only then mints Energy Units.

Until these conditions are satisfied, the system should remain a simulation.

---

## Practical First Approach (Start Small)

We do not need a perfect global solution at the beginning.  
A realistic first version can be deliberately limited:

### Components

- A small number of high-quality meters (industrial or utility-grade).
- Each meter (or a trusted gateway attached to it) can produce a signed report containing:
  - Device identity
  - Amount of energy (kWh)
  - Timestamp
  - Digital signature
- The ledger keeps a short list of public keys it is allowed to trust.
- When a signed report arrives, the ledger:
  1. Checks that the public key is on the approved list
  2. Verifies the signature
  3. Only then creates the corresponding Energy Units (minus the protocol fee)

### Why start small

- The set of trusted devices remains auditable.
- It is easier to detect problems when only a few sources exist.
- A future pilot can begin with just one or two real installations instead of requiring a large network.

---

## How This Changes the Current Ledger

In the simulation we have today, minting looks roughly like this:

```text
ledger.report_production(producer_id, kwh)
```

In a trusted-measurement version, it would look more like this:

```text
ledger.report_signed_measurement(
    device_id,
    kwh,
    timestamp,
    signature,
    public_key
)
```

The ledger would reject any measurement that fails signature verification or comes from an unknown device.

All other rules stay the same:
- Circulating Energy Units can never exceed total verified production
- Storage still has efficiency losses
- Redemption still burns units
- The protocol fee still applies

---

## What This Stage Does Not Solve Yet

- It does not create a fully decentralized global network of meters.
- It does not eliminate the need for some initial trust in the chosen devices or gateways.
- It does not address regulation, utility agreements, or large-scale deployment.

Those issues belong to later stages (pilot and broader use).  
Trying to solve everything at once usually produces weak systems.

---

## Success Criteria for Stage 2

We can consider this stage successful when:

- The ledger can accept a signed measurement and mint Energy Units only after verifying it.
- Invalid or unsigned measurements are rejected.
- The same physical scarcity invariant still holds.
- The design remains simple enough that a small real-world pilot is realistic.

---

## Relationship to the Overall Roadmap

- Stage 1 (Simulation) gave us clear rules and working code.
- Stage 2 (Trusted Measurement) is about feeding those rules with hard-to-fake real-world data.
- Stage 3 (Small Pilot) can only begin after Stage 2 is credible.
- Stage 4 (Broader Use) comes last.

This order protects the core idea: digital claims should remain tightly linked to real energy.

---

*This document will be updated as the design becomes more concrete.*
