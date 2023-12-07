from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel
from sqlite.create_laboratory import Laboratory
from sqlite.util import session

RESOURCE_NAME: str = "laboratory"

router: APIRouter = APIRouter(
    prefix=f"/{RESOURCE_NAME}",
    tags=[RESOURCE_NAME],
)

class LabProp(BaseModel):
    name: str

@router.post("/create")
async def create(props: LabProp) -> dict:
    lab = Laboratory(name=props.name)
    session.add(lab)
    session.commit()

    return {"status": "ok"}