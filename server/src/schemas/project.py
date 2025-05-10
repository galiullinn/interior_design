from datetime import datetime

from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: str | None = Field(None, max_length=300)
    scene_data: str | None = None
    image_preview_url: str | None = None
    is_public: bool | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    title: str | None = Field(None, max_length=100)
    description: str | None = Field(None, max_length=300)
    scene_data: str | None = None
    image_preview_url: str | None = None
    is_public: bool | None = None


class ProjectResponse(ProjectBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True