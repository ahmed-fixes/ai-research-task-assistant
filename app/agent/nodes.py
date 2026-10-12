from app.agent.routing import (
    route_request,
    select_tool,
)

from app.agent.tool_executor import execute_tool

from app.agent.state import AgentState

from app.services.llm_service import ask_llm

from app.services.embedding_service import generate_embedding
from app.services.document_service import vector_store
from app.services.rag_service import (
    build_context,
    build_rag_prompt,
    build_sources,
)

from app.config import MAX_AGENT_STEPS


def router_node(
    state: AgentState,
) -> dict:

    if state.get("step_count", 0) >= MAX_AGENT_STEPS:

        return {
            "error": "Maximum agent steps exceeded.",
            "final_answer": (
                "I could not complete the request "
                "within the allowed number of steps."
            ),
        }

    result = route_request(
        state["user_input"]
    )

    return {
        "route": result.route,
        "step_count": (
            state.get("step_count", 0) + 1
        ),
        "actions": (
            state.get("actions", [])
            + [f"route selected: {result.route}"]
        ),
    }


def tool_selection_node(
    state: AgentState,
) -> dict:

    result = select_tool(
        state["user_input"]
    )

    return {
        "tool_name": result.tool_name,
        "tool_input": result.tool_input,
        "step_count": (
            state.get("step_count", 0) + 1
        ),
        "actions": (
            state.get("actions", [])
            + [f"tool selected: {result.tool_name}"]
        ),
    }


def tool_execution_node(
    state: AgentState,
) -> dict:

    try:

        result = execute_tool(
            state["tool_name"],
            state["tool_input"],
        )

        return {
            "tool_output": result,
            "step_count": (
                state.get("step_count", 0) + 1
            ),
            "actions": (
                state.get("actions", [])
                + [
                    f"tool executed: "
                    f"{state['tool_name']}"
                ]
            ),
        }

    except Exception as e:

        return {
            "error": str(e),
            "step_count": (
                state.get("step_count", 0) + 1
            ),
            "actions": (
                state.get("actions", [])
                + [
                    f"tool failed: "
                    f"{state['tool_name']}"
                ]
            ),
        }



def direct_answer_node(
    state: AgentState,
) -> dict:

    messages = state.get("messages", [])

    conversation = ""

    for message in messages:
        conversation += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )

    prompt = f"""
Answer the user's request using the conversation context below.

Conversation history:
{conversation}

Current user request:
{state["user_input"]}

Use the previous conversation to understand references
such as "it", "this", "that", "they", etc.

Give a clear and concise answer.
"""

    try:

        answer = ask_llm(prompt)

        return {
            "final_answer": answer,
            "step_count": (
                state.get("step_count", 0) + 1
            ),
            "actions": (
                state.get("actions", [])
                + ["generated direct answer"]
            ),
        }

    except Exception as e:

        return {
            "error": str(e),
            "step_count": (
                state.get("step_count", 0) + 1
            ),
            "actions": (
                state.get("actions", [])
                + ["direct answer generation failed"]
            ),
        }



def tool_answer_node(
    state: AgentState,
) -> dict:

    prompt = f"""
Answer the user's request using the tool result.

User request:
{state["user_input"]}

Tool used:
{state["tool_name"]}

Tool result:
{state["tool_output"]}

Give only the final answer.
Do not mention internal reasoning.
"""

    try:

        answer = ask_llm(prompt)

        return {
            "final_answer": answer,
            "step_count": (
                state.get("step_count", 0) + 1
            ),
            "actions": (
                state.get("actions", [])
                + [
                    "generated final answer "
                    "from tool result"
                ]
            ),
        }

    except Exception as e:

        return {
            "error": str(e),
            "step_count": (
                state.get("step_count", 0) + 1
            ),
            "actions": (
                state.get("actions", [])
                + ["tool answer generation failed"]
            ),
        }


def rag_node(
    state: AgentState,
) -> dict:

    try:

        question = state["user_input"]

        # Generate embedding for the user's question
        question_vector = generate_embedding(
            question
        )

        # Search the FAISS vector store
        distances, results = vector_store.search(
            question_vector,
            k=3,
        )

        # Build context from retrieved chunks
        context = build_context(
            results
        )

        # Build the RAG prompt
        prompt = build_rag_prompt(
            question,
            context,
        )

        # Generate final answer using the existing LLM service
        answer = ask_llm(
            prompt
        )

        # Build source information
        sources = build_sources(
            results
        )

        return {
            "final_answer": answer,
            "retrieved_context": sources,
            "step_count": (
                state.get("step_count", 0) + 1
            ),
            "actions": (
                state.get("actions", [])
                + [
                    "retrieved relevant documents",
                    "generated RAG answer",
                ]
            ),
        }

    except Exception as e:

        return {
            "error": str(e),
            "step_count": (
                state.get("step_count", 0) + 1
            ),
            "actions": (
                state.get("actions", [])
                + ["RAG execution failed"]
            ),
        }


def error_node(
    state: AgentState,
) -> dict:

    error = state.get(
        "error",
        "An unexpected error occurred.",
    )

    return {
        "final_answer": (
            "Sorry, I could not complete "
            f"your request. Reason: {error}"
        ),
        "actions": (
            state.get("actions", [])
            + ["returned error response"]
        ),
    }