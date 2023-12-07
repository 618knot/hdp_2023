import datetime
from typing import Optional
from fastapi import APIRouter, WebSocket
from pydantic import BaseModel
from sqlalchemy import desc
from sqlite.create_being_status import BeingStatus
from sqlite.util import session
from sqlite.create_user import User

RESOURCE_NAME: str = "being"

router: APIRouter = APIRouter(
    prefix=f"/{RESOURCE_NAME}",
    tags=[RESOURCE_NAME],
)

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

ws_connections = {}

@router.post("/enter")
async def enter(props: BeingProps) -> dict:
    laboratory_id = session.query(User.laboratory_id).filter(User.id == props.user_id)
    being = BeingStatus(user_id=props.user_id, laboratory_id=laboratory_id, status=True)
    session.add(being)
    session.commit()

    if str(props.user_id) in ws_connections:
        ws_manager: ConnectionManager = ws_connections[str(props.user_id)]
        ws_manager.send_message(get_being_status(laboratory_id))
    

    return {"status": "ok"}

@router.post("/leave")
async def leave(props: BeingProps) -> dict:
    laboratory_id = session.query(User.laboratory_id).filter(User.id == props.user_id)
    being = BeingStatus(user_id=props.user_id, laboratory_id=laboratory_id, status=False)
    session.add(being)
    session.commit()

    if str(props.user_id) in ws_connections:
        ws_manager: ConnectionManager = ws_connections[str(props.user_id)]
        ws_manager.send_message(get_being_status(laboratory_id))

    return {"status": "ok"}

@router.get("/history/{user_id}")
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

@router.get("/status/{laboratory_id}")
async def being_status(laboratory_id: int) -> dict:
    return get_being_status(laboratory_id)

@router.websocket("/ws/{id}")
async def websocket_endpoint(websocket: WebSocket, id: int):
    ws_manager = ConnectionManager()
    ws_connections[str(id)] = ws_manager
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
