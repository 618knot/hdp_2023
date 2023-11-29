from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel

RESOURCE_NAME: str = "being"

router: APIRouter = APIRouter(
    prefix=f"/{RESOURCE_NAME}",
    tags=[RESOURCE_NAME],
)

class UserProps(BaseModel):
    pass

@router.post("/enter")
async def enter(props: UserProps):
    pass

@router.post("/leave")
async def leave(props: UserProps):
    pass