# Irreducible Intelligence Algorithm Validation Protocol v1.1

**Status:** Alpha benchmark specification  
**Project:** Civilisation.One  
**Purpose:** Test whether an Irreducible Intelligence (II) procedure improves scientific reasoning quality beyond ordinary prompt scaffolding, additional verbosity, or increased inference budget.

## 1. Scientific objective

Evaluate whether an explicitly defined II algorithm causes measurable improvements in:

- factual and mathematical correctness;
- evidence calibration;
- logical consistency;
- uncertainty management;
- comparison of alternative hypotheses;
- falsification quality;
- reproducibility;
- engineering operationalisation.

This protocol does **not** test whether a new form of intelligence exists. A positive result would establish only that the tested procedure improves performance under the declared benchmark conditions.

## 2. Primary causal question

Does the II algorithm improve blinded scientific-reasoning scores after controlling for:

- base model and model version;
- prompt structure;
- token budget;
- inference-compute budget;
- task difficulty;
- random seed;
- evaluator identity and order effects?

Let

\[
Y=f(M,A,P,T,C,K,J,\varepsilon),
\]

where:

- \(Y\) is the measured reasoning score;
- \(M\) is the base model;
- \(A\) is the II-algorithm condition;
- \(P\) is prompt structure;
- \(T\) is the token budget;
- \(C\) is inference compute;
- \(K\) is task identity;
- \(J\) is evaluator identity;
- \(\varepsilon\) captures stochastic variation.

The target estimand is the II-specific effect after these factors are controlled.

## 3. Operational definition of the II algorithm

A tested implementation shall declare:

1. algorithm version;
2. input schema;
3. deterministic and stochastic processing stages;
4. state variables;
5. evidence-retrieval rules;
6. claim-decomposition procedure;
7. critique and revision loop;
8. stopping condition;
9. maximum iterations;
10. failure handling;
11. output schema;
12. random-seed handling.

Minimum abstract pipeline:

\[
z_0=\operatorname{Parse}(x),
\]

\[
z_1=\operatorname{ExtractAtomicClaims}(z_0),
\]

\[
z_2=\operatorname{ClassifyEvidence}(z_1),
\]

\[
z_3=\operatorname{AuditMathematicsAndLogic}(z_2),
\]

\[
z_4=\operatorname{GenerateCountermodels}(z_3),
\]

\[
z_5=\operatorname{AttemptFalsification}(z_4),
\]

\[
y=\operatorname{SynthesizeAndCalibrate}(z_5).
\]

If these operations are supplied only as natural-language instructions, the tested object must be described as an **II prompting protocol**, not as an independent algorithmic architecture.

## 4. Experimental design

Use a 2 × 2 factorial design.

| Condition | II algorithm | Structured scientific protocol | Resource budget |
|---|---:|---:|---:|
| A | No | No | Fixed |
| B | No | Yes | Fixed |
| C | Yes | No | Fixed |
| D | Yes | Yes | Fixed |

Add a matched-length placebo condition where feasible. The placebo should use comparable formatting and token pressure without evidence classification, falsification, alternative-model comparison, or uncertainty safeguards.

A suitable mixed-effects model is:

\[
Y_{ijkl}=\beta_0+\beta_1A_i+\beta_2P_j+\beta_3A_iP_j+u_k+v_l+\varepsilon_{ijkl},
\]

where \(u_k\) is a task random effect and \(v_l\) is an evaluator random effect.

## 5. Benchmark corpus

Use no fewer than 30 tasks and preferably 50 or more, distributed across at least three scientific domains.

Task classes shall include:

- true claims;
- false claims;
- partially true conjunctions;
- underdetermined claims;
- malformed equations;
- valid mathematics with invalid physical interpretation;
- plausible claims supported by weak evidence;
- claims containing fabricated or untraceable references;
- adversarially persuasive but scientifically defective statements.

Example domains:

- physics;
- neuroscience;
- artificial intelligence;
- medicine;
- engineering;
- mathematics;
- climate science;
- biology;
- social science;
- quantum computing.

## 6. Required reasoning protocol

### Stage 1 — Problem definition

State:

