from typing import TypedDict , List,Optional

class AgentState(TypedDict):
    task: str
    generated_code:Optional[str]
    file_path: Optional[str]
    language: str 
    iterations: int
    error:Optional[str]
    success: bool