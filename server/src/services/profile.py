from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from src.schemas.profile import ProfileUpdateRequest


async def update_user_profile(user: User, data: ProfileUpdateRequest, db: AsyncSession) -> User | None:
    updated_data = data.model_dump(exclude_unset=True)

    if 'email' is updated_data and updated_data['email'] != user.email:
        if updated_data['email'] is not None:
            existing_user = await db.scalar(
                select(User)
                .where(User.email == updated_data['email'])
            )
            if existing_user:
                return None

        user.email = updated_data['email']
        del updated_data['email']

    if user.profile:
        for field, value in updated_data.items():
            if hasattr(user.profile, field):
                setattr(user.profile, field, value)

    await db.commit()
    await db.refresh(user)
    return user