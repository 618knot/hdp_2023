from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel
from sqlite.util import session
from sqlite.create_user import User

RESOURCE_NAME: str = "user"

router: APIRouter = APIRouter(
    prefix=f"/{RESOURCE_NAME}",
    tags=[RESOURCE_NAME],
)

class UserProp(BaseModel):
    laboratory_id: int
    name: str

@router.post("/signup")
async def signup(props: UserProp) -> dict:
    user = User(name=props.name, laboratory_id=props.laboratory_id)
    session.add(user)
    session.commit()

    return {"status": "ok"}