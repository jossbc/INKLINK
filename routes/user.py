from fastapi import APIRouter
from models.users import User
from controllers.users import create_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/")
async def create_user_endpoint(user: User) -> User:
    return await create_user(user)