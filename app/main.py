from fastapi import FastAPI, WebSocket
# from routers import users, sessions, rent_parking, reverse_geocoding, chat_rooms
# from starlette.middleware.cors import CORSMiddleware
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

# @app.get("/")
# async def hello() -> str:
#     return "HELLO"

# @app.websocket("/ws/{id}")
# async def websocket_endpoint(websocket: WebSocket, id: int):
#     await websocket.accept()
#     tmp = 0
#     while True:
        
#         await websocket.receive()

#         tmp += 1

#         await websocket.send_text(f"{tmp}")

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

class BeingProps(BaseModel):
    user_id: int

ws_manager = ConnectionManager()
ws_connections = {}

@app.post("/enter")
async def enter(props: BeingProps) -> dict:
    global ws_connections, ws_manager
    laboratory_id = session.query(User.laboratory_id).filter(User.id == props.user_id)
    being = BeingStatus(user_id=props.user_id, laboratory_id=laboratory_id, status=True)
    session.add(being)
    session.commit()

    
    print(ws_connections)
    print("hoge")

    if str(being.laboratory_id) in ws_connections.keys():
        await ws_manager.send_message(get_being_status(being.laboratory_id), ws_connections[str(being.laboratory_id)])
    

    return {"status": "ok"}

@app.post("/leave")
async def leave(props: BeingProps) -> dict:
    global ws_connections, ws_manager
    laboratory_id = session.query(User.laboratory_id).filter(User.id == props.user_id)
    being = BeingStatus(user_id=props.user_id, laboratory_id=laboratory_id, status=False)
    session.add(being)
    session.commit()

    print(ws_connections)
    print(being.laboratory_id)
    print(str(being.laboratory_id) in ws_connections.keys())
    print("hoge")
    
    
    if str(being.laboratory_id) in ws_connections.keys():
        print("fuga")
        await ws_manager.send_message(get_being_status(being.laboratory_id), ws_connections[str(being.laboratory_id)])

    return {"status": "ok"}

@app.get("/history/{user_id}")
async def show(user_id: int) -> dict:
    laboratory_id = session.query(User.laboratory_id).filter(User.id == user_id)
    history = session.query(BeingStatus.time, BeingStatus.status, User.name).join(User, BeingStatus.laboratory_id == User.laboratory_id).all()

    # print(get_being_status(laboratory_id))
    # response = get_being_status(laboratory_id)
    response = { "history": [] }

    for item in history:
        response["history"].append({ 
            "time": item[0].strftime("%Y/%m/%d %H:%m"),
             "status": item[1],
             "user": item[2]
              })

    return response

@app.get("/status/{laboratory_id}")
async def being_status(laboratory_id: int) -> dict:
    return get_being_status(laboratory_id)

@app.websocket("/ws/{id}")
async def websocket_endpoint(websocket: WebSocket, id: int):
    global ws_connections, ws_manager
    ws_connections[str(id)] = websocket
    print(ws_connections)
    await ws_manager.connect(websocket)
    
    try:
        while True:
            await websocket.receive()
    except:
        pass
    finally:
        ws_manager.disconnect(websocket)
        ws_connections.pop(str(id))

def get_being_status(laboratory_id: int) -> dict:
    # laboratory_id = session.query(User.laboratory_id).filter(User.id == user_id)
    users = session.query(User.id, User.name).filter(User.laboratory_id == laboratory_id)

    statuses = { "status": [] }
    for user in users:
        status = session.query(BeingStatus.status, BeingStatus.time).order_by(desc(BeingStatus.time)).filter(user[0] == BeingStatus.user_id).first() #本当はテーブル結合でどうにかするところ

        if status:
            statuses["status"].append({
            "being": status[0],
            "name": user[1]
        })
        else:
            statuses["status"].append({
            "being": "-",
            "name": user[1]
        })
            
    return statuses

app.include_router(laboratory.router)
app.include_router(user.router)