from fastapi import (
    Depends,
    WebSocket,
    APIRouter,
)
from sqlalchemy import select, insert
from starlette.websockets import WebSocketDisconnect

from src.chat.models import Message
from src.database import get_async_session, _async_session_maker

chat_router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, add_to_db: bool = True):
        if add_to_db:
            await self.__add_messages(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    async def __add_messages(self, message: str):
        async with _async_session_maker() as session:
            state = insert(Message).values(text=message)
            await session.execute(state)
            await session.commit()


manager = ConnectionManager()


@chat_router.get("/last_messages")
async def get_last_messages(session=Depends(get_async_session)):
    q = select(Message).order_by(Message.id.desc()).limit(5)
    res = await session.execute(q)
    messages: list[Message] = res.scalars().all()
    return [m.text for m in messages]


@chat_router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket,
                             client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", add_to_db=False)
