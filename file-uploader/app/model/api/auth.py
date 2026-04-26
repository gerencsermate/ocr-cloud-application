from dataclasses import dataclass

from pydantic import BaseModel, Field, model_validator
from typing import Optional, Self
from enum import Enum

class LoginRequest(BaseModel):
    username: str = Field()
    password: str = Field()

class RegisterRequest(BaseModel):
    username: str = Field(min_length=5)
    password: str = Field(min_length=8)
    re_password: str = Field(min_length=8)
    as_admin: bool = Field()

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.re_password:
            raise ValueError("Passwords do not match!")
        return self

class Role(Enum):
    ADMIN = "admin"
    USER = "user"

class TokenData(BaseModel):
    user_id: str
    username: str
    role: Role 
    exp: Optional[int] = None