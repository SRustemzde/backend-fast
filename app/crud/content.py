# app/crud/content.py

from typing import List, Optional
from beanie import PydanticObjectId, Link
from beanie.odm.operators.update.general import Set
from beanie.odm.queries.find import FindMany # FindMany import edildi
from app.models.content import ContentDocument
from app.models.category import CategoryDocument
from app.schemas.content import ContentCreate, ContentUpdate
from datetime import datetime
# import re # Regex için şu an kullanılmıyor

async def get_content(content_id: str) -> Optional[ContentDocument]:
    return await ContentDocument.get(content_id, fetch_links=True)

async def get_content_by_source_details(source_name: str, source_id: int) -> Optional[ContentDocument]:
    return await ContentDocument.find_one(
        ContentDocument.source_name == source_name,
        ContentDocument.source_id == source_id,
        fetch_links=True
    )

async def get_contents(
    skip: int = 0,
    limit: int = 10,
    category_name: Optional[str] = None,
    content_type: Optional[str] = None,
    featured: Optional[bool] = None,
    trending: Optional[bool] = None,
    sort_by: Optional[str] = None,
    search_query: Optional[str] = None
) -> List[ContentDocument]:
    
    query_filter = {} # MongoDB sorgu filtresi için bir dictionary
    projection = None # Projeksiyon için (örn: textScore)

    if search_query:
        query_filter["$text"] = {"$search": search_query}
        # Text araması yapılıyorsa ve özel bir sıralama istenmiyorsa veya skora göre isteniyorsa
        if not sort_by or sort_by == "$textScore":
            projection = {"score": {"$meta": "textScore"}}
            sort_by_expression = [("score", {"$meta": "textScore"})] # PyMongo stili
        else: # Arama var ama farklı bir sıralama isteniyor
            sort_by_expression = None # sort_by parametresine göre aşağıda ayarlanacak
    else: # Arama yok
        sort_by_expression = None


    if content_type:
        # query_filter[ContentDocument.content_type.name] = content_type.upper() # type: ignore
        # Beanie doğrudan model alanlarını kullanmayı tercih eder
        query_filter["content_type"] = content_type.upper()
    
    if featured is not None:
        query_filter["featured"] = featured
        
    if trending is not None:
        query_filter["trending"] = trending


    # Sıralama ifadesini oluştur
    if not search_query or (search_query and sort_by and sort_by != "$textScore"): # Eğer text araması yoksa veya varsa ama farklı bir sıralama isteniyorsa
        if sort_by:
            if sort_by.startswith("-"):
                # sort_by_expression = ("-" + getattr(ContentDocument, sort_by[1:]).name) # type: ignore
                sort_by_expression = [ (sort_by[1:], -1) ] # PyMongo stili
            else:
                try:
                    # sort_by_expression = getattr(ContentDocument, sort_by).name # type: ignore
                    sort_by_expression = [ (sort_by, 1) ] # PyMongo stili
                except AttributeError:
                    sort_by_expression = None # Geçersiz sıralama alanı
        # Eğer search_query var ve sort_by $textScore değilse, MongoDB'nin doğal sıralaması ($text için) kullanılmaz.
        # Bu durumda, sort_by_expression'ı yukarıdaki gibi ayarlamak doğru olur.


    # Temel sorgu
    find_query: FindMany[ContentDocument] = ContentDocument.find(query_filter, projection_model=projection, fetch_links=True)


    if sort_by_expression:
         find_query = find_query.sort(sort_by_expression)
    
    contents = await find_query.skip(skip).limit(limit).to_list()
    
    # Kategori adına göre Python tarafında filtreleme (Link yapısı nedeniyle, fetch_links=True ile çözülmeli)
    if category_name:
        category_doc_for_filter = await CategoryDocument.find_one(CategoryDocument.name == category_name)
        if category_doc_for_filter:
            filtered_contents = []
            for content_item in contents:
                if content_item.categories: # Kategoriler populate edilmiş olmalı (Link<CategoryDocument> ise)
                    # Eğer content_item.categories List[CategoryDocument] ise (populate edilmişse)
                    for cat_doc in content_item.categories: # cat_doc artık CategoryDocument nesnesi
                        if cat_doc.name.lower() == category_name.lower():
                            filtered_contents.append(content_item)
                            break
                # Eğer categories alanı List[Link[CategoryDocument]] ise ve populate edilmemişse, ID ile karşılaştırma gerekebilir:
                # elif content_item.categories: # Kategoriler Link listesi ise
                #     for cat_link in content_item.categories:
                #         if cat_link.ref.id == category_doc_for_filter.id: # veya cat_link.id
                #             filtered_contents.append(content_item)
                #             break
            return filtered_contents
        else:
            return [] # Kategori bulunamadıysa boş liste
    
    return contents


async def create_content(content_in: ContentCreate) -> ContentDocument:
    content_data = content_in.model_dump(exclude={"category_ids"})
    current_time = datetime.utcnow()
    content_data["time_created"] = current_time
    content_data["time_updated"] = current_time

    category_docs_to_link = []
    if content_in.category_ids:
        for cat_id_str in content_in.category_ids:
            try:
                cat_object_id = PydanticObjectId(cat_id_str)
                category = await CategoryDocument.get(cat_object_id)
                if category:
                    category_docs_to_link.append(category) # Doğrudan CategoryDocument nesnesini ekle
            except Exception: 
                # Geçersiz ID formatı veya bulunamayan kategori için loglama/hata yönetimi eklenebilir
                pass 
    
    content_data["categories"] = category_docs_to_link
    
    content_doc = ContentDocument(**content_data)
    await content_doc.insert()
    # insert sonrası ilişkili verileri de içeren dökümanı döndürmek için tekrar çek
    return await get_content(str(content_doc.id))

async def update_content(content_id: str, content_in: ContentUpdate) -> Optional[ContentDocument]:
    content_doc = await ContentDocument.get(content_id)
    if not content_doc:
        return None

    update_data = content_in.model_dump(exclude_unset=True, exclude={"category_ids"})
    update_data["time_updated"] = datetime.utcnow()

    if content_in.category_ids is not None: # Eğer category_ids alanı request'te varsa (boş liste dahil)
        category_docs_to_link = []
        if content_in.category_ids: # Eğer boş liste değilse
            for cat_id_str in content_in.category_ids:
                try:
                    cat_object_id = PydanticObjectId(cat_id_str)
                    category = await CategoryDocument.get(cat_object_id)
                    if category:
                        category_docs_to_link.append(category)
                except Exception:
                    pass
        update_data["categories"] = category_docs_to_link # categories alanını tamamen güncelle
    
    # Eğer update_data boşsa ve categories alanı da güncellenmiyorsa, bir şey yapma
    if not update_data and "categories" not in update_data:
         return await get_content(content_id) # Mevcut dökümanı (linkleri çözülmüş) döndür

    await content_doc.update({"$set": update_data}) # $set operatörü ile güncelle
    return await get_content(content_id) # Güncellenmiş ve ilişkili verileri çek

async def delete_content(content_id: str) -> bool:
    content_doc = await ContentDocument.get(content_id)
    if content_doc:
        await content_doc.delete()
        return True
    return False