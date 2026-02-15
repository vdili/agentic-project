from langgraph.graph import StateGraph, END
from core.state import AgentState

from agents.planner import planner_agent
from agents.research import research_agent
from agents.writer import writer_agent
from agents.verifier import verifier_agent


def build_graph():
    g = StateGraph(AgentState)

    g.add_node("planner", planner_agent)
    g.add_node("research", research_agent)
    g.add_node("writer", writer_agent)
    g.add_node("verifier", verifier_agent)

    g.set_entry_point("planner")

    g.add_edge("planner", "research")
    g.add_edge("research", "writer")
    g.add_edge("writer", "verifier")
    g.add_edge("verifier", END)

    return g.compile()
