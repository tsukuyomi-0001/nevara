from langchain_core.messages import AIMessageChunk, HumanMessage
import asyncio

from nevara.components.tts import TTS_engine, text_queue
from nevara.schema import state as schema_state
from nevara.utils import tts_kit
from nevara import agent

class Interface:
    def __init__(self) -> None:
        pass
    
    def grace_shutdown(self):
        agent.converstation_memory.session_end()
    
    def stream(self, userInput: str):
        in_state = schema_state.GlobalState(user_input=HumanMessage(content=userInput))
        for chunk in agent.NevaraV1.stream(in_state, stream_mode='messages'):
            message, metadata = chunk
            print(metadata)
            tts_kit.chunk_print(message)
            
    async def astream(self, userInput: str):
        sentence = ''
        in_state = schema_state.GlobalState(user_input=HumanMessage(content=userInput))
        async for chunk in agent.NevaraV1.astream(in_state, stream_mode='messages'):
            message, metadata = chunk
            if type(metadata) != dict: continue
            
            if metadata['langgraph_node'] == 'Brain' and type(message) == AIMessageChunk:
                sentence += str(message.content)
                sentence = await tts_kit.process_sentence(sentence)
            tts_kit.chunk_print(message)
        await text_queue.put(sentence)
        await text_queue.put(None)
        
    async def astream_audioSupport(self, userInput: str):
        text_generation_task = asyncio.create_task(self.astream(userInput))
        tts_task = asyncio.create_task(TTS_engine())
        await text_generation_task
        await tts_task