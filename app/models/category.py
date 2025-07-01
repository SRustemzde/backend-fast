# app/models/category.py

from beanie import Document, Indexed
from pydantic import Field
from typing import Optional
from datetime import datetime

class CategoryDocument(Document):
    name: Indexed(str, unique=True) # Kategori adı (örn: Action, Comedy)
    description: Optional[str] = None
    # Frontend'deki CategoryList.jsx'ten gelen ek alanlar
    icon: Optional[str] = None # Örn: "fa-bomb"
    color: Optional[str] = None # Örn: "#c2185b"

    time_created: datetime = Field(default_factory=datetime.utcnow)
    time_updated: Optional[datetime] = None

    class Settings:
        name = "categories"

    def __repr__(self) -> str:
        return f"<CategoryDocument(id={self.id}, name='{self.name}')>"