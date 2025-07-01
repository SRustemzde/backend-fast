# app/models/watchlist.py

from beanie import Document, Link
from pydantic import Field
from typing import Optional
from datetime import datetime
from pymongo import IndexModel # pymongo'dan IndexModel'i import et

from .user import UserDocument
from .content import ContentDocument

class WatchlistItemDocument(Document):
    user: Link[UserDocument]
    content: Link[ContentDocument]
    added_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "watchlist_items"
        # Birleşik benzersiz indeks
        indexes = [
            IndexModel(
                [
                    ("user", 1),      # 'user' alanının referans ID'si üzerinden
                    ("content", 1),   # 'content' alanının referans ID'si üzerinden
                ],
                name="user_content_unique_idx", # İndekse bir isim verelim
                unique=True
            )
        ]
    
    def __repr__(self) -> str:
        # Link objesinden ID'yi almak için .ref.id kullanmak yerine,
        # eğer document populate edilmişse doğrudan .id kullanılabilir.
        # Ancak __repr__ içinde populate edilmemiş olabilir, bu yüzden dikkatli olmak gerek.
        # Şimdilik basit tutalım veya populate edilme durumuna göre kontrol ekleyelim.
        user_id_repr = str(self.user.id) if self.user and hasattr(self.user, 'id') and self.user.id else "N/A"
        content_id_repr = str(self.content.id) if self.content and hasattr(self.content, 'id') and self.content.id else "N/A"
        return f"<WatchlistItemDocument user_id={user_id_repr} content_id={content_id_repr}>"