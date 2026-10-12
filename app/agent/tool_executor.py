from typing import Any

from app.tools.calculator import calculator_tool
from app.tools.utility_tool import weather_tool


TOOLS = {
    "calculator": calculator_tool,
    "get_weather": weather_tool,
}


def execute_tool(
    tool_name: str,
    tool_input: dict[str, Any],
) -> Any:

    tool = TOOLS.get(tool_name)

    if tool is None:
        raise ValueError(
            f"Unknown tool: {tool_name}"
        )

    try:
        return tool.invoke(tool_input)

    except Exception as e:
        raise ValueError(
            f"Tool execution failed: {str(e)}"
        )