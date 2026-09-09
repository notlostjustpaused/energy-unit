# Quick Start — Energy Unit Simulation

## How to run it

1. Open a terminal
2. Go into the project folder:
   ```bash
   cd energy-unit
   ```
3. Run the main simulation:
   ```bash
   python -m src.simulate_v2
   ```
   (If that doesn’t work, try `python3 -m src.simulate_v2`)

## What you will see

The program will simulate 3 days of electricity production, storage, trading, and use.

At the end it will show:
- How much real electricity was produced
- How many Energy Units (EUs) are still in circulation
- How much went into the shared Treasury
- That the system stayed honest (circulating units never exceeded real production)

## What the numbers mean

- **Verified production** = real electricity that was measured
- **Circulating EUs** = digital units still being held by someone
- **Fees collected / Treasury** = the small 1% that builds a shared pool
- **Backing ratio** = circulating ÷ production (this should always stay at or below 1.0)

## Important

This is a **simulation** (a computer model).  
It is not connected to real power plants or real money yet.  
It is a clear foundation that can later be connected to the real world.
