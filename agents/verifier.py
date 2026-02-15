from core.state import AgentState


def verifier_agent(state: AgentState) -> AgentState:
    # get trace info
    trace = state.get("trace") or []
    step_num = len(trace) + 1

    # read draft + sources
    draft = (state.get("draft") or "").strip()
    sources = state.get("sources") or []

    # check if answer exists
    if not draft or draft == "Not found in sources." or not sources:
        state["final_answer"] = "Not found in sources."

        # log fail step
        trace.append({
            "step": step_num,
            "agent": "Verifier",
            "action": "Check answer + sources",
            "outcome": "NO_EVIDENCE"
        })

        state["trace"] = trace
        return state

    # save final answer
    state["final_answer"] = draft

    # log success
    trace.append({
        "step": step_num,
        "agent": "Verifier",
        "action": "Check answer + sources",
        "outcome": "OK"
    })

    state["trace"] = trace
    return state