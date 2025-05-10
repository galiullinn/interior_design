from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database import get_db
from src.dependencies.user import get_current_active_user
from src.models import User
from src.schemas.project import ProjectResponse, ProjectCreate, ProjectUpdate
from src.services.project import get_user_projects, get_user_project_by_id, create_project, update_project, delete_project

router = APIRouter(prefix="/projects", tags=["Проекты"])


@router.get("", response_model=List[ProjectResponse], summary="Получить список проектов пользователя")
async def get_projects_endpoint(
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db)
):
    projects = await get_user_projects(current_user.id, db)
    return projects


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED, summary="Создать новый проект")
async def create_project_endpoint(
        project_data: ProjectCreate,
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db)
):
    db_project = await create_project(current_user.id, project_data, db)
    return db_project


@router.get("/{project_id}", response_model=ProjectResponse, summary="Получить данные одного проекта пользователя")
async def get_project_endpoint(
        project_id: int,
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db)
):
    project = await get_user_project_by_id(current_user.id, project_id, db)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Проект не найден"
        )

    return project


@router.patch("/{project_id}", response_model=ProjectResponse, summary="Обновить данные проекта пользователя")
async def update_project_endpoint(
        project_id: int,
        update_data: ProjectUpdate,
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db)
):
    updated_project = await update_project(current_user.id, project_id, update_data, db)

    if updated_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Проект не найден"
        )

    return updated_project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить проект пользователя")
async def delete_project_endpoint(
        project_id: int,
        current_user: User = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db)
):
    deleted_project = await delete_project(current_user.id, project_id, db)
    if deleted_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Проект не найден"
        )

    return {"msg": f"Проект {project_id} удален"}