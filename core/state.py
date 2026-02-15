from typing import TypedDict, List


# text chunk
class Chunk(TypedDict):
    doc_id: str
    filename: str
    locator: str
    text: str


# source info
class Source(TypedDict, total=False):
    id: str
    title: str
    locator: str
    snippet: str


# trace row
class TraceRow(TypedDict):
    step: int
    agent: str
    action: str
    outcome: str


# main state
class AgentState(TypedDict, total=False):
    task: str
    chunks: List[Chunk]
    plan: List[str]
    notes: str
    sources: List[Source]
    draft: str
    final_answer: str
    trace: List[TraceRow]