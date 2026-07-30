"""Strict candidate evaluation that separates diagnostics from promotion."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import pandas as pd

from .expressions import FormulaContract, evaluate_formula


@dataclass(frozen=True)
class PromotionGate:
    min_oos_rank_ic: float = 0.02
    min_oos_net_return: float = 0.0
    max_turnover: float = 0.60
    transaction_cost_bps: float = 30.0


def _daily_rank_ic(panel: pd.DataFrame, signal: pd.Series) -> pd.Series:
    data = panel.assign(signal=signal).dropna(subset=["signal", "forward_return"])
    return data.groupby("date", sort=False).apply(
        lambda group: group["signal"].rank().corr(group["forward_return"].rank()), include_groups=False
    )


def _portfolio_diagnostics(panel: pd.DataFrame, signal: pd.Series, cost_bps: float) -> pd.DataFrame:
    """Calculate a simple top-quintile diagnostic with explicit turnover costs."""
    ranked = panel.assign(signal=signal).groupby("date", sort=False)["signal"].rank(pct=True)
    positions = (ranked >= 0.8).astype(float)
    shifts = positions.groupby(panel["asset"], sort=False).shift(1).fillna(0.0)
    daily_turnover = (positions - shifts).abs().groupby(panel["date"], sort=False).mean()
    returns = panel.assign(position=positions).groupby("date", sort=False).apply(
        lambda group: group.loc[group["position"] > 0, "forward_return"].mean(),
        include_groups=False,
    )
    diagnostics = pd.DataFrame({"turnover": daily_turnover, "gross_return": returns})
    diagnostics["net_return"] = diagnostics["gross_return"] - diagnostics["turnover"] * cost_bps / 10_000
    return diagnostics


def evaluate_candidate(expression: str, panel: pd.DataFrame, split_date: str, gate: PromotionGate) -> dict:
    """Return diagnostics and promotion status; never optimize against test results."""
    contract = FormulaContract(frozenset({"close", "amount", "returns"}))
    signal = evaluate_formula(expression, panel, contract)
    rank_ic = _daily_rank_ic(panel, signal)
    oos = rank_ic.loc[rank_ic.index >= pd.Timestamp(split_date)]
    portfolio = _portfolio_diagnostics(panel, signal, gate.transaction_cost_bps)
    oos_portfolio = portfolio.loc[portfolio.index >= pd.Timestamp(split_date)]
    mean_oos_ic = float(oos.mean()) if not oos.empty else float("nan")
    turnover = float(oos_portfolio["turnover"].mean())
    gross_return = float(oos_portfolio["gross_return"].mean())
    net_return = float(oos_portfolio["net_return"].mean())
    promoted = bool(
        mean_oos_ic >= gate.min_oos_rank_ic
        and turnover <= gate.max_turnover
        and net_return >= gate.min_oos_net_return
    )
    return {
        "formula": expression,
        "oos_rank_ic": round(mean_oos_ic, 6),
        "oos_gross_return": round(gross_return, 6),
        "oos_net_return": round(net_return, 6),
        "turnover": round(turnover, 6),
        "transaction_cost_bps": gate.transaction_cost_bps,
        "promoted": promoted,
        "reason": "passed frozen promotion gate" if promoted else "rejected by frozen OOS IC, turnover, or net-return gate",
        "gate": asdict(gate),
    }
