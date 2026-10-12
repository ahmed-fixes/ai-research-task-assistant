import ast
import math
import operator

from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool


class CalculatorInput(BaseModel):
    expression: str = Field(
        min_length=1,
        description="Mathematical expression to calculate."
    )


BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log10,
    "ln": math.log,
    "abs": abs,
    "floor": math.floor,
    "ceil": math.ceil,
    "factorial": math.factorial,
    "exp": math.exp,
}

CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}


def _evaluate(node):

    if isinstance(node, ast.Constant):

        if (
            isinstance(node.value, (int, float))
            and not isinstance(node.value, bool)
        ):
            return node.value

        raise ValueError("Only numeric values are allowed.")

    if isinstance(node, ast.BinOp):

        operator_function = BINARY_OPERATORS.get(type(node.op))

        if operator_function is None:
            raise ValueError("Unsupported mathematical operator.")

        left = _evaluate(node.left)
        right = _evaluate(node.right)

        return operator_function(left, right)

    if isinstance(node, ast.UnaryOp):

        operator_function = UNARY_OPERATORS.get(type(node.op))

        if operator_function is None:
            raise ValueError("Unsupported unary operator.")

        value = _evaluate(node.operand)

        return operator_function(value)

    if isinstance(node, ast.Name):

        if node.id in CONSTANTS:
            return CONSTANTS[node.id]

        raise ValueError(f"Unknown constant: {node.id}")

    if isinstance(node, ast.Call):

        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid function.")

        function = FUNCTIONS.get(node.func.id)

        if function is None:
            raise ValueError(
                f"Unsupported function: {node.func.id}"
            )

        if node.keywords:
            raise ValueError(
                "Keyword arguments are not allowed."
            )

        arguments = [
            _evaluate(argument)
            for argument in node.args
        ]

        return function(*arguments)

    raise ValueError("Unsupported expression.")


def calculate(expression: str) -> float:

    try:
        tree = ast.parse(
            expression,
            mode="eval"
        )

        result = _evaluate(tree.body)

        if not math.isfinite(result):
            raise ValueError(
                "Result is not a finite number."
            )

        return result

    except ZeroDivisionError:
        raise ValueError(
            "Cannot divide by zero."
        )

    except ValueError as e:
        raise ValueError(str(e))

    except Exception:
        raise ValueError(
            "Invalid mathematical expression."
        )
    
calculator_tool = StructuredTool.from_function(
    func=calculate,
    name="calculator",
    description=(
        "Perform mathematical calculations. "
        "Use this tool for arithmetic and mathematical "
        "expressions such as addition, subtraction, "
        "multiplication, division, powers, square roots, "
        "logarithms, trigonometry, and factorials. "
        "The input must contain an expression field."
    ),
    args_schema=CalculatorInput,
)