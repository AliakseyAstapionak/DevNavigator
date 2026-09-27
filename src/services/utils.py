import httpx
from asyncio import Lock

_clients: dict[str, httpx.AsyncClient] = {}

_lock = Lock()
async def get_client(name: str) -> httpx.AsyncClient:
    if name not in _clients:
        async with _lock:      
            if name not in _clients:  
                _clients[name] = httpx.AsyncClient(
                    timeout=10.0,
                    limits=httpx.Limits(max_connections=200, max_keepalive_connections=50),
                )
    return _clients[name]


async def close_client() -> None:
    for client in _clients.values():
        await client.aclose()
    _clients.clear()