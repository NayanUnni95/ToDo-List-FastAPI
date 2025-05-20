from fastapi import APIRouter, WebSocket
from ..repository import realtime

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws")
async def websocket_endpoint(token: str, websocket: WebSocket):
    return await realtime.websocket_connection(token, websocket)
