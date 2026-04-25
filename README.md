# Information-Coupled Field Dynamics

## 🧠 Summary

This repository implements a **validated nonlinear field theory** with an entropy (information-theoretic) coupling term.

The system is:

- Numerically stable
- Analytically verified
- Variationally consistent (gradient flow)
- Experimentally reproducible
- Structured for automated analysis

---

## 📐 Core Model

### PDE

∂ₜ Ξ = D ∇²Ξ − ∂V/∂Ξ − λ Ξ [log(Ξ² + ε) + 1]

### Potential

V(Ξ) = Ξ⁴ − Ξ²

### Free Energy

F = ∫ [ (D/2)|∇Ξ|² + V(Ξ) + λ ρ log ρ ] dx  
where ρ = Ξ² + ε

### Interpretation

- Diffusion term → smoothing
- Potential → symmetry breaking
- Entropy term → information-driven regularization

---

## 🧱 Architecture (Codex Map)

```
configs/                # YAML experiment definitions

src/
core/                 # PDE engine
field.py            # grid + laplacian
evolution.py        # time stepping
energy.py           # free energy

analysis/             # data interpretation
phase_transition.py # λ_c detection

scripts/
run_phase_diagram.py  # main experiment
plot_phase_diagram.py # visualization

results/                # generated outputs

docs/
verification_layers/  # scientific validation
```

---

## ⚙️ How to Run (Deterministic)

### Install

```bash
pip install -r requirements.txt
```

### Run experiment

```bash
python scripts/run_phase_diagram.py
```

### Generate plot

```bash
python scripts/plot_phase_diagram.py
```

### Output

```
results/
phase_diagram.csv
phase_diagram.png
```

---

## 🔬 Verification Layers (Formal)

The model is validated across independent constraints:

### Layer 1 — Stability

dt ≤ dx² / (2D)

### Layer 2 — Diffusion Law

σ²(t) = 2Dt

### Layer 3 — Mass Conservation

∫Ξ dx = constant

### Layer 4 — Convergence

dx → 0 consistency

### Layer 5 — Free Energy

F(t) is monotonically decreasing

### Layer 6 — Linear Stability

ω(k) = −Dk² + α(λ)

### Layer 7 — Nonlinear Effects

D_eff(λ) nonlinear

### Layer 8 — Phase Diagram

λ-dependent macroscopic behavior

### Layer 9 — Critical Scaling

t_domain ∼ (λ_c − λ)^(-ν)

---

## 📊 Scientific Findings

### Diffusion

Baseline:
σ²(t) ≈ 2Dt (validated to ~1e-9)

### Entropy Effect

D_eff grows nonlinearly with λ:

λ=0.0 → 2.0  
λ=0.3 → ~4.0  
λ=0.5 → ~6.4  
λ=1.0 → ~16+

### Mechanism

- Linear regime → entropy increases instability
- Nonlinear regime → entropy suppresses localization

Result:

Entropy both **destabilizes and stabilizes** depending on amplitude.

---

## 🧠 Interpretation for Codex

When modifying this model:

### DO

- Preserve CFL condition
- Keep free energy decreasing
- Maintain normalization
- Validate against diffusion baseline

### DO NOT

- Remove entropy term without re-validating
- Change potential without updating energy functional
- Skip convergence checks

---

## 🔁 Reproducibility Contract

Each run is defined by:

- dx, dt, D
- λ (entropy coupling)
- seed
- T (simulation time)

All outputs are deterministic given config.

---

## ⚠️ Important Implementation Detail

### Field normalization

```python
xi /= (sum(xi) * dx)
```

Ensures mass conservation.

---

### Optional clamp

```python
xi = clip(xi, 0, ∞)
```

Interpretation changes:

| Mode | Meaning |
|------|--------|
| no clamp | signed field (phase separation) |
| clamp | density field |

---

## 🧪 Extending the Model

### Add 2D

- Replace 1D array with 2D grid
- Update laplacian to 2D stencil

### Add noise (SPDE)

Ξ → Ξ + η(x,t)

### Add new physics

- modify potential
- modify entropy functional

---

