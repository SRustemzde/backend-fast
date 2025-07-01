# backend_fastapi/seed_db.py

import asyncio
from beanie import PydanticObjectId, init_beanie # init_beanie import edildi
from motor.motor_asyncio import AsyncIOMotorClient

# App modüllerini import et
from app.core.config import settings # Ayarları settings objesi üzerinden kullanacağız
from app.models import get_document_models # Tüm Beanie modellerini almak için
    
from app.models.category import CategoryDocument
from app.models.content import ContentDocument
from app.models.user import UserDocument
    
from app.utils.security import get_password_hash # Admin şifresini hashlemek için

# --- DUMMY DATA (Python Formatında) ---
# Not: Resim ve video URL'leri placeholder olarak bırakılmıştır.
# Gerçek URL'lerle değiştirilmeli veya statik dosya sunumu/CDN ayarlanmalıdır.

dummy_home_data = [
    {
        "id": 1, "name": "Casino Royale", "rating": 8.4, "time": "2hr : 24mins",
        "desc": "Casino Royale is a 2006 spy film, the twenty-first in the Eon Productions James Bond series...",
        "starring": ["Daniel Craig", "Eva Green", "Mads Mikkelsen"], # Liste olarak
        "genres": "Action", "tags": ["Action", "Adventures"], # Liste olarak
        "cover": "https://via.placeholder.com/300x450.png?text=Casino+Royale",
        "video": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4",
        "date": "16-Nov-2006", "source_name": "homeData", "source_id": 1 # source_id ve source_name eklendi
    },
    {
        "id": 2, "name": "The Godfather", "rating": 9.2, "time": "2hr : 55mins",
        "desc": "The Godfather is a 1972 American crime film directed by Francis Ford Coppola...",
        "starring": ["Marlon Brando", "Al Pacino", "James Caan"],
        "genres": "Crime, Drama", "tags": ["Crime", "Drama", "Mafia"],
        "cover": "https://via.placeholder.com/300x450.png?text=The+Godfather",
        "video": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4",
        "date": "24-Mar-1972", "source_name": "homeData", "source_id": 2
    },
    {
        "id": 3, "name": "John Wick", "rating": 7.4, "time": "1hr : 41mins",
        "desc": "John Wick is a 2014 American neo-noir action thriller film directed by Chad Stahelski...",
        "starring": ["Keanu Reeves", "Michael Nyqvist", "Willem Dafoe"],
        "genres": "Action, Thriller", "tags": ["Action", "Crime", "Thriller"],
        "cover": "https://via.placeholder.com/300x450.png?text=John+Wick",
        "video": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4",
        "date": "24-Oct-2014", "source_name": "homeData", "source_id": 3
    },
    {
        "id": 4, "name": "No Time to Die", "rating": 7.3, "time": "2hr : 43mins",
        "desc": "No Time to Die is a 2021 spy film and the twenty-fifth installment in the James Bond series...",
        "starring": ["Daniel Craig", "Rami Malek", "Léa Seydoux"],
        "genres": "Action, Adventure, Thriller", "tags": ["Action", "Adventure", "Spy"],
        "cover": "https://via.placeholder.com/300x450.png?text=No+Time+to+Die",
        "video": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4",
        "date": "30-Sep-2021", "source_name": "homeData", "source_id": 4
    },
]

