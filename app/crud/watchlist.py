# app/crud/watchlist.py

from typing import List, Optional
from beanie import PydanticObjectId, Link
from datetime import datetime

from app.models.watchlist import WatchlistItemDocument
from app.models.user import UserDocument
from app.models.content import ContentDocument
from app.schemas.watchlist import WatchlistItemCreate

async def get_watchlist_item(user_id: PydanticObjectId, content_id: PydanticObjectId) -> Optional[WatchlistItemDocument]:
    # Kullanıcı ve içerik Link'lerini oluşturarak sorgulama
    user_link = UserDocument.link_from_id(user_id)
    content_link = ContentDocument.link_from_id(content_id)
    return await WatchlistItemDocument.find_one(
        WatchlistItemDocument.user == user_link, # Beanie Link karşılaştırması
        WatchlistItemDocument.content == content_link,
        fetch_links=True # Content bilgisini de çek
    )

async def add_to_watchlist(user: UserDocument, content: ContentDocument) -> Optional[WatchlistItemDocument]:
    # Zaten var mı diye kontrol et (indeks sayesinde veritabanı seviyesinde de engellenir)
    existing_item = await get_watchlist_item(user.id, content.id)
    if existing_item:
        return existing_item # Varsa mevcut olanı döndür

    watchlist_item = WatchlistItemDocument(user=user, content=content) # Link'leri doğrudan model nesneleriyle oluştur
    await watchlist_item.insert()
    return await WatchlistItemDocument.get(watchlist_item.id, fetch_links=True)

async def remove_from_watchlist(user_id: PydanticObjectId, content_id: PydanticObjectId) -> bool:
    item_to_delete = await get_watchlist_item(user_id, content_id)
    if item_to_delete:
        await item_to_delete.delete()
        return True
    return False

async def get_user_watchlist(user_id: PydanticObjectId, skip: int = 0, limit: int = 100) -> List[WatchlistItemDocument]:
    user_link = UserDocument.link_from_id(user_id)
    return await WatchlistItemDocument.find(
        WatchlistItemDocument.user == user_link,
        skip=skip,
        limit=limit,
        sort="-added_at", # En son eklenenler üstte
        fetch_links=True # Content bilgisini de çek
    ).to_list()