from typing import Any

from pydantic import BaseModel, Field

from app.services.llm_service import ask_llm


class RouteDecision(BaseModel):

    route: str = Field(
        description=(
            "The route to use: direct, rag, or tool."
        )
    )


class ToolDecision(BaseModel):

    tool_name: str

    tool_input: dict[str, Any]


ALLOWED_ROUTES = {
    "direct",
    "rag",
    "tool",
}


ALLOWED_TOOLS = {
    "calculator",
    "get_weather",
}


def route_request(
    user_input: str,
) -> RouteDecision:

    prompt = f"""
You are a request router for an AI research
and task assistant.

Choose exactly one route:

direct:
Use when the request can be answered directly
by the LLM.

rag:
Use when the request requires information from
the user's documents or knowledge base.

tool:
Use when the request requires a calculator
or weather tool.

User request:
{user_input}

Return only valid JSON:

{{
    "route": "direct"
}}
"""

    result = ask_llm(prompt)

    decision = RouteDecision.model_validate_json(
        result
    )

    if decision.route not in ALLOWED_ROUTES:

        raise ValueError(
            f"Invalid route returned by LLM: "
            f"{decision.route}"
        )

    return decision


def select_tool(
    user_input: str,
) -> ToolDecision:

    prompt = f"""
You are a tool selector.

Available tools:

calculator:
Performs mathematical calculations.

Input:
{{
    "expression": "25 * 8"
}}

get_weather:
Gets current weather for a city.

Input:
{{
    "city": "Lahore"
}}

Choose exactly one tool.

User request:
{user_input}

Return only valid JSON.

Calculator example:
{{
    "tool_name": "calculator",
    "tool_input": {{
        "expression": "25 * 8"
    }}
}}

Weather example:
{{
    "tool_name": "get_weather",
    "tool_input": {{
        "city": "Lahore"
    }}
}}
"""

    result = ask_llm(prompt)

    decision = ToolDecision.model_validate_json(
        result
    )

    if decision.tool_name not in ALLOWED_TOOLS:

        raise ValueError(
            f"Invalid tool returned by LLM: "
            f"{decision.tool_name}"
        )

    if not decision.tool_input:

        raise ValueError(
            "Tool input cannot be empty."
        )

    return decision