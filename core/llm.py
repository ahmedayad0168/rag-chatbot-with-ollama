from functools import lru_cache
from langchain_ollama import OllamaLLM

from config import LLM_MODEL


@lru_cache(maxsize=1)
def get_llm():
    return OllamaLLM(model= LLM_MODEL)