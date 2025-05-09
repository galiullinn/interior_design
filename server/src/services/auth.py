from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, Profile
from schemas.auth import RegisterRequest
from schemas.token import TokenResponse
from services.security import hash_password, verify_password, create_access_token, create_refresh_token, verify_token


async def create_user_with_profile(user_data: RegisterRequest, db: AsyncSession) -> User | None:
    existing_user = await db.scalar(
        select(User)
        .where(User.email == user_data.email)
    )
    if existing_user:
        return None

    hashed_password = hash_password(user_data.password)

    db_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        is_active=True,
        is_admin=False,
    )
    db.add(db_user)
    await db.flush()

    db_profile = Profile(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        user_id=db_user.id,
    )
    db.add(db_profile)

    await db.commit()
    await db.refresh(db_user)

    return db_user


async def authenticate(email: str, password: str, db: AsyncSession) -> User | None:
    user = await db.scalar(
        select(User)
        .where(User.email == email)
    )

    if not user or not verify_password(password, user.password_hash):
        return None

    return user


async def create_user_tokens(user: User) -> TokenResponse:
    access_token_payload = {"sub": user.email, "user_id": user.id}
    refresh_token_payload = {"sub": user.email, "user_id": user.id}

    access_token = create_access_token(access_token_payload)
    refresh_token = create_refresh_token(refresh_token_payload)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


async def refresh_user_tokens(refresh_token: str, db: AsyncSession) -> TokenResponse | None:
    payload = verify_token(refresh_token)

    if not payload:
        return None

    user_id = payload.user_id
    user = await db.get(User, user_id)
    if not user or not user.is_active:
        return None

    new_tokens = await create_user_tokens(user)
    return new_tokens