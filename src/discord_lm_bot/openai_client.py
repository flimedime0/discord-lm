from functools import cache
import os

from openai import AsyncOpenAI


@cache
def client_oai() -> AsyncOpenAI:
    # dummy key ⇒ no network access during tests
    return AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", "dummy"))


DEFAULT_O3_PARAMS = {
    "temperature": 1,
    # optional tuning knobs you may want:
    "max_tokens": None,
    "stop": None,
    "seed": None,
    # "stream": False,
}

# System prompt enforcing inline citations with a source list
SYSTEM_CITE = (
    "After answering, add a line 'Sources:' followed by every URL from "
    "web_search, one per line. Speak naturally."
)

__all__ = ["client_oai", "DEFAULT_O3_PARAMS", "SYSTEM_CITE"]
