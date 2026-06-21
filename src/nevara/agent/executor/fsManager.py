from langchain_core.runnables import RunnableLambda
from langchain_core.messages import SystemMessage
from langchain_core.tools import StructuredTool
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph
from nevara.agent import LM

from nevara.schema import state as schema_state
from nevara import manager

fsManager = manager.FSManager()

#### TOOLS ####
read_file = StructuredTool.from_function(
    func=fsManager.read_file,
)

write_file = StructuredTool.from_function(
    func=fsManager.write_file,
)

create_file = StructuredTool.from_function(
    func=fsManager.create_file,
)

delete_file = StructuredTool.from_function(
    func=fsManager.delete_file,
)

create_directory = StructuredTool.from_function(
    func=fsManager.create_directory,
)

delete_directory = StructuredTool.from_function(
    func=fsManager.delete_directory,
)

change_directory = StructuredTool.from_function(
    func=fsManager.change_directory,
)

list_directory = StructuredTool.from_function(
    func=fsManager.list_directory,
)

tools = [
    read_file, 
    write_file,
    create_file,
    delete_file,
    create_directory,
    delete_directory,
    change_directory,
    list_directory
]

### executor ####
toolNode = ToolNode(tools, messages_key='messages')
worker = LM.ChatModel.bind_tools(tools)

def Worker(state: schema_state.ExecutorState):
    systemPrompt = SystemMessage(content=f"Use your tools to solve given prompt: {state.input}")
    response = worker.invoke([systemPrompt])
    return { 'messages': [response] }

def END_NODE(state: schema_state.ExecutorState):
    return { 'result': state.messages[-1] }


graph = StateGraph(schema_state.ExecutorState)
graph.add_node('Worker', Worker)
graph.add_node('ToolNode', toolNode)
graph.add_node('END_NODE', END_NODE)

graph.set_entry_point('Worker')
graph.add_edge('Worker', 'ToolNode')
graph.add_edge('ToolNode', 'END_NODE')

def task_creation(input_: str):
    return schema_state.ExecutorState(input=input_)

def extract_result(state: dict):
    state_ = schema_state.ExecutorState(**state)
    return str(state_.result.content)

task_runnable = RunnableLambda(task_creation)
extract_runnable = RunnableLambda(extract_result)

executor_agent = task_runnable | graph.compile() | extract_runnable