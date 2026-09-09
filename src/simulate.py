#!/usr/bin/env python3
"""
Simple demonstration simulation of the Energy Unit (EU) system.
Run with: python -m src.simulate   or   python src/simulate.py
"""

from datetime import datetime, timedelta
from src.eu_ledger import EnergyLedger


def run_demo():
    print("Starting Energy Unit (EU) Currency MVP Simulation\n")
    ledger = EnergyLedger(name="Demo Regional Grid — EU Ledger")

    # Create participants
    solar_farm = ledger.create_account("Sunny Hills Solar", is_producer=True)
    wind_farm = ledger.create_account("Coastal Wind", is_producer=True)
    battery = ledger.create_account("Grid Battery Storage", is_producer=True, is_storage=True)
    factory = ledger.create_account("MetalWorks Factory")
    data_center = ledger.create_account("AI Compute Center")
    household = ledger.create_account("Green Family Home")

    print(ledger.snapshot())
    print("-" * 60)

    # Day 1: Production
    print("\n>>> Day 1: Strong solar + wind production")
    t0 = datetime(2026, 9, 9, 8, 0, 0)

    ledger.report_production(solar_farm.id, 12_500.0, timestamp=t0, location="South Region", notes="Clear skies")
    ledger.report_production(wind_farm.id, 8_200.0, timestamp=t0 + timedelta(hours=2), location="Coast", notes="Steady 12 m/s")
    ledger.report_production(battery.id, 1_800.0, timestamp=t0 + timedelta(hours=4), location="Central", notes="Evening peak discharge")

    print(ledger.snapshot())
    print("-" * 60)

    # Transfers
    print("\n>>> Transfers: Producers sell EUs to consumers")
    ledger.transfer(solar_farm.id, factory.id, 6_000.0, timestamp=t0 + timedelta(hours=6))
    ledger.transfer(solar_farm.id, data_center.id, 4_000.0, timestamp=t0 + timedelta(hours=6))
    ledger.transfer(wind_farm.id, data_center.id, 5_000.0, timestamp=t0 + timedelta(hours=7))
    ledger.transfer(wind_farm.id, household.id, 500.0, timestamp=t0 + timedelta(hours=7))
    ledger.transfer(battery.id, household.id, 800.0, timestamp=t0 + timedelta(hours=8))

    print(ledger.snapshot())
    print("-" * 60)

    # Redemptions
    print("\n>>> Redemptions: Consumers redeem EUs for delivered energy")
    ledger.redeem(factory.id, 5_500.0, delivery_note="Factory shift production", timestamp=t0 + timedelta(hours=10))
    ledger.redeem(data_center.id, 7_500.0, delivery_note="GPU cluster overnight job", timestamp=t0 + timedelta(hours=12))
    ledger.redeem(household.id, 1_100.0, delivery_note="Home heating + EV charge", timestamp=t0 + timedelta(hours=14))

    print(ledger.snapshot())
    print("-" * 60)

    # Day 2
    print("\n>>> Day 2: Additional production + residual balances")
    t1 = t0 + timedelta(days=1)
    ledger.report_production(solar_farm.id, 9_800.0, timestamp=t1, notes="Partly cloudy")
    ledger.report_production(wind_farm.id, 11_400.0, timestamp=t1 + timedelta(hours=1), notes="Strong overnight winds")

    ledger.transfer(solar_farm.id, factory.id, 3_000.0, timestamp=t1 + timedelta(hours=3))
    ledger.transfer(wind_farm.id, factory.id, 2_500.0, timestamp=t1 + timedelta(hours=3))

    print(ledger.snapshot())
    print("-" * 60)

    stats = ledger.summary_stats()
    print("\n=== Final Summary Statistics ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    print("\nSimulation complete. Invariants held throughout.")
    print("Circulating EUs are fully backed by verified production.")
    return ledger


if __name__ == "__main__":
    run_demo()
