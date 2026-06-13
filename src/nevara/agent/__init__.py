from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph.state import StateGraph

from nevara.memory import ConverstationMemory
from nevara.modules.util import get_time_date
from nevara.schema.state import GlobalState
from nevara.prompts import load_prompt
from nevara.agent.LM import BrainModel

memorySystem = ConverstationMemory()

def brain(state: GlobalState):
    memorySystem.maintainMemory()
    userInput = HumanMessage(content=state.userInput)
    
    history_prompt = memorySystem.build_history_prompt(state.userInput)
    
    date, time = get_time_date()
    system_content = load_prompt('brain/system', time=time, date=date) + history_prompt; print(system_content)
    
    prompt: list = [SystemMessage(content=system_content)]
    prompt.extend(memorySystem.getMessages())
    prompt.append(userInput)
    
    response = BrainModel.invoke(prompt)
    
    memorySystem.commitMessage([userInput, response])

graph = StateGraph(GlobalState)
graph.add_node('Brain', brain)
graph.set_entry_point('Brain')

NevaraV1 = graph.compile()
