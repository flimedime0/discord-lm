# File purpose: Hold global and model-specific defaults.

from typing import Any

GLOBAL_DEFAULTS: dict[str, Any] = {"model": "o3", "params": {"temperature": 1.0}}

SUPPORTED_PARAMS: dict[str, list[str]] = {
    "gpt-4o": ["temperature", "top_p", "max_tokens"],
    "o3": ["temperature", "max_tokens"],
}
