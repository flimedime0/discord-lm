import json
import os

import httpx

SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search the public internet for up-to-date information.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query",
                },
                "num_results": {
                    "type": "integer",
                    "description": "How many results (1-10)",
                    "default": 8,
                },
            },
            "required": ["query"],
        },
    },
}


async def do_search(query: str, num_results: int = 8) -> str:
    """Return Google CSE results (title + link) as JSON string."""
    api_key = os.getenv("GOOGLE_API_KEY")
    cse_id = os.getenv("GOOGLE_CSE_ID")
    if not api_key or not cse_id:
        return json.dumps([{"error": "Google CSE keys not set"}])

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cse_id,
        "q": query,
        "num": num_results,
    }
    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params, timeout=10)
        data = r.json()

    items = data.get("items", [])
    results = [{"title": it["title"], "url": it["link"], "snippet": it["snippet"]} for it in items]
    return json.dumps(results, ensure_ascii=False)
