import re
import sympy as sp
from decimal import Decimal
from typing import Dict, Callable

class Tool:
    def __init__(self, name: str, schema: dict, func: Callable[[dict], dict]):
        self.name = name
        self.schema = schema
        self.call = func

def _safe_calc(args: dict) -> dict:
    expr = args["expression"]
    if re.search(r"[^\d+\-*/().^ ]", expr):
        return {"error": "Illegal characters in expression"}
    try:
        val = Decimal(str(sp.sympify(expr).evalf()))
        return {"result": str(val)}
    except Exception as e:
        return {"error": str(e)}

def _reverse_string(args: dict) -> dict:
    return {"result": args["text"][::-1]}

def _word_count(args: dict) -> dict:
    return {"result": len(args["text"].split())}

TOOLS: Dict[str, Tool] = {
    "calculator": Tool(
        "calculator",
        {
            "type": "object",
            "properties": {"expression": {"type": "string"}},
            "required": ["expression"],
        },
        _safe_calc,
    ),
    "reverse_string": Tool(
        "reverse_string",
        {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
        _reverse_string,
    ),
    "word_count": Tool(
        "word_count",
        {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
        _word_count,
    ),
}
