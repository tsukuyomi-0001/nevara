from langchain_core.messages import AIMessageChunk
import asyncio

from nevara.modules.util import chunk_print, process_sentence
from nevara.agent import NevaraV1, GlobalState, memorySystem
from nevara.modules.tts import TTS_engine, text_queue

class Interface:
    def __init__(self) -> None:
        pass
    
    def grace_shutdown(self):
        memorySystem.session_end()
    
    def stream(self, userInput: str):
        for chunk in NevaraV1.stream(GlobalState(userInput=userInput), stream_mode='messages'):
            message, metadata = chunk
            print(metadata)
            chunk_print(message)
            
    async def astream(self, userInput: str):
        sentence = ''
        async for chunk in NevaraV1.astream(GlobalState(userInput=userInput), stream_mode='messages'):
            message, metadata = chunk
            if type(metadata) != dict: continue
            
            if metadata['langgraph_node'] == 'Brain' and type(message) == AIMessageChunk:
                sentence += str(message.content)
                sentence = await process_sentence(sentence)
            chunk_print(message)
        await text_queue.put(sentence)
        await text_queue.put(None)
        
    async def astream_audioSupport(self, userInput: str):
        text_generation_task = asyncio.create_task(self.astream(userInput))
        tts_task = asyncio.create_task(TTS_engine())
        await text_generation_task
        await tts_task