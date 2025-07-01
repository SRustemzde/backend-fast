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
    
    title: Indexed(str) # 'name' alanı dummyData'da
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
            # Başlık ve açıklama üzerinde metin araması için text indeksi
            IndexModel(
                [
                    ("title", TEXT),
                    ("description", TEXT),
                    # İsteğe bağlı: ("starring", TEXT), ("tags", TEXT)
                ],
                name="content_text_search_idx",
                default_language="english", # Arama dilini belirtmek iyi bir pratiktir
                weights={"title": 10, "description": 5} # Başlığa daha fazla ağırlık ver
            ),
            # Diğer sık kullanılan alanlar için indeksler
            IndexModel([("rating", -1)], name="rating_desc_idx"),
            IndexModel([("release_date", -1)], name="release_date_desc_idx"),
            IndexModel([("content_type", 1)], name="content_type_idx"),
            IndexModel([("source_name", 1), ("source_id", 1)], name="source_details_idx", unique=False), # unique=False olabilir
            IndexModel([("categories.id", 1)], name="categories_id_idx", sparse=True) # Eğer Link kullanıyorsak bu şekilde ID'ye göre index
        ]

    def __repr__(self) -> str:
        return f"<ContentDocument(id={self.id}, title='{self.title}')>"