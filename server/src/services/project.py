from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Project
from src.schemas.project import ProjectCreate, ProjectUpdate


async def get_user_projects(user_id: int, db: AsyncSession) -> List[Project]:
    result = await db.execute(
        select(Project)
        .where(Project.user_id == user_id)
        .order_by(Project.created_at)
    )
    return list(result.scalars().all())


async def get_user_project_by_id(user_id: int, project_id: int, db: AsyncSession) -> Project | None:
    result = await db.execute(
        select(Project)
        .where(Project.id == project_id, Project.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def create_project(user_id: int, project_data: ProjectCreate, db: AsyncSession) -> Project:
    db_project = Project(**project_data.model_dump())
    db_project.user_id = user_id

    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)

    return db_project


async def update_project(user_id: int, project_id: int, updated_data: ProjectUpdate, db: AsyncSession) -> Project | None:
    db_project = await get_user_project_by_id(user_id, project_id, db)
    if db_project is None:
        return None

    update_data_dict = updated_data.model_dump(exclude_unset=True)

    for field, value in update_data_dict.items():
        if hasattr(db_project, field):
            setattr(db_project, field, value)

    await db.commit()
    await db.refresh(db_project)

    return db_project


async def delete_project(user_id: int, project_id: int, db: AsyncSession) -> Project | None:
    db_project = await get_user_project_by_id(user_id, project_id, db)
    if db_project is None:
        return None

    await db.delete(db_project)
    await db.commit()

    return db_project