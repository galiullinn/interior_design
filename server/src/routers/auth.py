from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database import get_db
from src.schemas.auth import RegisterRequest, RegisterResponse
from src.schemas.token import TokenResponse, TokenRequest, RefreshTokenRequest
from src.services.auth import create_user_with_profile, authenticate, create_user_tokens, refresh_user_tokens

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя"
)
async def register(user_data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    db_user = await create_user_with_profile(user_data, db)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Данный адрес эл. почты уже занят"
        )

    return RegisterResponse.model_validate(db_user)


@router.post(
    "/token",
    response_model=TokenResponse,
    summary="Получение токенов доступа"
)
async def login(form_data: TokenRequest, db: AsyncSession = Depends(get_db)):
    user = await authenticate(form_data.email, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный адрес эл. почты или пароль",
            headers={"WWW-Authenticate": "Bearer"}
        )

    tokens = await create_user_tokens(user)
    return tokens


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Обновление токенов по refresh токену"
)
async def refresh_token(refresh_request: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    tokens = await refresh_user_tokens(refresh_request.refresh_token, db)

    if tokens is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный или устаревший refresh токен",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return tokens