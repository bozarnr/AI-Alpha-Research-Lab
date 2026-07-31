# Rejection Gallery

A useful alpha lab should reject bad candidates quickly and preserve why they failed. This page collects the failure modes the public demo is designed to catch, plus the code helpers that turn rejected candidates into inspectable evidence.

| Failure mode | What triggers it | Why it matters | Current check |
|---|---|---|---|
| Future field leakage | A formula references `forward_return`, `label_*`, or a field outside the allowed contract | A model that sees the answer is not research | `FormulaContract` and `FormulaError` reject it before evaluation |
| Broken time order | The panel is not sorted by `asset` and `date` | Rolling and delta operators become ambiguous | `evaluate_formula` rejects unsorted panels |
| In-sample comfort | A formula only looks acceptable before the split date | Selection is not evidence | `evaluate_candidate` reports OOS Rank IC only after the split |
| Cost erosion | Gross top-quintile return is positive but turnover costs erase it | A signal can be statistically interesting but untradable | `PromotionGate` checks cost-adjusted net return |
| Turnover overload | Candidate changes positions too aggressively | Capacity and implementation risk matter | `PromotionGate.max_turnover` blocks promotion |

## Implemented loop accounting

- `CandidateRecord.from_result` converts evaluator output into a compact audit record.
- `summarize_loop` reports total candidates, promoted/rejected counts, best diagnostics, and rejection-reason counts.
- `rejection_gallery` ranks rejected candidates by OOS IC and OOS net return so near-misses can be reviewed without calling them deployable.

## Demo record

The current synthetic demo is intentionally conservative: the candidate is evaluated, transaction costs are applied, the loop summary is emitted, and the final verdict is rejection under the frozen gate. That is not a failed repo state; it is the behavior this repo is meant to show.
