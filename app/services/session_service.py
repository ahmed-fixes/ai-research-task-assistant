from typing import Any


_sessions: dict[str, dict[str, Any]] = {}


def create_session(session_id: str) -> dict[str, Any]:

    if session_id not in _sessions:
        _sessions[session_id] = {
            "session_id": session_id,
            "messages": [],
            "step_count": 0,
            "route": "",
            "actions": [],
        }

    return _sessions[session_id]


def get_session(
    session_id: str,
) -> dict[str, Any] | None:

    return _sessions.get(session_id)


def update_session(
    session_id: str,
    state: dict[str, Any],
) -> dict[str, Any]:

    session = create_session(session_id)

    for key in [
        "messages",
        "step_count",
        "route",
        "actions",
    ]:
        if key in state:
            session[key] = state[key]

    return session


def delete_session(
    session_id: str,
) -> bool:

    if session_id not in _sessions:
        return False

    del _sessions[session_id]

    return True