# app/crud/watch_history.py

from typing import List, Optional
from beanie import PydanticObjectId, Link
from beanie.odm.operators.update.general import Set
from datetime import datetime

from app.models.watch_history import WatchHistoryItemDocument
from app.models.user import UserDocument
from app.models.content import ContentDocument
from app.schemas.watch_history import WatchHistoryItemCreateOrUpdate

async def get_watch_history_item(user_id: PydanticObjectId, content_id: PydanticObjectId) -> Optional[WatchHistoryItemDocument]:
    user_link = UserDocument.link_from_id(user_id)
    content_link = ContentDocument.link_from_id(content_id)
    return await WatchHistoryItemDocument.find_one(
        WatchHistoryItemDocument.user == user_link,
        WatchHistoryItemDocument.content == content_link,
        fetch_links=True
    )

async def add_or_update_watch_history(
    user: UserDocument, 
    content: ContentDocument, 
    progress_percentage: int
) -> WatchHistoryItemDocument:
    existing_item = await get_watch_history_item(user.id, content.id)
    current_time = datetime.utcnow()

    if existing_item:
        # Var olanı güncelle
        await existing_item.update(
            Set({
                WatchHistoryItemDocument.progress_percentage: progress_percentage,
                WatchHistoryItemDocument.last_watched_at: current_time
            })
        )
        # Güncellenmiş dökümanı fetch_links ile tekrar çek
        return await WatchHistoryItemDocument.get(existing_item.id, fetch_links=True)
    else:
        # Yeni oluştur
        history_item = WatchHistoryItemDocument(
            user=user, 
            content=content,
            progress_percentage=progress_percentage,
            watched_at=current_time, # İlk izlenme
            last_watched_at=current_time # Son izlenme (ilk izlenmeyle aynı)
        )
        await history_item.insert()
        return await WatchHistoryItemDocument.get(history_item.id, fetch_links=True)


async def remove_from_watch_history(user_id: PydanticObjectId, content_id: PydanticObjectId) -> bool:
    item_to_delete = await get_watch_history_item(user_id, content_id)
    if item_to_delete:
        await item_to_delete.delete()
        return True
    return False

async def get_user_watch_history(user_id: PydanticObjectId, skip: int = 0, limit: int = 100) -> List[WatchHistoryItemDocument]:
    user_link = UserDocument.link_from_id(user_id)
    return await WatchHistoryItemDocument.find(
        WatchHistoryItemDocument.user == user_link,
        skip=skip,
        limit=limit,
        sort="-last_watched_at", # En son izlenenler üstte
        fetch_links=True
    ).to_list()