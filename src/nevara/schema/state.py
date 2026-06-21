from langchain_core.messages import BaseMessage, ToolMessage, AIMessage, HumanMessage
from typing import Annotated, Optional
from pydantic import BaseModel
from operator import add

class GlobalState(BaseModel):
    user_input: HumanMessage
    prompt: list[BaseMessage] = []
    brain_scratchpad: Annotated[list[BaseMessage], add] = []
    
class ExecutorState(BaseModel):
    input: str
    messages: Annotated[list[BaseMessage], add] = []
    result: ToolMessage = ToolMessage(content='EMPTY', tool_call_id='')