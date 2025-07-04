# app/models/content.py

from beanie import Document, Indexed, Link
from pydantic import Field
from typing import Optional, List
from datetime import datetime
from pymongo import IndexModel, TEXT # TEXT import edildi
from .category import CategoryDocument # CategoryDocument modelini import ediyoruz

class ContentDocument(Document):
    # Frontend'deki dummyData.js'den gelen alanlar
    source_id: Optional[int] = None # dummyData'daki orijinal id (örn: homeData içindeki id)
    source_name: Optional[str] = None # dummyData'daki kaynak adı (örn: "homeData", "trending")
    
    title: str # 'name' alanı dummyData'da
    description: Optional[str] = None # 'desc' alanı dummyData'da
    release_date: Optional[str] = None # 'date' alanı dummyData'da (string olarak tuttuk, datetime'a çevrilebilir)
    duration: Optional[str] = None # 'time' alanı dummyData'da
    rating: Optional[float] = None
    
    cover_image_url: Optional[str] = None # 'cover' alanı dummyData'da
    thumbnail_url: Optional[str] = None # Thumbnail image for small previews
    video_url: Optional[str] = None # 'video' alanı dummyData'da
    trailer_url: Optional[str] = None # Trailer video URL
    
    starring: Optional[List[str]] = Field(default_factory=list) # 'starring' alanı (string listesi)
    director: Optional[str] = None # Director name
    language: Optional[str] = None # Content language
    country: Optional[str] = None # Production country
    tags: Optional[List[str]] = Field(default_factory=list) # 'tags' alanı (string listesi)
    
    content_type: str = Field(default="MOVIE") # "MOVIE" veya "TV_SHOW" olabilir (Enum yapılabilir)

    # Featured and trending flags
    featured: bool = Field(default=False)
    trending: bool = Field(default=False)

    # Kategori ile ilişki
    categories: Optional[List[Link[CategoryDocument]]] = Field(default_factory=list)
    # Alternatif olarak, eğer direkt CategoryDocument nesnelerini saklamak isterseniz:
    # categories: Optional[List[CategoryDocument]] = Field(default_factory=list)
    # Bu durumda Beanie, referans yerine gömülü dökümanlar olarak saklamaya çalışabilir
    # veya Link'leri otomatik yönetebilir. Link kullanmak genellikle daha esnektir.

    # Otomatik zaman damgaları
    time_created: datetime = Field(default_factory=datetime.utcnow)
    time_updated: Optional[datetime] = None

    class Settings:
        name = "contents"
        indexes = [
            # Minimal indexes for now
            IndexModel([("content_type", 1)], name="content_type_idx"),
            IndexModel([("rating", -1)], name="rating_desc_idx")
        ]

    def __repr__(self) -> str:
        return f"<ContentDocument(id={self.id}, title='{self.title}')>"