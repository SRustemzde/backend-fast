# app/models/__init__.py

from typing import List, Type
from pydantic import BaseModel # Veya Beanie Document

from .user import UserDocument
from .category import CategoryDocument
from .content import ContentDocument
from .watchlist import WatchlistItemDocument # Yeni
from .watch_history import WatchHistoryItemDocument # Yeni

def get_document_models() -> List[Type[BaseModel]]:
    models = [
        UserDocument,
        CategoryDocument,
        ContentDocument,
        WatchlistItemDocument,      # Eklendi
        WatchHistoryItemDocument,   # Eklendi
    ]
    return models