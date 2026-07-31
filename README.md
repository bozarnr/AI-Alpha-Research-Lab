# AI Alpha Research Lab

An auditable sandbox for formula-based alpha research. The project is designed
to make a negative result useful: a candidate is promoted only when it survives
time-safe evaluation, out-of-sample checks, and explicit trading frictions.

中文简介：这是一个可审计的公式因子研究沙盒。它不把漂亮的样本内指标
当成成果；候选公式必须通过时点安全、样本外、换手与成本门槛，才会被晋级。

## Public Research Stack

This repository is one part of a public AI-quant portfolio:

- [AI Alpha Research Lab](https://github.com/bozarnr/eee): formula-alpha research with strict promotion gates.
- [Paper Alpha Replications](https://github.com/bozarnr/paper-library): evidence-first paper replication ledger.
- [Quant Research Toolkit](https://github.com/bozarnr/experiment): reusable time-safe factor diagnostics.
- [Strategy Game Agents](https://github.com/bozarnr/behavioral-finance-experiment): behavioral experiment tooling plus strategy-agent simulation.

## What is included

- A small allow-listed expression language (`rank`, `delta`, `mean`, arithmetic).
- Point-in-time evaluation on a stock-date panel.
- A strict promotion gate for OOS IC, turnover, and costs.
- A deterministic synthetic-data demo that intentionally promotes no factor.
- Regression tests for parsing, future-field rejection, and the rejection gate.

## Quick start

```bash
python -m pip install -e .
python -m ai_alpha_lab.demo
python -m unittest discover -s tests -v
```

The demo is an engineering smoke test, not a backtest or investment result.

## Evidence boundary

The initial research record is deliberately conservative. A prior multi-source
AutoAlpha-style study implemented the search and validation pipeline, but under
the frozen executable protocol its final candidate count was zero. See
[`evidence/validation-summary.md`](evidence/validation-summary.md) and
[`research_state.json`](research_state.json).

## Repository layout

```text
src/ai_alpha_lab/  public, dependency-light research core
tests/             regression and safety checks
evidence/          compact, human-readable evidence records
research_state.json current claim ceiling and next reopening condition
```

## Non-goals

- No private data, employer code, credentials, or proprietary research assets.
- No claim that a high IC, this demo, or a successful run is tradable.
- No automatic capital deployment.

## Next research track

The formula space used in the first record is closed. Reopen only with a
pre-registered economic mechanism, genuinely independent data, a frozen
baseline, and the same or stricter promotion gates.
