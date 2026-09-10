# Roadmap — From Simulation to Real Energy Units

This document explains the realistic stages needed to turn the current computer simulation into something that could eventually work with real electricity.

We are deliberately going in this order so the system stays honest at every step.

---

## Stage 1: Simulation (Current Stage)

**Where we are now.**

- Everything happens inside a computer program.
- We invent the production numbers for the sake of testing.
- The rules (especially “circulating EUs can never exceed verified production”) are already enforced.
- Goal of this stage: Make the rules clear, test incentives, and create a solid foundation.

**Status: Complete enough to move forward.**

---

## Stage 2: Trusted Measurement (The Hardest Technical Step)

The biggest challenge is not the digital ledger itself.  
It is answering this question reliably:

> “How do we know the electricity was really produced?”

In the real world this usually comes from electricity meters.

### What is needed
- Meters that can securely report how much energy was produced or consumed.
- A way for those reports to be cryptographically signed so they cannot be easily faked.
- The ledger only mints new Energy Units when it receives a valid, signed measurement.

This is often called the “oracle problem” — connecting the digital system to the physical world without creating a weak point that can be cheated.

### Realistic first version
- Start with a very small number of trusted meters (for example one solar installation and one battery).
- Use existing industrial or utility-grade metering where possible.
- Keep the set of trusted data sources small and auditable at first.

---

## Stage 3: Small Pilot

Once trusted measurements exist, run a limited real-world test.

Possible form:
- One or a few real producers (solar, wind, or battery).
- A small number of consumers who are willing to receive and redeem Energy Units.
- The digital ledger records everything according to the same rules we already have.

Goal of the pilot:
- Prove that the full cycle works with real energy: produce → mint → transfer → redeem.
- Discover practical problems (metering, timing, user experience, regulation) while the scale is still small.

---

## Stage 4: Broader Use

Only after a successful pilot does it make sense to expand.

At this point the system could:
- Support more producers and consumers.
- Add stronger decentralization of the measurement verification.
- Explore connections with existing energy markets, utilities, or other systems.
- Consider whether (and how) Energy Units might interact with regular money.

---

## Guiding Principle

Many projects launch a token first and only later try to connect it to something real.  
That usually leads to speculation without substance.

We are doing the opposite:

1. First make the rules clear and enforceable.
2. Then solve how to feed the system trustworthy real-world data.
3. Then test with real energy at small scale.
4. Only then consider wider adoption.

This order protects the core idea: **digital claims should stay tightly linked to real, verified energy.**

---

## What This Means Right Now

- The simulation and documentation we have built are the foundation.
- The next meaningful technical work is understanding and designing how trusted meter data would enter the system.
- No token launch, fundraising, or large claims are needed (or wise) until Stage 2 and Stage 3 are much clearer.

This roadmap will be updated as we learn more.
