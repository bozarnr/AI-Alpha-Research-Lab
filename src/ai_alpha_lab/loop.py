from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class CandidateRecord:
    formula: str
    oos_rank_ic: float
    oos_net_return: float
    turnover: float
    promoted: bool
    reason: str

    @classmethod
    def from_result(cls, result: dict) -> "CandidateRecord":
        return cls(
            formula=str(result["formula"]),
            oos_rank_ic=float(result["oos_rank_ic"]),
            oos_net_return=float(result["oos_net_return"]),
            turnover=float(result["turnover"]),
            promoted=bool(result["promoted"]),
            reason=str(result["reason"]),
        )


@dataclass(frozen=True)
class ResearchLoopSummary:
    total_candidates: int
    promoted_candidates: int
    rejected_candidates: int
    best_oos_rank_ic: float | None
    best_oos_net_return: float | None
    rejection_reasons: dict[str, int]

    def to_dict(self) -> dict[str, object]:
        return {
            "total_candidates": self.total_candidates,
            "promoted_candidates": self.promoted_candidates,
            "rejected_candidates": self.rejected_candidates,
            "best_oos_rank_ic": self.best_oos_rank_ic,
            "best_oos_net_return": self.best_oos_net_return,
            "rejection_reasons": self.rejection_reasons,
        }


def summarize_loop(records: Iterable[CandidateRecord]) -> ResearchLoopSummary:
    items = list(records)
    reasons: dict[str, int] = {}
    for record in items:
        if not record.promoted:
            reasons[record.reason] = reasons.get(record.reason, 0) + 1
    return ResearchLoopSummary(
        total_candidates=len(items),
        promoted_candidates=sum(1 for record in items if record.promoted),
        rejected_candidates=sum(1 for record in items if not record.promoted),
        best_oos_rank_ic=max((record.oos_rank_ic for record in items), default=None),
        best_oos_net_return=max((record.oos_net_return for record in items), default=None),
        rejection_reasons=dict(sorted(reasons.items())),
    )


def rejection_gallery(records: Iterable[CandidateRecord], limit: int = 10) -> list[dict[str, object]]:
    if limit <= 0:
        raise ValueError("limit must be positive")
    rejected = [record for record in records if not record.promoted]
    ranked = sorted(rejected, key=lambda record: (record.oos_rank_ic, record.oos_net_return), reverse=True)
    return [
        {
            "formula": record.formula,
            "oos_rank_ic": record.oos_rank_ic,
            "oos_net_return": record.oos_net_return,
            "turnover": record.turnover,
            "reason": record.reason,
        }
        for record in ranked[:limit]
    ]