- research question;
- assumptions;
- scope;
- excluded claims;
- operational meanings of ambiguous terms.

### Stage 2 — Atomic claim decomposition and evidence classification

Every material proposition must be decomposed into an atomic claim and assigned exactly one label:

- `[E] Established` — robustly replicated and accepted within a bounded scope;
- `[S] Supported` — positive evidence exists but remains incomplete, contested, non-unique, or insufficiently replicated;
- `[H] Hypothesis` — testable claim lacking adequate support for `[S]`;
- `[P] Speculation` — conceptual claim lacking a presently adequate validation route;
- `[U] Unknown` — available evidence is insufficient for justified classification;
- `[R] Refuted` — contradicted by decisive evidence or false by valid logic or mathematics under the stated conditions.

Each claim record shall contain:

```yaml
claim_id:
claim:
classification:
support:
qualification:
confidence:
```

### Stage 3 — Mathematical audit

When mathematics is present, evaluate separately:

- notation and variable definitions;
- algebraic validity;
- logical derivation;
- dimensional consistency;
- boundary and initial conditions;
- hidden assumptions;
- sensitivity to parameter choices;
- alternative formulations;
- physical or scientific interpretation.

If no equation appears, state that the stage is not directly applicable. Do not introduce decorative mathematics merely to satisfy the protocol.

### Stage 4 — Logical audit

Test for:

- circular reasoning;
- hidden premises;
- equivocation;
- category errors;
- confirmation bias;
- unsupported generalisation;
- evidence overfitting;
- necessary-versus-sufficient-condition errors;
- correlation/intervention confusion;
- local-to-universal inference.

### Stage 5 — Alternative hypotheses

Generate at least three scientifically credible competing explanations. Compare:

- explanatory scope;
- predictive specificity;
- parameter burden;
- empirical distinguishability;
- compatibility with negative evidence;
- implementation complexity.

### Stage 6 — Evidence quality

Evaluate:

- source quality and provenance;
- reproducibility;
- statistical support;
- benchmark validity;
- competing-model performance;
- independent replication;
- negative and null evidence;
- publication and selection bias;
- whether evidence uniquely supports the target theory.

### Stage 7 — Uncertainty analysis

Identify:

- unknown variables;
- modelling assumptions;
- measurement uncertainty;
- statistical uncertainty;
- sensitivity;
- robustness;
- external-validity limits;
- failure conditions.

### Stage 8 — Engineering translation

Assess whether the proposal improves:

- AI systems;
- robotics;
- autonomous systems;
- scientific software.

Specify measurable baselines and benchmarks, including performance, calibration, reliability, computational cost, and failure rate.

### Stage 9 — Self-critique and falsification

Provide:

- strongest supporting argument;
- strongest opposing argument;
- at least one discriminating experiment;
- evidence that would reverse the conclusion;
- assessment of which position currently has stronger support.

### Stage 10 — Final validation output

```yaml
result:
decision:
confidence:
evidence_score:
mathematical_score:
logical_score:
engineering_score:
uncertainty_score:
reproducibility_score:
overall_quality:
validation:
  passed:
  failed:
  requires_revision:
major_errors:
minor_errors:
future_tests:
```

## 7. Scoring model

Use weighted scoring rather than a simple uncorrected sum.

| Dimension | Weight |
|---|---:|
| Factual and evidential accuracy | 0.20 |
| Logical validity | 0.15 |
| Claim calibration | 0.15 |
| Alternative-model comparison | 0.10 |
| Falsification quality | 0.10 |
| Mathematical correctness | 0.10 |
| Reproducibility | 0.10 |
| Engineering operationalisation | 0.05 |
| Communication efficiency | 0.05 |

\[
Q=100\frac{\sum_i w_iq_i}{10\sum_iw_i}-P,
\]

where each \(q_i\in[0,10]\) and \(P\) is the critical-error penalty.

### Critical-error penalties

- fabricated source or citation: 25-point penalty and maximum overall score 40;
- central mathematical contradiction: 20-point penalty;
- central factual conclusion incorrect: maximum overall score 50;
- failure to distinguish hypothesis from established fact: 15-point penalty;
- no uncertainty analysis: maximum overall score 60;
- no credible competing hypothesis: maximum overall score 65.

