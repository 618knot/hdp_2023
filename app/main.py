from fastapi import FastAPI, WebSocket
import laboratory, user
import os
import datetime
from typing import Optional
from fastapi import APIRouter, WebSocket
from pydantic import BaseModel
from sqlalchemy import desc
from sqlite.create_being_status import BeingStatus
from sqlite.util import session
from sqlite.create_user import User
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# CORSを回避するために追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)
# ssl検証を無効にする
os.environ['UVICORN_CMD_SSL'] = '0'

@app.on_event("startup")
def startup_event() -> None:
    pass

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[dict] = {}

    async def connect(self, websocket: WebSocket, laboratory_id: int, ws_id: int) -> None:
        await websocket.accept()

        self.active_connections[str(ws_id)] = {"websocket": websocket, "laboratory_id": laboratory_id}

    def disconnect(self, ws_id: int) -> None:
        self.active_connections.pop(str(ws_id))

    async def send_personal_message(self, message: dict, ws_id: int) -> None:
        await self.active_connections[str(ws_id)].send_json(message)

    async def send_laboratory_message(self, message: dict, laboratory_id: int) -> None:
        for connection in self.active_connections.values():
            if connection["laboratory_id"] == laboratory_id:
                await connection["websocket"].send_json(message)


class BeingProps(BaseModel):
    user_id: int

ws_manager = ConnectionManager()

@app.get("/enter/{user_id}")
async def enter(user_id: int) -> dict:
    laboratory_id = session.query(User.laboratory_id).filter(User.id == user_id)
    being = BeingStatus(user_id=user_id, laboratory_id=laboratory_id, status=True)
    session.add(being)
    session.commit()

    await ws_manager.send_laboratory_message(get_being_status(being.laboratory_id), str(being.laboratory_id), )    

    return {"status": "ok"}

@app.get("/leave/{user_id}")
async def leave(user_id: int) -> dict:
    laboratory_id = session.query(User.laboratory_id).filter(User.id == user_id)
    being = BeingStatus(user_id=user_id, laboratory_id=laboratory_id, status=False)
    session.add(being)
    session.commit()

    await ws_manager.send_laboratory_message(get_being_status(being.laboratory_id), str(being.laboratory_id))

    return {"status": "ok"}

@app.get("/history/{user_id}")
async def show(user_id: int) -> dict:
    laboratory_id = session.query(User.laboratory_id).filter(User.id == user_id)
    # history = session.query(BeingStatus.time, BeingStatus.status, User.name).join(User, BeingStatus.laboratory_id == User.laboratory_id).all()
    history = session.query(BeingStatus.time, BeingStatus.status, User.name).join(User, (BeingStatus.user_id == User.id) & (BeingStatus.laboratory_id == User.laboratory_id)).order_by(desc(BeingStatus.time)).all()

    response = { "history": [] }

    for item in history:
        response["history"].append({ 
            "time": item[0].strftime("%Y/%m/%d %H:%M"),
            "status": item[1],
            "user": item[2]
            })

    return response

@app.get("/status/{laboratory_id}")
async def being_status(laboratory_id: int) -> dict:
    return get_being_status(laboratory_id)

@app.websocket("/ws/{laboratory_id}/{ws_id}")
async def websocket_endpoint(websocket: WebSocket, laboratory_id: int, ws_id: int):
    await ws_manager.connect(websocket, laboratory_id, ws_id)
    
    try:
        while True:
            await websocket.receive()
    except:
        pass
    finally:
        ws_manager.disconnect(ws_id)

def get_being_status(laboratory_id: int) -> dict:
    # laboratory_id = session.query(User.laboratory_id).filter(User.id == user_id)
    users = session.query(User.id, User.name, User.student_number).filter(User.laboratory_id == laboratory_id)

    statuses = { "status": [] }
    for user in users:
        status = session.query(BeingStatus.status, BeingStatus.time).order_by(desc(BeingStatus.time)).filter(user[0] == BeingStatus.user_id).first() #本当はテーブル結合でどうにかするところ

        if status:
            statuses["status"].append({
            "being": status[0],
            "name": user[1],
            "student_number": user[2],
            "user_id": user[0] 
        })
        else:
            statuses["status"].append({
            "being": "-",
            "name": user[1],
            "student_number": user[2],
            "user_id": user[0]
        })
            
    return statuses

app.include_router(laboratory.router)
app.include_router(user.router)