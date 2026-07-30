"""Public, auditable building blocks for formula-alpha research."""

from .expressions import FormulaError, evaluate_formula
from .research import PromotionGate, evaluate_candidate

__all__ = ["FormulaError", "PromotionGate", "evaluate_candidate", "evaluate_formula"]
