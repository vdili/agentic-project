from core.state import AgentState


def planner_agent(state: AgentState) -> AgentState:
    # Get existing trace or initialize it
    trace = state.get("trace") or []
    step_num = len(trace) + 1

    # Read and clean user task
    task = (state.get("task") or "").strip()

    # Define high-level execution plan
    plan = [
        "Understand the task",
        "Retrieve relevant evidence from uploaded documents",
        "Write a grounded answer with citations",
        "Verify the answer is supported by sources"
    ]

    # Store plan in shared state
    state["plan"] = plan

    # Log planner step
    trace.append({
        "step": step_num,
        "agent": "Planner",
        "action": "Create plan",
        "outcome": "OK"
    })

    state["trace"] = trace
    return state
