from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, AIMessageChunk
from datetime import datetime
from pathlib import Path
import emoji
import json
import os
import re

from nevara.schema.types import messageList
from nevara.modules.tts import text_queue
from nevara.agent.LM import BrainModel
from nevara.prompts import load_prompt
import data

def messages_token_count(msg: list):
    return BrainModel.get_num_tokens_from_messages(msg)

def split_messages(message: list, max_token: int) -> tuple[messageList, messageList]:
    total_tokens = 0
    for idx, _ in enumerate(message):
        neg_idx = idx+1
        total_tokens += messages_token_count([message[-neg_idx]])
        if total_tokens > max_token: return (message[:-neg_idx], message[-neg_idx:])
        
    return ([], message)

def summarizer(messages: messageList):
    msg_string = []
    for msg in messages:
        if type(msg) == AIMessage: msg_string.append(f"Nevara: {msg.content}")
        elif type(msg) == HumanMessage: msg_string.append(f"BlankStare: {msg.content}")
        
    msg_string = "\n".join(msg_string)
    
    sysPrompt = load_prompt("system/summary", msg_string=msg_string)
    sysMessage = SystemMessage(content=sysPrompt)
    response = BrainModel.invoke([sysMessage])
    return str(response.content)

def get_memory_dir():
    file_parent = Path(data.__file__).absolute().parent
    memory_dir = file_parent / "memory"
    if not memory_dir.exists(): os.mkdir(memory_dir)
    return memory_dir

def get_time_date() -> tuple[str, str]:
    now = datetime.now()
    return now.strftime(f"%d/%m/%Y"), now.strftime(r"%H:%M:%S")

def datetime_formater(summarys: list[str]) -> list[str]:
    docs = []
    for summary in summarys:
        current_date, current_time = get_time_date()
        summary_template = f"[{current_date} - {current_time}] {summary}"
        docs.append(summary_template)
        
    return docs

def message_load_deserial(path) -> messageList:
    with open(path, 'r', encoding='utf-8') as f:
        content = json.load(f)
        message_deserial = [
            HumanMessage(**msg) if msg['type'] == 'human' else AIMessage(**msg) 
            for msg in content
        ]
    return message_deserial
    
def chunk_print(inChunk):
    if type(inChunk) == AIMessageChunk:
        print(inChunk.content, end='', flush=True)
        if inChunk.chunk_position == 'last': print()

def text_sanitize(text: str):
    text = emoji.replace_emoji(text, replace='')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def split_text(text: str) -> tuple[list[str], str]:
    splits = [s.strip() for s in re.findall(r"[^.?]+[.?]?", text) if s.strip()]
    if len(splits) == 0: return splits[:-1], ''
    
    return splits[:-1], splits[-1]

async def process_sentence(text: str) -> str:
    text = text_sanitize(text)
    
    chunks, save_text = split_text(text)
    for chunk in chunks:
        await text_queue.put(chunk)
    return save_text