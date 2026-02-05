from __future__ import annotations

import ast
import operator as op
from typing import Any, Dict

from kruti.tools.base import Tool, ToolSpec


_ALLOWED = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.Mod: op.mod,
}


def _eval(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED:
        return _ALLOWED[type(node.op)](_eval(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED:
        return _ALLOWED[type(node.op)](_eval(node.left), _eval(node.right))
    raise ValueError("Unsupported expression")


class CalcTool(Tool):
    spec = ToolSpec(
        name="calc",
        description="Safely evaluate a basic arithmetic expression (no variables, no function calls).",
        args_schema={"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]},
    )

    def run(self, args: Dict[str, Any], timeout_seconds: int = 10) -> str:
        expr = str(args.get("expression", "")).strip()
        if not expr:
            return "error: empty expression"
        try:
            tree = ast.parse(expr, mode="eval")
            result = _eval(tree.body)
            # normalize integer-ish floats
            if abs(result - round(result)) < 1e-12:
                return str(int(round(result)))
            return str(result)
        except Exception as e:
            return f"error: {e}"
