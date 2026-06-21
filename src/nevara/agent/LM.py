from langchain_ollama import ChatOllama, OllamaEmbeddings
from transformers import AutoTokenizer

from nevara.schema.types import ModelConfig

## set tokenizer through config ! future update
qwen_tokenizer = AutoTokenizer.from_pretrained('Qwen/Qwen3.5-4B')

def qwen_token_encoder(text: str) -> list[int]:
    return qwen_tokenizer.encode(text)

ChatModel = ChatOllama(
    model = ModelConfig.brain_model, 
    reasoning = False, 
    num_ctx = ModelConfig.ctx_window,
    keep_alive=ModelConfig.keep_alive,
    custom_get_token_ids=qwen_token_encoder,
    top_p=0.9,
    repeat_penalty=1.1,
    num_predict=512,
    temperature=0.7
)

StructureModel = ChatOllama(
    model = ModelConfig.structure_model,
    reasoning = False, 
    num_ctx = ModelConfig.ctx_window,
    keep_alive=ModelConfig.keep_alive,
    custom_get_token_ids=qwen_token_encoder,
    top_p=0.9,
    repeat_penalty=1.1,
    num_predict=512,
    temperature=0.7
)

EmbeddingModel = OllamaEmbeddings(
    model = ModelConfig.embed_model
)