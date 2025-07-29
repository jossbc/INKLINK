from fastapi import APIRouter
from fastapi import Request
from models.publisher import Publisher
from utils.security import validateadmin
from controllers.publisher import (
    create_publisher,
    get_all_publishers,
    get_publisher_by_id,
)
from utils.security import validateadmin

router = APIRouter(prefix="/publishers", tags=["publishers"])

@router.get("/", response_model=list[Publisher])
async def endpoint_get_all_publishers():
    return await get_all_publishers()

@router.post("/", response_model=Publisher)
@validateadmin
async def endpoint_create_publisher(request: Request, publisher: Publisher):
    return await create_publisher(publisher)

@router.get("/{publisher_id}", response_model=Publisher)
async def endpoint_get_publisher_by_id(publisher_id: str):
    return await get_publisher_by_id(publisher_id)