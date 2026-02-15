from core.state import AgentState


def writer_agent(state: AgentState) -> AgentState:
    # get trace
    trace = state.get("trace") or []
    step_num = len(trace) + 1

    # read notes + sources
    notes = (state.get("notes") or "").strip()
    sources = state.get("sources") or []

    # if missing data
    if not notes or notes == "Not found in sources." or not sources:
        state["draft"] = "Not found in sources."

        # log fail
        trace.append({
            "step": step_num,
            "agent": "Writer",
            "action": "Write draft",
            "outcome": "NO_EVIDENCE"
        })

        state["trace"] = trace
        return state

    cited = []

    # build citations
    for s in sources:
        cited.append(f"[{s['id']}] {s['title']} ({s.get('locator','')})")

    # build draft
    draft = "Summary (grounded in sources):\n"
    draft += notes + "\n\n"
    draft += "Citations / Sources:\n"
    draft += "\n".join(cited)

    # save draft
    state["draft"] = draft

    # log success
    trace.append({
        "step": step_num,
        "agent": "Writer",
        "action": "Write draft",
        "outcome": "OK"
    })

    state["trace"] = trace
    return state