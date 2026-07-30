"""A tiny point-in-time formula language with no dynamic code execution."""

from __future__ import annotations

import ast
from dataclasses import dataclass

import pandas as pd


class FormulaError(ValueError):
    """Raised when a candidate violates the public formula contract."""


@dataclass(frozen=True)
class FormulaContract:
    allowed_fields: frozenset[str]
    max_window: int = 60


def _require_panel(frame: pd.DataFrame) -> None:
    if not {"date", "asset"}.issubset(frame.columns):
        raise FormulaError("panel requires date and asset columns")
    if not frame.sort_values(["asset", "date"])[["asset", "date"]].equals(frame[["asset", "date"]]):
        raise FormulaError("panel must be sorted by asset and date")


def _cross_section_rank(series: pd.Series, frame: pd.DataFrame) -> pd.Series:
    return series.groupby(frame["date"], sort=False).rank(pct=True)


def _by_asset_rolling(series: pd.Series, frame: pd.DataFrame, window: int) -> pd.Series:
    return series.groupby(frame["asset"], sort=False).transform(
        lambda values: values.rolling(window=window, min_periods=window).mean()
    )


def _by_asset_delta(series: pd.Series, frame: pd.DataFrame, period: int) -> pd.Series:
    return series.groupby(frame["asset"], sort=False).transform(lambda values: values.diff(period))


def evaluate_formula(expression: str, frame: pd.DataFrame, contract: FormulaContract) -> pd.Series:
    """Evaluate an allow-listed formula using only contemporaneous or past values."""
    _require_panel(frame)
    tree = ast.parse(expression, mode="eval")

    def visit(node: ast.AST) -> pd.Series | int | float:
        if isinstance(node, ast.Name):
            if node.id not in contract.allowed_fields or node.id not in frame.columns:
                raise FormulaError(f"field is not allowed: {node.id}")
            if "future" in node.id.lower() or "label" in node.id.lower():
                raise FormulaError(f"future-looking field is forbidden: {node.id}")
            return frame[node.id].astype(float)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            return left / right.replace(0, float("nan")) if isinstance(right, pd.Series) else left / right
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -visit(node.operand)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            args = [visit(argument) for argument in node.args]
            if node.func.id == "rank" and len(args) == 1 and isinstance(args[0], pd.Series):
                return _cross_section_rank(args[0], frame)
            if node.func.id in {"delta", "mean"} and len(args) == 2 and isinstance(args[0], pd.Series):
                period = args[1]
                if not isinstance(period, int) or not 1 <= period <= contract.max_window:
                    raise FormulaError("window must be an integer within the contract")
                return _by_asset_delta(args[0], frame, period) if node.func.id == "delta" else _by_asset_rolling(args[0], frame, period)
        raise FormulaError(f"unsupported formula syntax: {ast.dump(node, include_attributes=False)}")

    result = visit(tree.body)
    if not isinstance(result, pd.Series):
        raise FormulaError("formula must evaluate to a series")
    return result.replace([float("inf"), float("-inf")], float("nan"))
