# app/models/watch_history.py

from beanie import Document, Link
from pydantic import Field, conint
from typing import Optional
from datetime import datetime
from pymongo import IndexModel # pymongo'dan IndexModel'i import et

from .user import UserDocument
from .content import ContentDocument

class WatchHistoryItemDocument(Document):
    user: Link[UserDocument]
    content: Link[ContentDocument]
    watched_at: datetime = Field(default_factory=datetime.utcnow)
    progress_percentage: conint(ge=0, le=100) = Field(default=0)
    last_watched_at: Optional[datetime] = None

    class Settings:
        name = "watch_history_items"
        indexes = [
            IndexModel(
                [
                    ("user", 1),
                    ("content", 1),
                ],
                name="user_content_history_unique_idx", # İndekse bir isim verelim
                unique=True
            )
        ]

    def __repr__(self) -> str:
        user_id_repr = str(self.user.id) if self.user and hasattr(self.user, 'id') and self.user.id else "N/A"
        content_id_repr = str(self.content.id) if self.content and hasattr(self.content, 'id') and self.content.id else "N/A"
        return f"<WatchHistoryItemDocument user_id={user_id_repr} content_id={content_id_repr} progress={self.progress_percentage}%>"