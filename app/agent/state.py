from typing import Any

from typing_extensions import TypedDict


class AgentState(TypedDict, total=False):

    session_id: str

    user_input: str

    messages: list[dict[str, str]]

    route: str

    retrieved_context: list[dict[str, Any]]

    tool_name: str

    tool_input: dict[str, Any]

    tool_output: Any

    step_count: int

    final_answer: str

    actions: list[str]

    error: str