dummy_upcome_data = [
    {"id": 1, "cover": "https://via.placeholder.com/300x450.png?text=Daredevil", "name": "Daredevil: Born Again", "time": "2hr : 45mins", "video": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4", "genres": "Action, Crime", "source_name": "upcome", "source_id": 1, "tags": ["Superhero", "Marvel"]},
    {"id": 2, "cover": "https://via.placeholder.com/300x450.png?text=Esref+Ruya", "name": "Esref Ruya", "time": "2hr : 20mins", "video": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4", "genres": "Drama", "source_name": "upcome", "source_id": 2, "tags": ["Turkish", "Drama"]},
    # Diğer upcome verileri eklenebilir...
]

dummy_latest_data = [
    {"id": 1, "cover": "https://via.placeholder.com/300x450.png?text=Mandalorian", "name": "The Mandalorian", "time": "2hr : 25mins", "video": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4", "genres": "Action, Sci-Fi", "source_name": "latest", "source_id": 1, "tags": ["Star Wars", "Space"]},
    {"id": 2, "cover": "https://via.placeholder.com/300x450.png?text=Transporter", "name": "Transporter", "time": "1hr : 45mins", "video": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4", "genres": "Action, Thriller", "source_name": "latest", "source_id": 2, "tags": ["Action", "Jason Statham"]},
    # Diğer latest verileri eklenebilir...
]

dummy_trending_data = [
    {"id": 1, "name": "Central Intelligence", "rating": 4.7, "time": "1hr : 47mins", "desc": "A lethal CIA agent and his former schoolmate encounter shootouts, espionage and double-crosses while on a top-secret case.", "starring": ["Dwayne Johnson", "Kevin Hart"], "genres": "Action, Comedy", "tags": ["Action", "Comedy", "Spy"], "cover": "https://via.placeholder.com/300x450.png?text=Central+Intel", "date": "17-Jun-2016", "video": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4", "source_name": "trending", "source_id": 1},
    {"id": 2, "name": "Scent of a Woman", "rating": 4.9, "time": "2hr : 37mins", "desc": "A prep school student needing money agrees to 'babysit' a blind man, but the job is not at all what he anticipated.", "starring": ["Al Pacino", "Chris O'Donnell"], "genres": "Drama", "tags": ["Drama", "Classic"], "cover": "https://via.placeholder.com/300x450.png?text=Scent+of+Woman", "date": "23-Dec-1992", "video": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4", "source_name": "trending", "source_id": 2},
    # Diğer trending verileri eklenebilir...
]

dummy_recommended_data = [
    {"id": 1, "cover": "https://via.placeholder.com/300x450.png?text=Matrix", "name": "The Matrix", "time": "2hr : 16mins", "video": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4", "genres": "Action, Sci-Fi", "source_name": "recommended", "source_id": 1, "tags": ["Cyberpunk", "Keanu Reeves"]},
    # Diğer recommended verileri eklenebilir...
]

dummy_documentaries_data = [
    {"id": 1, "cover": "https://via.placeholder.com/300x450.png?text=Grizzly+Man", "name": "Grizzly Man", "time": "1hr : 43mins", "video": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4", "genres": "Documentary", "source_name": "documentaries", "source_id": 1, "tags": ["Nature", "Biography"]},
    # Diğer documentary verileri eklenebilir...
]

dummy_animation_data = [
    {"id": 1, "cover": "https://via.placeholder.com/300x450.png?text=Tom+Jerry", "name": "Tom & Jerry", "time": "1hr : 41mins", "video": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4", "genres": "Animation, Comedy", "source_name": "animation", "source_id": 1, "tags": ["Kids", "Classic Cartoons"]},
    # Diğer animation verileri eklenebilir...
]

all_dummy_content_sources = {
    "homeData": dummy_home_data,
    "upcome": dummy_upcome_data,
    "latest": dummy_latest_data,
    "trending": dummy_trending_data,
    "recommended": dummy_recommended_data,
    "documentaries": dummy_documentaries_data,
    "animation": dummy_animation_data,
}

async def clear_collections():
    print("Clearing existing collections (CategoryDocument, ContentDocument)...")
    # Önce tüm içerikleri sil (kategori referansları nedeniyle)
    await ContentDocument.delete_all()
    await CategoryDocument.delete_all()
    # UserDocument.delete_all() # Kullanıcıları genellikle silmek istemeyiz
    print("Relevant collections cleared.")

async def seed_categories():
    print("Seeding categories...")
    categories_in_db_map = {} # name: CategoryDocument objesi
    
    all_genre_names_from_dummy = set()
    for source_list in all_dummy_content_sources.values():
        for item_data in source_list:
            if item_data.get("genres"):
                # genres string ise (örn: "Action, Comedy") listeye çevir
                if isinstance(item_data["genres"], str):
                    genres_list = [g.strip() for g in item_data["genres"].split(',')]
                elif isinstance(item_data["genres"], list): # Zaten liste ise
                    genres_list = item_data["genres"]
                else:
                    genres_list = []
                
                for genre_name in genres_list:
                    if genre_name: # Boş stringleri atla
                        all_genre_names_from_dummy.add(genre_name)
    
    # Frontend'den gelen veya varsayılan kategorileri de ekleyelim
    default_category_names = [
        "Action", "Comedy", "Drama", "SciFi", "Romance", 
        "Documentary", "Cartoon", "Animation", "Thriller", "Crime", "Adventure", "Fantasy", "Horror", "Mystery", "Family"
    ]
    for cat_name in default_category_names:
        all_genre_names_from_dummy.add(cat_name)
        
    for genre_name in sorted(list(all_genre_names_from_dummy)):
        existing_category = await CategoryDocument.find_one(CategoryDocument.name == genre_name)
        if not existing_category:
            # Frontend'deki CategoryList.jsx'ten icon ve color bilgileri alınabilir (opsiyonel)
            # Örnek: category_icons = {"Action": "fa-bomb", "Comedy": "fa-laugh"}
            category_doc = CategoryDocument(name=genre_name, description=f"Content in the {genre_name} genre.")
            await category_doc.insert()
            categories_in_db_map[genre_name] = category_doc
            print(f"  Created category: {genre_name}")
        else:
            categories_in_db_map[genre_name] = existing_category
            print(f"  Category '{genre_name}' already exists. Using existing.")
    print("Categories seeded.")
    return categories_in_db_map

async def seed_content(seeded_categories_map: dict):
    print("Seeding content...")
    content_count = 0
    for source_key_name, source_list_data in all_dummy_content_sources.items():
        for item_data in source_list_data:
            # Benzersizliği source_name ve source_id üzerinden kontrol et
            unique_content_identifier = f"{item_data['source_name']}_{item_data['source_id']}"
            existing_content = await ContentDocument.find_one(
                ContentDocument.source_name == item_data["source_name"],
                ContentDocument.source_id == item_data["source_id"]
            )
            if existing_content:
                print(f"  Content '{item_data['name']}' (ID: {unique_content_identifier}) already exists. Skipping.")
                continue

            content_linked_categories = []
            if item_data.get("genres"):
                if isinstance(item_data["genres"], str):
                    genres_list = [g.strip() for g in item_data["genres"].split(',')]
                elif isinstance(item_data["genres"], list):
                    genres_list = item_data["genres"]
                else:
                    genres_list = []
                
                for genre_name in genres_list:
                    if genre_name and genre_name in seeded_categories_map:
                        # Modeldeki categories alanı List[Link[CategoryDocument]] olduğu için
                        # doğrudan CategoryDocument nesnesini atayabiliriz, Beanie Link'e çevirir.
                        content_linked_categories.append(seeded_categories_map[genre_name])
            
            starring_list = []
            if isinstance(item_data.get("starring"), str):
                starring_list = [s.strip() for s in item_data["starring"].split(',') if s.strip()]
            elif isinstance(item_data.get("starring"), list):
                starring_list = [s.strip() for s in item_data["starring"] if isinstance(s, str) and s.strip()]

            tags_list = []
            if isinstance(item_data.get("tags"), str):
                tags_list = [t.strip() for t in item_data["tags"].split(',') if t.strip()]
            elif isinstance(item_data.get("tags"), list):
                tags_list = [t.strip() for t in item_data["tags"] if isinstance(t, str) and t.strip()]

            content_doc_data = {
                "title": item_data["name"],
                "description": item_data.get("desc"),
                "release_date": item_data.get("date"),
                "duration": item_data.get("time"),
                "rating": item_data.get("rating"),
                "cover_image_url": item_data.get("cover") if item_data.get("cover") else "https://via.placeholder.com/300x450.png?text=No+Cover",
                "video_url": item_data.get("video") if item_data.get("video") else "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4",
                "starring": starring_list,
                "tags": tags_list,
                "content_type": "MOVIE", # Varsayılan, gerekirse TV_SHOW olarak ayarla
                "categories": content_linked_categories, # Doğrudan CategoryDocument listesi
                "source_id": item_data.get("source_id"),
                "source_name": item_data.get("source_name"),
            }
            
            content_doc = ContentDocument(**content_doc_data)
            await content_doc.insert()
            content_count += 1
            print(f"  Created content: {item_data['name']} (ID: {unique_content_identifier})")
    print(f"{content_count} content items seeded.")

async def create_default_admin_user():
    print("Checking/Creating default admin user...")
    # .env dosyasından admin bilgilerini al
    admin_email = settings.ADMIN_EMAIL
    admin_password = settings.ADMIN_PASSWORD

    if not admin_email or not admin_password:
        print("  ADMIN_EMAIL or ADMIN_PASSWORD not set in .env. Skipping admin user creation.")
        print("  Please add ADMIN_EMAIL and ADMIN_PASSWORD to your .env file.")
        return

    admin_user = await UserDocument.find_one(UserDocument.email == admin_email)
    if not admin_user:
        hashed_password = get_password_hash(admin_password)
        admin_user_doc = UserDocument(
            email=admin_email,
            hashed_password=hashed_password,
            full_name="Admin User",
            is_active=True,
            is_superuser=True
        )
        await admin_user_doc.insert()
        print(f"  Default admin user created with email: {admin_email}")
        print(f"  IMPORTANT: Use password '{admin_password}' to login as admin.")
    else:
        updated_admin = False
        update_payload = {}
        if not admin_user.is_superuser:
            update_payload["is_superuser"] = True
            updated_admin = True
        if not admin_user.is_active:
             update_payload["is_active"] = True
             updated_admin = True
        
        if updated_admin:
            await admin_user.update({"$set": update_payload})
            print(f"  Admin user '{admin_email}' found and ensured superuser & active status.")
        else:
            print(f"  Admin user '{admin_email}' already exists and is correctly configured.")


async def main_seed():
    mongo_client = None # client'ı dışarıda tanımla, FastAPI'dekiyle karışmasın
    try:
        print(f"Attempting to connect to MongoDB: {settings.MONGO_CONNECTION_STRING}")
        mongo_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
        # Bağlantıyı test et
        await mongo_client.admin.command('ping') 
        print("Successfully connected to MongoDB for seeding!")
        
        # Beanie'yi başlat
        # init_db fonksiyonunu app.core.db'den çağırmak yerine burada direkt init_beanie kullanıyoruz
        # çünkü bu bir standalone script.
        all_models_to_init = get_document_models()
        await init_beanie(
            database=mongo_client[settings.MONGO_DB_NAME], # Veritabanı adını settings'den al
            document_models=all_models_to_init
        )
        print(f"Beanie initialized for seeding with database: {settings.MONGO_DB_NAME} and models: {[m.__name__ for m in all_models_to_init]}")

        # Veritabanını temizle (isteğe bağlı, dikkatli kullanın!)
        # await clear_collections() 

        await create_default_admin_user()
        seeded_categories_map = await seed_categories()
        await seed_content(seeded_categories_map)
        
        print("\n------------------------------------")
        print("Database seeding process complete!")
        print("------------------------------------")

    except Exception as e:
        print(f"XXXXXXXX An error occurred during seeding XXXXXXXX: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if mongo_client:
            mongo_client.close() # PyMongo client'ını kapat, motor async client için close()
            print("MongoDB connection closed after seeding.")


if __name__ == "__main__":
    print("====================================")
    print("Starting Database Seed Script...")
    print("Make sure your MongoDB server is running.")
    print("Ensure ADMIN_EMAIL and ADMIN_PASSWORD are set in your .env file.")
    print("====================================")
    
    asyncio.run(main_seed())