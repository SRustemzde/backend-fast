# app/schemas/category.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Temel Kategori Şeması (veritabanından okuma için)
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None

# Kategori Oluşturma Şeması
class CategoryCreate(CategoryBase):
    pass

# Kategori Güncelleme Şeması
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None

# API'den Dönen Kategori Şeması
class CategoryPublic(CategoryBase):
    id: str # MongoDB _id
    time_created: datetime
    time_updated: Optional[datetime] = None

    class Config:
        from_attributes = True