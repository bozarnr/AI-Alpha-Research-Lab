"""Deterministic, synthetic smoke run. It must not be interpreted as a backtest."""

from __future__ import annotations

import json

import numpy as np
import pandas as pd

from .research import PromotionGate, evaluate_candidate


def synthetic_panel(seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2024-01-02", periods=90)
    assets = [f"asset_{index:02d}" for index in range(24)]
    index = pd.MultiIndex.from_product([dates, assets], names=["date", "asset"])
    panel = index.to_frame(index=False)
    noise = rng.normal(0, 0.015, len(panel))
    panel["returns"] = noise
    panel["close"] = 100 * (1 + panel["returns"]).groupby(panel["asset"]).cumprod()
    panel["amount"] = rng.lognormal(mean=14, sigma=0.7, size=len(panel))
    panel["forward_return"] = panel.groupby("asset")["returns"].shift(-1)
    return panel.sort_values(["asset", "date"]).reset_index(drop=True)


def main() -> None:
    panel = synthetic_panel()
    result = evaluate_candidate(
        "rank(delta(amount, 3)) - rank(mean(returns, 5))",
        panel,
        split_date="2024-03-15",
        # A deliberately conservative gate prevents a noise-only smoke run
        # from being presented as an investable discovery.
        gate=PromotionGate(min_oos_rank_ic=0.05, max_turnover=0.60),
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
