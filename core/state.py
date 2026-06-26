from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    idea: str
    refined_idea: str
    prd_path: str
    issues: list[str]
    current_issue: str
    code_status: str
    messages: Annotated[list, add_messages]
