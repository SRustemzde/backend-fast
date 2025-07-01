# app/schemas/watch_history.py

from pydantic import BaseModel, Field, conint
from typing import Optional
from datetime import datetime
from .content import ContentPublicShort

# İzleme geçmişine öğe eklemek/güncellemek için request
class WatchHistoryItemCreateOrUpdate(BaseModel):
    content_id: str
    progress_percentage: conint(ge=0, le=100)

# İzleme geçmişi öğesini API'den döndürmek için
class WatchHistoryItemPublic(BaseModel):
    id: str
    user_id: str
    content: ContentPublicShort
    progress_percentage: int
    watched_at: datetime # İlk izlenme tarihi gibi düşünülebilir
    last_watched_at: Optional[datetime] = None # Son izlenme tarihi

    class Config:
        from_attributes = True