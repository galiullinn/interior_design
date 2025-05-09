from pydantic import BaseModel, EmailStr


class TokenRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: EmailStr
    user_id: int


class RefreshTokenRequest(BaseModel):
    refresh_token: str