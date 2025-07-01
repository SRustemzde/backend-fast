# app/schemas/watchlist.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .content import ContentPublicShort # İçerik bilgisini göstermek için

# İzleme listesine öğe eklemek için request
class WatchlistItemCreate(BaseModel):
    content_id: str # Eklenecek içeriğin global ID'si

# İzleme listesi öğesini API'den döndürmek için
class WatchlistItemPublic(BaseModel):
    id: str # WatchlistItem'ın kendi ID'si
    user_id: str # Kullanıcı ID'si (string olarak)
    content: ContentPublicShort # İlişkili içerik bilgisi (kısa versiyon)
    added_at: datetime

    class Config:
        from_attributes = True