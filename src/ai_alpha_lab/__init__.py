"""Public, auditable building blocks for formula-alpha research."""

from .expressions import FormulaError, evaluate_formula
from .loop import CandidateRecord, ResearchLoopSummary, rejection_gallery, summarize_loop
from .research import PromotionGate, evaluate_candidate

__all__ = [
    "CandidateRecord",
    "FormulaError",
    "PromotionGate",
    "ResearchLoopSummary",
    "evaluate_candidate",
    "evaluate_formula",
    "rejection_gallery",
    "summarize_loop",
]
