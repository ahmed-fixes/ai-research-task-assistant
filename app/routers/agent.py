from fastapi import APIRouter, HTTPException
from uuid import uuid4

from app.schemas import (
    AgentRunRequest,
    AgentChatRequest,
    AgentResponse,
    SessionResponse,
)

from app.agent.graph import agent_graph

from app.services.session_service import (
    create_session,
    get_session,
    update_session,
    delete_session,
)


router = APIRouter()


def run_agent(
    session_id: str,
    message: str,
) -> AgentResponse:

    session = create_session(session_id)

    messages = session.get("messages", [])

    messages.append({
        "role": "user",
        "content": message,
    })

    initial_state = {
        "session_id": session_id,
        "user_input": message,
        "messages": messages,
        "step_count": 0,
        "actions": [],
        "retrieved_context": [],
    }

    config = {
        "configurable": {
            "thread_id": session_id
        }
    }

    try:

        result = agent_graph.invoke(
            initial_state,
            config=config,
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Agent execution failed: {str(e)}",
        )

    answer = result.get(
        "final_answer",
        "I could not generate an answer.",
    )

    updated_messages = result.get(
        "messages",
        messages,
    )

    updated_messages.append({
        "role": "assistant",
        "content": answer,
    })

    result["messages"] = updated_messages

    update_session(
        session_id,
        result,
    )

    return AgentResponse(
        answer=answer,
        actions=result.get("actions", []),
        sources=result.get(
            "retrieved_context",
            []
        ),
        session_id=session_id,
        step_count=result.get(
            "step_count",
            0
        ),
        error=result.get("error"),
    )


@router.post(
    "/agent/run",
    response_model=AgentResponse,
)
def run_agent_endpoint(
    request: AgentRunRequest,
):

    session_id = str(uuid4())

    return run_agent(
        session_id=session_id,
        message=request.message,
    )


@router.post(
    "/agent/chat",
    response_model=AgentResponse,
)
def chat_endpoint(
    request: AgentChatRequest,
):

    session = get_session(
        request.session_id
    )

    if session is None:

        raise HTTPException(
            status_code=404,
            detail="Session not found.",
        )

    return run_agent(
        session_id=request.session_id,
        message=request.message,
    )


@router.get(
    "/sessions/{session_id}",
    response_model=SessionResponse,
)
def get_session_endpoint(
    session_id: str,
):

    session = get_session(session_id)

    if session is None:

        raise HTTPException(
            status_code=404,
            detail="Session not found.",
        )

    return SessionResponse(
        session_id=session["session_id"],
        messages=session.get(
            "messages",
            []
        ),
        step_count=session.get(
            "step_count",
            0
        ),
        route=session.get(
            "route",
            ""
        ),
        actions=session.get(
            "actions",
            []
        ),
    )


@router.delete(
    "/sessions/{session_id}"
)
def delete_session_endpoint(
    session_id: str,
):

    deleted = delete_session(
        session_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Session not found.",
        )

    return {
        "message": "Session deleted successfully.",
        "session_id": session_id,
    }