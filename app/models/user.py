# app/models/user.py

from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Literal
from datetime import datetime
from enum import Enum

class LanguageEnum(str, Enum):
    tr = "tr"
    en = "en"
    de = "de"
    fr = "fr"
    es = "es"

class GenreEnum(str, Enum):
    action = "action"
    comedy = "comedy"
    drama = "drama"
    horror = "horror"
    romance = "romance"
    thriller = "thriller"
    documentary = "documentary"
    animation = "animation"
    scifi = "scifi"
    fantasy = "fantasy"

class UserPreferences(BaseModel):
    language: LanguageEnum = Field(default=LanguageEnum.tr)
    genres: List[GenreEnum] = Field(default_factory=list)
    maturity_rating: Literal["G", "PG", "PG-13", "R", "NC-17"] = Field(default="PG")

class UserSecurity(BaseModel):
    two_factor_enabled: bool = Field(default=False)
    login_attempts: int = Field(default=0)

class UserDocument(Document):
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    password: str
    first_name: str
    last_name: str
    avatar: Optional[str] = None
    subscription: Literal["free", "basic", "premium"] = Field(default="free")
    
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    
    is_verified: bool = Field(default=False)
    is_active: bool = Field(default=True)
    
    security: UserSecurity = Field(default_factory=UserSecurity)
    
    devices: List[dict] = Field(default_factory=list)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    version: int = Field(default=0, alias="__v")
    last_login: Optional[datetime] = None
    country: Optional[str] = "sikistan"
    phone: Optional[str] = "123213213213123123213"
    birthdate: Optional[datetime] = Field(default_factory=lambda: datetime(2025, 6, 20))

    class Settings:
        name = "users"

    def __repr__(self) -> str:
        return f"<UserDocument(id={self.id}, username='{self.username}', email='{self.email}')>"