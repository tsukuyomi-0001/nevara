from langchain_core.messages import AIMessage, HumanMessage
from configs import config

memory = config['memory']
model = config['model']

messageType = AIMessage | HumanMessage
messageList = list[messageType]

class ModelConfig:
    brain_model: str = model['brain']
    structure_model: str = model['struct_model']
    ctx_window: int = model['ctx_window']
    keep_alive: str = model['keep_alive']
    embed_model: str = model['embed_model']

class MemoryConfig:
    messages_ctx: int = memory['ctx']
    messages_token_cap: float = memory['token_cap']
    keepLatestHistory: int = memory['latestHistory']