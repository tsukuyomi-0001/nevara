from langchain_core.messages import BaseMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from typing import TypeGuard

### brain Tool
@tool
def router_tool(prompt: str):
    """
    [USEAGE]
    prompt: prompt in what you want to be done.
    
    [DESC]
    use this tool to do interactive tasks.
    
    Capability support:
    1) Web Search / Internet Lookup
    2) File System eg: creating, read, write, delete related to files or directory.
    3) Document Retrival Tool: able to read documents for "Tempory Retrival Files"
    """
    
brain_tools = [router_tool]

### utility
def isAIMessage(message: BaseMessage) -> TypeGuard[AIMessage]:
    return isinstance(message, AIMessage)

def makeToolMessage(content: str, tool_call_id: str) -> ToolMessage:
    return ToolMessage(content=content, tool_call_id=tool_call_id)

def tool_data_extract(message: AIMessage) -> tuple[str, str]:
    tool_call = message.tool_calls[-1]
    return tool_call['args']['prompt'], str(tool_call['id'])