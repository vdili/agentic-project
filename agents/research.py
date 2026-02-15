from core.state import AgentState
from core.retrieval import top_k_chunks


def research_agent(state: AgentState) -> AgentState:
    trace = state.get("trace") or []
    step_num = len(trace) + 1

    task = (state.get("task") or "").strip()
    chunks = state.get("chunks") or []

    # If no uploaded documents
    if not chunks:
        state["notes"] = ""
        state["sources"] = []

        trace.append({
            "step": step_num,
            "agent": "Research",
            "action": "Check documents",
            "outcome": "NO_DOCUMENTS"
        })

        state["trace"] = trace
        return state

    # Run TF-IDF retrieval
    results = top_k_chunks(task, chunks, k=3)

    # Fallback for generic summary-like queries
    if not results and chunks:
        fallback_keywords = ["summarize", "summary", "overview", "main idea"]

        if any(word in task.lower() for word in fallback_keywords):
            # Use first chunk as fallback evidence
            results = [(chunks[0], 0.0)]

    notes = []
    sources = []

    for chunk, score in results:
        notes.append(chunk["text"])

        sources.append({
            "id": chunk["doc_id"],
            "title": chunk["filename"],
            "locator": chunk["locator"],
            "snippet": chunk["text"][:200]
        })

    state["notes"] = "\n".join(notes)
    state["sources"] = sources

    trace.append({
        "step": step_num,
        "agent": "Research",
        "action": "Retrieve relevant chunks (TF-IDF + fallback)",
        "outcome": "OK" if sources else "NO_EVIDENCE"
    })

    state["trace"] = trace
    return state
