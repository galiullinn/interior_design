from pydantic import BaseModel, Field, EmailStr


class ProfileUpdateRequest(BaseModel):
    first_name: str | None = Field(None, max_length=50)
    last_name: str | None = Field(None, max_length=50)
    bio: str | None = Field(None, max_length=300)
    image_url: str | None = None
    email: EmailStr | None = None


class ProfileDataSchema(BaseModel):
    first_name: str | None = Field(None, max_length=50)
    last_name: str | None = Field(None, max_length=50)
    bio: str | None = Field(None, max_length=300)
    image_url: str | None = None

    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    id: int
    email: EmailStr
    profile: ProfileDataSchema

    class Config:
        from_attributes = True