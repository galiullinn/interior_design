from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status

from src.database import get_db
from src.models import User
from src.services.security import verify_token


oauth_scheme = HTTPBearer()


async def get_current_user(
        token: HTTPAuthorizationCredentials = Depends(oauth_scheme),
        db: AsyncSession = Depends(get_db)
) -> User:
    payload = verify_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось подтвердить учетные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.user_id
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось подтвердить учетные данные (отсутствует идентификатор пользователя)",
            headers={"WWW-Authenticate": "Bearer"},
        )

    smtm = (
        select(User)
        .where(User.id == user_id)
        .options(joinedload(User.profile))
    )
    user = await db.scalar(smtm)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось подтвердить учетные данные (пользователь не найден)",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Неактивный пользователь"
        )
    return current_user