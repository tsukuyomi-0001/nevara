from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from pathlib import Path

from nevara.schema.types import messageList
from nevara.agent import LM
from nevara import prompts
import data
import json
import os

def messages_token_count(msg: list):
    return LM.ChatModel.get_num_tokens_from_messages(msg)

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
    
    sysPrompt = prompts.load_prompt("system/summary", msg_string=msg_string)
    sysMessage = SystemMessage(content=sysPrompt)
    response = LM.ChatModel.invoke([sysMessage])
    return str(response.content)

def get_memory_dir():
    file_parent = Path(data.__file__).absolute().parent
    memory_dir = file_parent / "memory"
    if not memory_dir.exists(): os.mkdir(memory_dir)
    return memory_dir

def message_load_deserial(path) -> messageList:
    with open(path, 'r', encoding='utf-8') as f:
        content = json.load(f)
        message_deserial = [
            HumanMessage(**msg) if msg['type'] == 'human' else AIMessage(**msg) 
            for msg in content
        ]
    return message_deserial