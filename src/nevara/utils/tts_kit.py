from langchain_core.messages import AIMessageChunk
import emoji
import re

from nevara.components.tts import text_queue

def text_sanitize(text: str):
    text = emoji.replace_emoji(text, replace='')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def split_text(text: str) -> tuple[list[str], str]:
    splits = [s.strip() for s in re.findall(r"[^.?]+[.?]?", text) if s.strip()]
    if len(splits) == 0: return splits[:-1], ''
    
    return splits[:-1], splits[-1]

def chunk_print(inChunk):
    if type(inChunk) == AIMessageChunk:
        print(inChunk.content, end='', flush=True)
        if inChunk.chunk_position == 'last': print()
        
async def process_sentence(text: str) -> str:
    text = text_sanitize(text)
    
    chunks, save_text = split_text(text)
    for chunk in chunks:
        await text_queue.put(chunk)
    return save_text