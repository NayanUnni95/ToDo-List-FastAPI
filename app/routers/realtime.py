from fastapi import APIRouter, WebSocket
from ..schema import schemas
from ..repository import realtime
from ..database.config import SessionDep
from ..services.Oauth2 import get_current_user

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    return await realtime.websocket_connection(websocket)
