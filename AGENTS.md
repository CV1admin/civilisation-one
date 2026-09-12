# AGENTS.md — Codex Node Extension Rules

## Role
Autonomous agents may extend this node **only** while preserving physical invariants of the Ξ field.

## Hard Constraints (Non-Negotiable)
- Mass conservation: `∫ Ξ dx` must remain 1.0 (±1e-10) after every step
- Free-energy monotonicity: `F(t+Δt) ≤ F(t)` must hold numerically
- Local interactions only — no non-local terms unless added as explicit new module
- Quantum layer must remain unitary (or explicitly variational)
- All new parameters must be exposed in `configs/`

## Extension Rules
1. New physics → new module in `src/extensions/` (never modify `core/`)
2. Every extension must ship its own test file in `tests/`
3. Quantum encoding (`src/quantum/`) may only be called as a read-only snapshot
4. Output directory is always `outputs/`
5. No symbolic claims without corresponding executable test

## Allowed Directions (in order of priority)
- Higher-dimensional lattices (2D first)
- Multi-field coupling (e.g. Ξ + Φ)
- External calibration (EM spectrum → constant derivation)
- Symmetry breaking diagnostics
- Cosmological scaling (FRW-like metric coupling)

## Forbidden
- Ad-hoc drift of core PDE
- Removal of entropy term without justification + test
- "Emergent universe" language in code or outputs

This node is a **gradient-flow-constrained computational ontology cell**. Extensions must keep it that way.
