# Rejection Gallery

A useful alpha lab should reject bad candidates quickly. This page collects the failure modes the public demo is designed to catch.

| Failure mode | What triggers it | Why it matters | Current check |
|---|---|---|---|
| Future field leakage | A formula references `forward_return`, `label_*`, or a field outside the allowed contract | A model that sees the answer is not research | `FormulaContract` and `FormulaError` reject it before evaluation |
| Broken time order | The panel is not sorted by `asset` and `date` | Rolling and delta operators become ambiguous | `evaluate_formula` rejects unsorted panels |
| In-sample comfort | A formula only looks acceptable before the split date | Selection is not evidence | `evaluate_candidate` reports OOS Rank IC only after the split |
| Cost erosion | Gross top-quintile return is positive but turnover costs erase it | A signal can be statistically interesting but untradable | `PromotionGate` checks cost-adjusted net return |
| Turnover overload | Candidate changes positions too aggressively | Capacity and implementation risk matter | `PromotionGate.max_turnover` blocks promotion |

## Demo record

The current synthetic demo is intentionally conservative: the candidate is evaluated, transaction costs are applied, and the final verdict is rejection under the frozen gate. That is not a failed repo state; it is the behavior this repo is meant to show.

## Next useful artifact

A stronger version would add a batch table of 10-30 candidate formulas, with one row per rejection reason. That would make the lab look more like an actual research queue rather than a single smoke test.
