from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database import get_db
from src.dependencies.user import get_current_active_user
from src.models import User
from src.schemas.profile import UserProfileResponse, ProfileUpdateRequest
from src.services.profile import update_user_profile

router = APIRouter(prefix="/profile", tags=["Профиль"])


@router.get("", response_model=UserProfileResponse, summary="Получить профиль текущего пользователя")
async def get_profile(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.patch("", response_model=UserProfileResponse, summary="Обновить профиль текущего пользователя")
async def update_profile(
        updated_data: ProfileUpdateRequest,
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db)
):
    updated_data = await update_user_profile(current_user, updated_data, db)

    if updated_data is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Данный адрес эл. почты уже занят"
        )

    return updated_data