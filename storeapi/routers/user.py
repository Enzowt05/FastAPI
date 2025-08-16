from fastapi import APIRouter, HTTPException, status

from storeapi.models.user import UserIn
from storeapi.security import get_user

router = APIRouter()


@router.post("/register", status_code=201)
async def register(user: UserIn):
    if await get_user(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with that email already exists",
        )
