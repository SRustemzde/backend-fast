# app/schemas/content.py

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .category import CategoryPublic # Kategori şemasını import et

# Temel İçerik Şeması
class ContentBase(BaseModel):
    title: str
    description: Optional[str] = None
    release_date: Optional[str] = None
    duration: Optional[str] = None
    rating: Optional[float] = None
    cover_image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    video_url: Optional[str] = None
    trailer_url: Optional[str] = None
    starring: Optional[List[str]] = Field(default_factory=list)
    director: Optional[str] = None
    language: Optional[str] = None
    country: Optional[str] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    content_type: str = "MOVIE"
    source_id: Optional[int] = None
    source_name: Optional[str] = None
    featured: bool = False
    trending: bool = False

# İçerik Oluşturma Şeması
class ContentCreate(ContentBase):
    # Oluştururken kategori ID'lerini string listesi olarak alabiliriz
    category_ids: Optional[List[str]] = Field(default_factory=list)

# İçerik Güncelleme Şeması
class ContentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    release_date: Optional[str] = None
    duration: Optional[str] = None
    rating: Optional[float] = None
    cover_image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    video_url: Optional[str] = None
    trailer_url: Optional[str] = None
    starring: Optional[List[str]] = None
    director: Optional[str] = None
    language: Optional[str] = None
    country: Optional[str] = None
    tags: Optional[List[str]] = None
    content_type: Optional[str] = None
    category_ids: Optional[List[str]] = None # Güncellemede de kategori ID'leri
    source_id: Optional[int] = None
    source_name: Optional[str] = None
    featured: Optional[bool] = None
    trending: Optional[bool] = None


# API'den Dönen İçerik Şeması (Detaylı)
class ContentPublic(ContentBase):
    id: str # MongoDB _id
    # Link ile bağladığımız kategorileri doğrudan CategoryPublic şemasıyla döndürebiliriz
    categories: Optional[List[CategoryPublic]] = Field(default_factory=list)
    time_created: datetime
    time_updated: Optional[datetime] = None

    class Config:
        from_attributes = True

# Listeleme için daha kısa bir içerik şeması (opsiyonel)
class ContentPublicShort(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    cover_image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    video_url: Optional[str] = None
    trailer_url: Optional[str] = None
    duration: Optional[str] = None
    rating: Optional[float] = None
    release_date: Optional[str] = None
    content_type: str
    starring: Optional[List[str]] = Field(default_factory=list)
    director: Optional[str] = None
    language: Optional[str] = None
    country: Optional[str] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    featured: bool = False
    trending: bool = False

    class Config:
        from_attributes = True