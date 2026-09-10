#!/usr/bin/env python3
"""
Short demonstration of Stage 2: signed measurements.
Shows both a valid measurement (accepted) and an invalid one (rejected).
"""

from datetime import datetime
from src.eu_ledger import EnergyLedger


def main():
    print("=" * 70)
    print("Stage 2 Demo — Signed Measurements")
    print("=" * 70)

    ledger = EnergyLedger(name="Trusted Measurement Demo", mint_fee_rate=0.01)

    # Create a producer account that will receive the minted EUs
    solar = ledger.create_account("Sunny Hills Solar", is_producer=True)

    # Register one trusted device + its public key
    device_id = "meter-solar-042"
    public_key = "pubkey-solar-042-example"
    ledger.add_approved_key(device_id, public_key)
    print(f"\nApproved device: {device_id}")

    # --- Valid measurement ---
    print("\n1. Submitting a VALID signed measurement...")
    ts = datetime(2026, 9, 10, 14, 30, 0)
    kwh = 14200.0
    measurement_type = "production"

    # Create the expected signature (this is what a real meter/gateway would produce)
    valid_signature = f"SIG:{device_id}:{kwh}:{ts.isoformat()}:{measurement_type}:{public_key}"

    try:
        event = ledger.report_signed_measurement(
            device_id=device_id,
            kwh=kwh,
            timestamp=ts,
            measurement_type=measurement_type,
            signature=valid_signature,
            public_key=public_key,
            producer_account_id=solar.id,
            notes="Clear sky production",
        )
        print(f"   Accepted. Minted net {event.net_minted:.1f} EU (fee {event.fee_eu:.1f} EU)")
    except Exception as e:
        print(f"   Rejected: {e}")

    print("\n" + ledger.snapshot())

    # --- Invalid measurement (bad signature) ---
    print("\n2. Submitting an INVALID signed measurement (tampered signature)...")
    bad_signature = "SIG:fake-or-tampered-data"

    try:
        ledger.report_signed_measurement(
            device_id=device_id,
            kwh=5000.0,
            timestamp=datetime(2026, 9, 10, 15, 0, 0),
            measurement_type="production",
            signature=bad_signature,
            public_key=public_key,
            producer_account_id=solar.id,
        )
        print("   Accepted (this should not happen)")
    except Exception as e:
        print(f"   Correctly rejected: {e}")

    # --- Unknown device ---
    print("\n3. Submitting a measurement from an UNKNOWN device...")
    try:
        ledger.report_signed_measurement(
            device_id="meter-unknown-999",
            kwh=3000.0,
            timestamp=datetime(2026, 9, 10, 16, 0, 0),
            measurement_type="production",
            signature="whatever",
            public_key="some-key",
            producer_account_id=solar.id,
        )
        print("   Accepted (this should not happen)")
    except Exception as e:
        print(f"   Correctly rejected: {e}")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("Valid measurements create Energy Units.")
    print("Invalid or unknown-device measurements are rejected.")
    print("=" * 70)


if __name__ == "__main__":
    main()
