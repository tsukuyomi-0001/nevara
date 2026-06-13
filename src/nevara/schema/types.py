from langchain_core.messages import AIMessage, HumanMessage
from nevara.config import config

memory = config['memory']
model = config['model']

messageType = AIMessage | HumanMessage
messageList = list[messageType]

class ModelConfig:
    brain_model: str = model['brain']
    ctx_window: int = model['ctx_window']
    keep_alive: str = model['alive']
    embed_model: str = model['embedModel']

class MemoryConfig:
    messages_ctx: int = memory['ctx']
    messages_token_cap: float = memory['token_cap']
    keepLatestHistory: int = memory['latestHistory']