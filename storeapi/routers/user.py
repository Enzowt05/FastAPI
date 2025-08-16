from fastapi import APIRouter, HTTPException

from storeapi.models.user import UserIn
from storeapi.security import get_user

router = APIRouter()

@router.post("/register", status_code=201)
async def register(user: UserIn):
    if await get_user(user.email):
        raise HTTPException(
            status_code =400,
            detail="User with that email already exists"
        )