from langgraph.graph.state import StateGraph, Command
from typing import cast

from nevara.schema import (
    state as state_schema, 
    struct as struct_schema
)
from nevara import memory, prompts, manager
from nevara.utils import agent_kit
from nevara.agent import executor
from nevara.agent import LM

promptManager = prompts.PromptManager([manager.fs_manager, manager.doc_manager])
routerModel = LM.StructureModel.with_structured_output(struct_schema)
brain_model = LM.ChatModel.bind_tools(agent_kit.brain_tools)
converstation_memory = memory.ConverstationMemory()
executors_table = executor.get_executors_index()

def contextBuildUp(state: state_schema.GlobalState):
    converstation_memory.maintainMemory()
    
    history_prompt = converstation_memory.build_history_prompt(str(state.user_input.content))
    systemMessage = promptManager.build_brain_system_prompt(history_prompt)
    
    ## making whole context
    prompt = [
        systemMessage,
        *converstation_memory.getMessages(),
        state.user_input,
        *state.brain_scratchpad
    ]
    return { 'prompt': prompt } 

def brain(state: state_schema.GlobalState):
    response = brain_model.invoke(state.prompt)
    
    if response.tool_calls:
        return Command(goto='Router', update={'brain_scratchpad': [response]})
    
    state.brain_scratchpad.clear()
    converstation_memory.commitMessage([state.user_input, response])
    
def router(state: state_schema.GlobalState):
    ai_message = state.brain_scratchpad[-1]
    if not agent_kit.isAIMessage(ai_message): return
    task, tool_id = agent_kit.tool_data_extract(ai_message)
    
    inPrompt = promptManager.build_router_system_prompt(task)
    response = routerModel.invoke([inPrompt])
    response = cast(struct_schema.RouterStruct, response)
    
    result = "Tool Inavailable OR There was problem in tool. Simply Report back to user."
    if response.route != 'DONE':
        try: result = executors_table[response.route].invoke(response.prompt)
        except Exception: raise Exception(f"Problem Occured During Routing...\nExecutor Route: {response.route}")

    return Command(
        goto='Brain', 
        update={'brain_scratchpad': [agent_kit.makeToolMessage(result, tool_id)]}
    )
    
graph = StateGraph(state_schema.GlobalState)
graph.add_node('contextBuildUp', contextBuildUp)
graph.add_node('Brain', brain)
graph.add_node('Router', router)

graph.set_entry_point('contextBuildUp')
graph.add_edge('contextBuildUp', 'Brain')

NevaraV1 = graph.compile()
