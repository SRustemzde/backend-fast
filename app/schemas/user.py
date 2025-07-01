# app/schemas/user.py

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

class UserPreferencesSchema(BaseModel):
    language: LanguageEnum = LanguageEnum.tr
    genres: List[GenreEnum] = []
    maturity_rating: Literal["G", "PG", "PG-13", "R", "NC-17"] = "PG"

class UserSecuritySchema(BaseModel):
    two_factor_enabled: bool = False
    login_attempts: int = 0

# --- Ana Kullanıcı Şemaları ---

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str
    last_name: str
    avatar: Optional[str] = None
    subscription: Literal["free", "basic", "premium"] = "free" 

class UserPublic(BaseModel):
    id: str
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    avatar: Optional[str] = None
    subscription: Literal["free", "basic", "premium"]
    
    preferences: UserPreferencesSchema
    
    is_verified: bool
    is_active: bool
    
    security: UserSecuritySchema
    
    devices: List[dict] = []
    
    created_at: datetime
    updated_at: Optional[datetime] = None
    version: int = Field(default=0, alias="__v")
    last_login: Optional[datetime] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    birthdate: Optional[datetime] = None

    class Config:
        from_attributes = True

# Token şeması (Aynı)
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[EmailStr] = None

class UserProfileUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[str] = None
    subscription: Optional[Literal["free", "basic", "premium"]] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    birthdate: Optional[datetime] = None

class UserPreferencesUpdate(BaseModel):
    preferences: Optional[UserPreferencesSchema] = None

class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)