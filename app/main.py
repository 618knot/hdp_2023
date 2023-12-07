from fastapi import FastAPI, WebSocket
# from routers import users, sessions, rent_parking, reverse_geocoding, chat_rooms
# from starlette.middleware.cors import CORSMiddleware
import laboratory, user, being_status
import os

app = FastAPI()

# # CORSを回避するために追加
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,   # 追記により追加
#     allow_methods=["*"],      # 追記により追加
#     allow_headers=["*"]       # 追記により追加
# )
# # ssl検証を無効にする
# os.environ['UVICORN_CMD_SSL'] = '0'

@app.on_event("startup")
def startup_event() -> None:
    pass

# @app.get("/")
# async def hello() -> str:
#     return "HELLO"

@app.websocket("/ws/{id}")
async def websocket_endpoint(websocket: WebSocket, id: int):
    await websocket.accept()
    tmp = 0
    while True:
        
        await websocket.receive()

        tmp += 1

        await websocket.send_text(f"{tmp}")

app.include_router(laboratory.router)
app.include_router(user.router)
app.include_router(being_status.router)