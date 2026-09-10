# Signed Measurement Design (Stage 2 – Draft)

This document makes the Trusted Measurement stage more concrete.  
It defines a simple format for a signed energy measurement and shows how the ledger would use it.

The goal is still the same:  
**Only mint Energy Units when there is strong evidence that real electricity was produced or discharged.**

---

## 1. Simple Measurement Format

A measurement report should contain at least these fields:

| Field            | Meaning                                      | Example                  |
|------------------|----------------------------------------------|--------------------------|
| device_id        | Unique identity of the meter or gateway      | "meter-solar-042"        |
| kwh              | Amount of energy measured                    | 14200.5                  |
| timestamp        | When the measurement was taken (UTC)         | 2026-09-10T14:30:00Z     |
| measurement_type | "production", "discharge", or "consumption"  | "production"             |
| signature        | Digital signature of the above data          | (long cryptographic string) |
| public_key       | Public key that can verify the signature     | (corresponding public key) |

Only the combination of these fields, when the signature is valid, should be accepted.

---

## 2. What the Ledger Must Check

Before creating any new Energy Units, the ledger should perform these checks in order:

1. **Is the public key approved?**  
   The ledger keeps a short list of trusted public keys.  
   If the key is not on the list, reject the measurement.

2. **Is the signature valid?**  
   Using the public key, verify that the signature matches the data.  
   If the signature is invalid, reject the measurement.

3. **Are the values sensible?**  
   - kwh must be positive  
   - timestamp should not be too far in the future or the distant past  
   - device_id must be known / registered

4. **Only then mint**  
   If all checks pass, create the Energy Units (minus the protocol fee) and record the measurement as verified production.

Any failure at steps 1–3 means **no Energy Units are created**.

---

## 3. Minimal Code Sketch (How the Ledger Would Change)

Current simple version (simulation only):

```python
ledger.report_production(producer_id, kwh)
```

New version that requires a signed measurement:

```python
def report_signed_measurement(
    self,
    device_id: str,
    kwh: float,
    timestamp: datetime,
    measurement_type: str,
    signature: str,
    public_key: str,
):
    # 1. Check the public key is on the approved list
    if public_key not in self.approved_keys:
        raise PermissionError("Public key not approved")

    # 2. Verify the signature (pseudocode)
    if not verify_signature(
        data={
            "device_id": device_id,
            "kwh": kwh,
            "timestamp": timestamp.isoformat(),
            "measurement_type": measurement_type,
        },
        signature=signature,
        public_key=public_key,
    ):
        raise ValueError("Invalid signature")

    # 3. Basic sanity checks
    if kwh <= 0:
        raise ValueError("Energy amount must be positive")

    # 4. Only now mint (same logic as before, with fee)
    fee = round(kwh * self.mint_fee_rate, 6)
    net = round(kwh - fee, 6)

    # Credit the appropriate account and update totals...
    # (rest of existing minting logic)
```

The rest of the system (transfers, redemptions, storage rules, circulating ≤ production invariant) stays exactly the same.

---

## 4. Starting Small – Approved Keys List

At the beginning the list of approved public keys should be very short and manually managed.

Example:

```text
approved_keys = {
    "meter-solar-042": "public_key_here",
    "battery-gateway-007": "another_public_key_here",
}
```

Only measurements signed by these keys are accepted.  
This makes the system auditable and limits the damage if one key is ever compromised.

Later, more sophisticated methods (multiple signatures, decentralized verification, hardware security modules, etc.) can be added.  
They are not required for a first working version.

---

## 5. What Success Looks Like at This Stage

We can consider the design successful when:

- The ledger rejects unsigned or invalid measurements.
- Valid signed measurements correctly create Energy Units.
- The circulating ≤ production rule still holds.
- The design is simple enough that a pilot with one or two real meters is realistic.

---

## 6. What Comes After

Once this design is stable:

- A small pilot can be planned (Stage 3).
- Real meters or gateways can be configured to produce the signed reports.
- The simulation can be extended to accept real signed data instead of invented numbers.

Until then, the system remains a well-structured simulation with a clear path to the physical world.

---

*This is a draft design. It will be refined as we learn more.*
