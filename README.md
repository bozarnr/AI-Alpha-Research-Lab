# AI Alpha Research Lab

A formula-alpha sandbox with hard rejection rules. The point is not to make a demo look profitable; it is to keep the research loop honest when a candidate fails after time-ordering, out-of-sample checks, turnover, and costs.

## Showcase

- [Rejection Gallery](reports/rejection-gallery.md): leakage, broken time order, cost erosion, turnover overload, and rejection accounting.

## Related repos

- [AI-Alpha-Research-Lab](https://github.com/bozarnr/AI-Alpha-Research-Lab): formula search, evaluation, and rejection gates.
- [Paper-Alpha-Replications](https://github.com/bozarnr/Paper-Alpha-Replications): replication notes with claim ceilings.
- [Quant-Research-Toolkit](https://github.com/bozarnr/Quant-Research-Toolkit): reusable checks for factor panels and diagnostics.
- [Strategy-Game-Agents](https://github.com/bozarnr/Strategy-Game-Agents): repeated-choice experiments and baseline agents.

## What is here

- Allow-listed formula language: `rank`, `delta`, `mean`, and arithmetic.
- Point-in-time evaluation on stock-date panels.
- Promotion gate for OOS IC, turnover, and cost-adjusted return.
- Rejection-gallery helpers that turn failed candidates into inspectable evidence.
- Deterministic synthetic-data demo that rejects the candidate.
- Tests for parsing, future-field rejection, rejection accounting, and promotion logic.

## Run

```bash
python -m pip install -e .
python -m ai_alpha_lab.demo
python -m unittest discover -s tests -v
```

## Evidence boundary

The first public record is intentionally conservative. An AutoAlpha-style study ran through the search and validation pipeline, but the frozen protocol produced zero final candidates. See [`evidence/validation-summary.md`](evidence/validation-summary.md), [`reports/rejection-gallery.md`](reports/rejection-gallery.md), and [`research_state.json`](research_state.json). The public disclosure boundary is recorded in [`DISCLOSURE.md`](DISCLOSURE.md), with a tiny synthetic candidate-log fixture in `sample_data/`.

## Layout

```text
src/ai_alpha_lab/  public research core
tests/             regression and safety checks
evidence/          short evidence records
reports/           recruiter-readable public summaries
research_state.json current claim ceiling and reopen condition
```

## Not included

- private data, employer code, credentials, or proprietary research assets
- tradable-performance claims
- automatic capital deployment
