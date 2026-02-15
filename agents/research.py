from core.state import AgentState
from core.retrieval import top_k_chunks


def research_agent(state: AgentState) -> AgentState:
    # get trace
    trace = state.get("trace") or []
    step_num = len(trace) + 1

    # read input
    task = (state.get("task") or "").strip()
    chunks = state.get("chunks") or []

    # find top matches
    top = top_k_chunks(task, chunks, k=3)

    # if nothing found
    if not top:
        state["notes"] = "Not found in sources."
        state["sources"] = []
        trace.append({
            "step": step_num,
            "agent": "Research",
            "action": "Retrieve chunks",
            "outcome": "NO_EVIDENCE"
        })
        state["trace"] = trace
        return state

    notes_lines = []
    sources = []

    # build notes + sources
    for i, (c, score) in enumerate(top, start=1):
        snippet = (c.get("text") or "").strip()

        # shorten text
        snippet = snippet[:300] + ("..." if len(snippet) > 300 else "")

        # save note line
        notes_lines.append(
            f"[{c['doc_id']}] {c['filename']} ({c['locator']}): {snippet}"
        )

        # save source data
        sources.append({
            "id": c["doc_id"],
            "title": c["filename"],
            "locator": c["locator"],
            "snippet": snippet
        })

    # update state
    state["notes"] = "\n".join(notes_lines)
    state["sources"] = sources

    # add trace step
    trace.append({
        "step": step_num,
        "agent": "Research",
        "action": "Retrieve chunks",
        "outcome": "OK"
    })

    state["trace"] = trace
    return state