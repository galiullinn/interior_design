from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, model_validator
from pydantic_core import PydanticCustomError


class RegisterRequest(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    password_confirm: str = Field(..., min_length=8)

    @model_validator(mode='after')
    def password_match(self):
        if self.password != self.password_confirm:
            raise PydanticCustomError(
                'value_error',
                'Пароли не совпадают.',
                {'field': 'password_confirm'}
            )
        return self


class RegisterResponse(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True