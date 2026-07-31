# AI Alpha Research Lab

A small formula-alpha sandbox with hard rejection rules. The point is not to make a demo look profitable; it is to keep the research loop honest when a candidate fails after time-ordering, out-of-sample checks, turnover, and costs.

这个项目放的是公开、可复查的因子研究骨架。样本内结果不算数，合成数据 demo 也不算策略。候选公式只有在时点安全、样本外、换手和成本门槛下还能站住，才允许往下一层走。

## Related repos

- [AI-Alpha-Research-Lab](https://github.com/bozarnr/AI-Alpha-Research-Lab): formula search, evaluation, and rejection gates.
- [Paper-Alpha-Replications](https://github.com/bozarnr/Paper-Alpha-Replications): replication notes with claim ceilings.
- [Quant-Research-Toolkit](https://github.com/bozarnr/Quant-Research-Toolkit): reusable checks for factor panels and diagnostics.
- [Strategy-Game-Agents](https://github.com/bozarnr/Strategy-Game-Agents): repeated-choice experiments and baseline agents.

## What is here

- Allow-listed formula language: `rank`, `delta`, `mean`, and arithmetic.
- Point-in-time evaluation on stock-date panels.
- Promotion gate for OOS IC, turnover, and cost-adjusted return.
- Deterministic synthetic-data demo that rejects the candidate.
- Tests for parsing, future-field rejection, and promotion logic.

## Run

```bash
python -m pip install -e .
python -m ai_alpha_lab.demo
python -m unittest discover -s tests -v
```

## Evidence boundary

The first public record is intentionally conservative. An AutoAlpha-style study ran through the search and validation pipeline, but the frozen protocol produced zero final candidates. See [`evidence/validation-summary.md`](evidence/validation-summary.md) and [`research_state.json`](research_state.json).

## Layout

```text
src/ai_alpha_lab/  public research core
tests/             regression and safety checks
evidence/          short evidence records
research_state.json current claim ceiling and reopen condition
```

## Not included

- private data, employer code, credentials, or proprietary research assets
- tradable-performance claims
- automatic capital deployment

## Next track

The current formula space is closed. I would reopen it only with a pre-registered mechanism, independent data, a frozen baseline, and the same or stricter gates.
