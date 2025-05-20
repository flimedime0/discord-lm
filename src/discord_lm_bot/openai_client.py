from openai import AsyncOpenAI

from .config import OPENAI_API_KEY

client_oai = AsyncOpenAI(api_key=OPENAI_API_KEY)

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