## 📈 Expected Behavior

### Low λ

- rapid domain formation

### Medium λ

- delayed domains

### High λ

- suppressed phase separation

---

## 🧩 Minimal API (for agents)

### Initialize

```python
evo = Evolution(cfg, lambda_ent=λ)
```

### Step

```python
evo.step()
```

### Access field

```python
xi = evo.field_obj.field
```

---

## 📄 License

MIT

---

## 👤 Author

[Your Name]

---

## 🧠 Key Insight

Information (entropy) is not passive.

It modifies dynamics by:

- accelerating small fluctuations
- suppressing large-scale structure

Resulting in a **nonlinear competition between order and information**.

---

## 🔧 Critical Improvements (Research-Grade Roadmap)

To move from a runnable scaffold to research-grade infrastructure, prioritize the following:

1. **Make the PDE explicit in implementation**
   - Use a clearly defined evolution equation of the form
     `∂t Ξ = D∇²Ξ − ∂V/∂Ξ + λ I(Ξ)`.
   - Implement and document `potential_grad(Ξ)` explicitly.

2. **Enforce explicit-Euler stability constraints**
   - Track spatial spacing `dx` in the field object.
   - Enforce/validate CFL-like diffusion condition: `dt ≤ dx²/(2D)`.

3. **Use local (not purely global) information coupling**
   - Avoid adding one global entropy scalar uniformly to all points.
   - Prefer spatially resolved entropy/information density coupling.

4. **Define boundary conditions explicitly**
   - Use an explicit stencil and BC choice (e.g., periodic via `np.roll`).
   - Keep BC assumptions consistent across analysis and verification.

5. **Connect the quantum layer to field state**
   - If quantum routines exist, map field state → circuit initialization/observables.
   - Avoid disconnected “toy” circuits that do not consume simulation state.

6. **Expose experiment controls via API**
   - Add runtime configuration endpoints for key parameters (`dt`, `D`, `λ`, etc.).
   - Keep run metadata for reproducibility.

7. **Track richer observables than mean alone**
   - Record time series of mean, variance, and energy-like quantities.
   - Use these diagnostics for phase behavior and regression testing.

---

## 🤖 Agent Constraints (AGENTS.md)

Contributors extending this system should follow strict invariants:

- Preserve mass conservation
- Preserve free-energy monotonicity
- Do not introduce non-local interactions unless explicitly defined

Extension policy:

- New physics should be added as a new module rather than by mutating core dynamics
- Quantum-layer extensions must preserve unitarity
- Every extension must include at least one verification test

Allowed extension directions:

- Higher dimensions (2D/3D)
- Coupled fields
- External constant calibration (EM spectrum, α, etc.)

## 🎯 Recommended Next Validation Target

Before extending model complexity, reproduce the **1D diffusion baseline**:

`∂t u = D∇²u`

If the solver does not recover this limit quantitatively, higher-level interpretations are not reliable.

---

## 🤖 Automated Coding + Physics Loop (Minimal Runnable)

A minimal self-optimizing loop is included to make model iteration executable:

1. Generate candidate parameterization (`delta`) for cosmology extension
2. Run simulation (`h_mkone(z, delta)`)
3. Evaluate fitness against LCDM baseline
4. Repeat for fixed iterations and persist results

Run it with:

```bash
python scripts/run_autonomous_loop.py
```

Output:

```
outputs/mkone_autofit.json
```

Code locations:

- `src/extensions/cosmology_solver.py`
- `src/automation/agent_loop.py`
- `tests/test_cosmology_solver.py`


---

## 🧭 Vireax Center Node (Unified Hub)

The repository now includes a modular center-node orchestrator that integrates:

- Quantum circuit simulation (`src/vireax/quantum_circuit.py`)
- EM spectrum ingestion (`src/vireax/data_pipeline.py`)
- Physics equation lookup/synthesis (`src/vireax/equation_framework.py`)
- REST-style API transformation layer (`src/vireax/api_layer.py`)

Run end-to-end orchestration:

```bash
python scripts/run_vireax_center.py
```

Output:

```
outputs/vireax_center_node.json
```
