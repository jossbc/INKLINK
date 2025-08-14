from fastapi import APIRouter
from models.login import Login
from controllers.users import login

router = APIRouter(prefix="/login", tags=["login"])
                   
@router.post("")
async def login_endpoint(login_data: Login) -> dict:
    return await login(login_data)