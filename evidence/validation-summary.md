# Validation Summary: Initial Formula Search Record

This public record summarizes a completed AutoAlpha-style research loop without
publishing private data, employer code, credentials, or raw experiment outputs.

## What was implemented

- Allow-listed AST expression evaluation rather than `eval`.
- Formula canonicalization, hashes, depth tracking, and search lineage.
- Stratified search, diversity filtering, warm starts, and ablations.
- Next-open execution timing, transaction costs, risk controls, turnover, and
  frozen independent-test promotion gates.

## What the evidence supports

The pipeline can generate, evaluate, audit, and reject formula candidates. It
does **not** support a claim that the tested price/volume/return formula space
contains an online-ready alpha pool.

## Strict result

Across frozen transfers and a multi-source retest, the final candidate count
was **0**. Discovery-stage signals concentrated in short-horizon amount and
return transformations; they did not retain a positive cost-aware portfolio
result after transfer.

## Reopening rule

Do not search the same closed formula space harder. Restart only with a
pre-registered new mechanism or field, independent data, and a frozen protocol.
