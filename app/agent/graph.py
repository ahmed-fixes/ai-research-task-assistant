from langgraph.graph import StateGraph, END

from app.agent.state import AgentState

from app.agent.nodes import (
    router_node,
    tool_selection_node,
    tool_execution_node,
    direct_answer_node,
    tool_answer_node,
    rag_node,
    error_node,
)

from app.storage.checkpoints import checkpointer


def route_after_router(
    state: AgentState,
) -> str:

    if state.get("error"):
        return "error"

    route = state.get("route")

    if route == "direct":
        return "direct"

    if route == "tool":
        return "tool"

    if route == "rag":
        return "rag"

    return "error"


def route_after_tool_execution(
    state: AgentState,
) -> str:

    if state.get("error"):
        return "error"

    return "tool_answer"


def build_graph():

    graph = StateGraph(AgentState)

    # Router
    graph.add_node(
        "router",
        router_node,
    )

    # Direct answer
    graph.add_node(
        "direct_answer",
        direct_answer_node,
    )

    # Tool flow
    graph.add_node(
        "tool_selection",
        tool_selection_node,
    )

    graph.add_node(
        "tool_execution",
        tool_execution_node,
    )

    graph.add_node(
        "tool_answer",
        tool_answer_node,
    )

    # RAG flow
    graph.add_node(
        "rag",
        rag_node,
    )

    # Error
    graph.add_node(
        "error",
        error_node,
    )

    # Start
    graph.set_entry_point(
        "router"
    )

    # Router decides where to go
    graph.add_conditional_edges(
        "router",
        route_after_router,
        {
            "direct": "direct_answer",
            "tool": "tool_selection",
            "rag": "rag",
            "error": "error",
        },
    )

    # Tool flow
    graph.add_edge(
        "tool_selection",
        "tool_execution",
    )

    graph.add_conditional_edges(
        "tool_execution",
        route_after_tool_execution,
        {
            "tool_answer": "tool_answer",
            "error": "error",
        },
    )

    # Direct answer finishes
    graph.add_edge(
        "direct_answer",
        END,
    )

    # Tool answer finishes
    graph.add_edge(
        "tool_answer",
        END,
    )

    # RAG answer finishes
    graph.add_edge(
        "rag",
        END,
    )

    # Error finishes
    graph.add_edge(
        "error",
        END,
    )

    return graph.compile(
        checkpointer=checkpointer
    )


agent_graph = build_graph()