# app/routers/users_interactions.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from beanie import PydanticObjectId

from app.dependencies import get_current_user # Bu satır eklendi veya güncellendi (get_current_active_user yerine)
from app.schemas.user import UserPublic # Bu zaten vardı, ama current_user için UserDocument kullanacağız
from app.schemas.watchlist import WatchlistItemCreate, WatchlistItemPublic
from app.schemas.watch_history import WatchHistoryItemCreateOrUpdate, WatchHistoryItemPublic
from app.crud import watchlist as crud_watchlist
from app.crud import watch_history as crud_watch_history
from app.crud import content as crud_content # İçerik var mı diye kontrol için
from app.models.user import UserDocument # current_user_doc'un tipini belirtmek için

router = APIRouter(
    prefix="/users/me",
    tags=["User Interactions"]
)

# --- Watchlist Endpoints ---
@router.post("/watchlist", response_model=WatchlistItemPublic, status_code=status.HTTP_201_CREATED)
async def add_item_to_my_watchlist(
    item_in: WatchlistItemCreate,
    current_user_doc: UserDocument = Depends(get_current_user) # Artık get_current_user import edildi
):
    content_doc = await crud_content.get_content(item_in.content_id)
    if not content_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found to add to watchlist")
    
    watchlist_item = await crud_watchlist.add_to_watchlist(user=current_user_doc, content=content_doc)
    if not watchlist_item:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not add item to watchlist")

    # WatchlistItemPublic'e dönüşüm için content alanının doğru maplendiğinden emin olalım.
    # crud_watchlist.add_to_watchlist zaten fetch_links=True ile dönüyor,
    # bu yüzden watchlist_item.content bir ContentDocument olmalı.
    # ContentPublicShort şeması, ContentDocument'tan alanları alabilmeli.
    return WatchlistItemPublic(
        id=str(watchlist_item.id),
        user_id=str(current_user_doc.id),
        content=watchlist_item.content, # Bu, Pydantic tarafından ContentPublicShort'a maplenecek
        added_at=watchlist_item.added_at
    )

@router.get("/watchlist", response_model=List[WatchlistItemPublic])
async def read_my_watchlist(
    skip: int = 0,
    limit: int = 20,
    current_user_doc: UserDocument = Depends(get_current_user)
):
    watchlist_items_db = await crud_watchlist.get_user_watchlist(user_id=current_user_doc.id, skip=skip, limit=limit)
    
    response_items = []
    for item_db in watchlist_items_db:
        # item_db.content bir ContentDocument nesnesi olmalı (fetch_links=True sayesinde)
        response_items.append(
            WatchlistItemPublic(
                id=str(item_db.id),
                user_id=str(current_user_doc.id),
                content=item_db.content, # Pydantic, ContentDocument'ı ContentPublicShort'a mapleyecek
                added_at=item_db.added_at
            )
        )
    return response_items

@router.delete("/watchlist/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_item_from_my_watchlist(
    content_id: str, # content_id'yi string olarak alalım
    current_user_doc: UserDocument = Depends(get_current_user)
):
    try:
        # String ID'yi PydanticObjectId'ye çevirmeye gerek yok eğer CRUD fonksiyonu string kabul ediyorsa.
        # Ancak, içeriğin varlığını kontrol ederken string ID kullanabiliriz.
        content_object_id_for_check = PydanticObjectId(content_id) # Bu satır Beanie'nin ObjectId beklentisi için
    except Exception: # pydantic.errors.PydanticCustomError veya ValueError olabilir
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid content ID format")

    # İçeriğin varlığını kontrol et
    # content_doc = await crud_content.get_content(content_id) # crud_content.get_content string ID bekliyor
    # if not content_doc:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found, cannot remove from watchlist")
    # Bu kontrol aslında CRUD içinde (get_watchlist_item) zaten dolaylı olarak yapılıyor.
    # Eğer content_id geçerli bir ObjectId değilse veya o ID'li içerik yoksa get_watchlist_item None döner.

    deleted = await crud_watchlist.remove_from_watchlist(user_id=current_user_doc.id, content_id=content_object_id_for_check)
    if not deleted:
        # Bu, ya içerik watchlist'te değildi ya da bir sorun oluştu anlamına gelir.
        # get_watchlist_item None döndüğünde zaten false dönecek.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found in watchlist or content does not exist")
    return None

# --- Watch History Endpoints ---
@router.post("/watch-history", response_model=WatchHistoryItemPublic, status_code=status.HTTP_200_OK)
async def add_or_update_my_watch_history(
    item_in: WatchHistoryItemCreateOrUpdate,
    current_user_doc: UserDocument = Depends(get_current_user)
):
    content_doc = await crud_content.get_content(item_in.content_id)
    if not content_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found to add to history")
    
    history_item = await crud_watch_history.add_or_update_watch_history(
        user=current_user_doc, 
        content=content_doc, 
        progress_percentage=item_in.progress_percentage
    )
    if not history_item:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not update watch history")

    return WatchHistoryItemPublic(
        id=str(history_item.id),
        user_id=str(current_user_doc.id),
        content=history_item.content,
        progress_percentage=history_item.progress_percentage,
        watched_at=history_item.watched_at,
        last_watched_at=history_item.last_watched_at
    )

@router.get("/watch-history", response_model=List[WatchHistoryItemPublic])
async def read_my_watch_history(
    skip: int = 0,
    limit: int = 20,
    current_user_doc: UserDocument = Depends(get_current_user)
):
    history_items_db = await crud_watch_history.get_user_watch_history(user_id=current_user_doc.id, skip=skip, limit=limit)
    
    response_items = []
    for item_db in history_items_db:
        response_items.append(
             WatchHistoryItemPublic(
                id=str(item_db.id),
                user_id=str(current_user_doc.id),
                content=item_db.content,
                progress_percentage=item_db.progress_percentage,
                watched_at=item_db.watched_at,
                last_watched_at=item_db.last_watched_at
            )
        )
    return response_items

@router.delete("/watch-history/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_item_from_my_watch_history(
    content_id: str, # content_id'yi string olarak alalım
    current_user_doc: UserDocument = Depends(get_current_user)
):
    try:
        content_object_id_for_check = PydanticObjectId(content_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid content ID format")

    # content_doc = await crud_content.get_content(content_id)
    # if not content_doc:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found, cannot remove from history")
    # Bu kontrol de CRUD içinde dolaylı olarak var.

    deleted = await crud_watch_history.remove_from_watch_history(user_id=current_user_doc.id, content_id=content_object_id_for_check)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found in watch history or content does not exist")
    return None