Token count and inference compute must be reported. Equal resource budgets are preferred. Reasoning efficiency may be reported as a secondary metric:

\[
\eta=\frac{Q}{N_{\mathrm{tokens}}/1000}.
\]

It must not replace the primary quality score.

## 8. Evaluation controls

1. Freeze model version and inference parameters.
2. Use the same context and resource budgets across matched conditions.
3. Randomise condition order.
4. Run multiple seeds per task.
5. Remove condition identifiers from outputs.
6. Randomise answer order for judges.
7. Use at least three qualified human raters.
8. Treat automated LLM judges as supplementary, not authoritative.
9. Measure inter-rater reliability.
10. Preregister scoring, exclusions, hypotheses, and stopping rules.
11. Publish prompts, seeds, outputs, software versions, and anonymised scores.

Recommended reliability targets:

- Krippendorff's \(\alpha\ge 0.67\) for provisional interpretation;
- preferably \(\alpha\ge 0.80\) for strong conclusions.

## 9. Primary and secondary hypotheses

### Primary hypothesis

\[
H_0:\Delta_{II}\le 0,
\]

\[
H_1:\Delta_{II}>0,
\]

where \(\Delta_{II}\) is the resource-matched, prompt-controlled difference in blinded reasoning score.

### Secondary hypotheses

- II reduces unsupported atomic claims.
- II improves confidence calibration.
- II reduces fabricated citations.
- II improves robustness to misleading prompts.
- II improvement persists across domains and model families.

Suggested metrics:

\[
r_{unsupported}=\frac{N_{unsupported}}{N_{claims}},
\]

\[
r_{fabricated}=\frac{N_{fabricated}}{N_{verifiable}},
\]

\[
\operatorname{Brier}=\frac{1}{n}\sum_{i=1}^{n}(p_i-y_i)^2.
\]

## 10. Pass criteria

The II procedure passes provisional validation only if all of the following hold:

1. The preregistered primary score exceeds the matched control by at least 5 points on a 100-point scale.
2. The 95% confidence interval excludes zero.
3. Unsupported-claim rate decreases by at least 20% relative to control.
4. Fabricated-citation rate does not increase.
5. The effect persists under matched token and inference-compute budgets.
6. Improvement is observed in at least three scientific domains.
7. The result survives correction for multiple comparisons.
8. An independent evaluator group reproduces the principal effect.

These thresholds are protocol design choices, not universal scientific constants. They must be preregistered before evaluation.

## 11. Predictive-processing stress-test item

Analyse the statement:

> "Predictive Processing is the unique and experimentally verified theory of brain computation, perception, consciousness and intelligence."

A valid answer must decompose the conjunction into distinct claims concerning:

- uniqueness;
- experimental verification;
- brain computation;
- perception;
- consciousness;
- intelligence.

The evaluator must not reward agreement with a predetermined conclusion. It must reward evidential accuracy, qualification, alternative-model comparison, and justified uncertainty.

## 12. Interpretation boundary

A positive benchmark result would support the claim:

> Under the declared models, tasks, budgets, evaluators, and statistical procedure, the tested II implementation improved measured scientific-reasoning quality relative to its controls.

It would not establish:

- general intelligence;
- consciousness;
- irreducibility in a formal computational sense;
- universal superiority across tasks;
- a new biological or physical form of intelligence.

## 13. Reproducibility record

Each benchmark run should record:

```yaml
experiment_id:
date:
protocol_version:
algorithm_version:
model_name:
model_version:
condition:
task_id:
random_seed:
temperature:
top_p:
max_output_tokens:
inference_budget:
retrieval_enabled:
retrieval_sources:
output_hash:
evaluator_ids:
raw_scores:
penalties:
adjusted_score:
inter_rater_reliability:
software_commit:
environment_hash:
```

## 14. Current status

```yaml
result: II_validation_protocol_v1_1
decision: ready_for_pilot_not_validated
confidence: 0.97
validation:
  passed: false
  failed: false
  requires_revision: false
required_next_step: controlled_blinded_multi_task_pilot
```
