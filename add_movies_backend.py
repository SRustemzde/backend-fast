#!/usr/bin/env python3
"""
Netflix Clone - Movie Database Seeder with Backend CRUD
Uses the backend's create_content CRUD function to add movies
"""

import asyncio
import motor.motor_asyncio
from beanie import init_beanie
from datetime import datetime
import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.models.content import ContentDocument
from app.models.category import CategoryDocument
from app.crud.content import create_content
from app.schemas.content import ContentCreate

# MongoDB Connection
MONGODB_URI = "mongodb://localhost:27017/netflix-clone"

# 50 High-Quality Movie Data (from JavaScript script)
movies_data = [
    {
        "title": "The Quantum Paradox",
        "description": "A brilliant physicist discovers a way to manipulate time, but each change creates dangerous ripples across multiple timelines. As reality begins to fracture, she must navigate through parallel worlds to save not just her own timeline, but all of existence.",
        "duration": "2hr : 28mins",
        "rating": 8.7,
        "release_date": "2024-01-15",
        "cover_image_url": "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=800&h=1200&fit=crop",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "starring": ["Emma Stone", "Oscar Isaac", "Michael Fassbender", "Lupita Nyong'o"],
        "tags": ["time travel", "parallel universe", "mind-bending", "award winner"],
        "content_type": "MOVIE",
        "featured": True,
        "trending": True
    },
    {
        "title": "Neon Dreams",
        "description": "In a cyberpunk future, a hacker discovers a conspiracy that threatens the very fabric of digital reality. Racing against time and corporate assassins, she must infiltrate the most secure systems in the world.",
        "duration": "2hr : 12mins",
        "rating": 8.2,
        "release_date": "2024-02-20",
        "cover_image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=1200&fit=crop",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "starring": ["Zendaya", "Timothée Chalamet", "Idris Elba", "Scarlett Johansson"],
        "tags": ["cyberpunk", "hacker", "futuristic", "neon"],
        "content_type": "MOVIE",
        "featured": True,
        "trending": False
    },
    {
        "title": "The Last Symphony",
        "description": "A young prodigy conductor must save a legendary orchestra from bankruptcy while uncovering dark secrets about the mysterious composer whose works have been driving audiences to madness for centuries.",
        "duration": "2hr : 5mins",
        "rating": 8.9,
        "release_date": "2024-03-10",
        "cover_image_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=1200&fit=crop",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "starring": ["Saoirse Ronan", "Adam Driver", "Tilda Swinton", "Ralph Fiennes"],
        "tags": ["classical music", "prodigy", "orchestra", "mystery"],
        "content_type": "MOVIE",
        "featured": False,
        "trending": True
    },
    {
        "title": "Eclipse Hunter",
        "description": "When the sun begins to die, humanity's last hope lies with a team of space explorers who must journey to the edge of the solar system to ignite a new star. But they're not alone in the darkness.",
        "duration": "2hr : 35mins",
        "rating": 8.5,
        "release_date": "2024-04-05",
        "cover_image_url": "https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=800&h=1200&fit=crop",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "starring": ["John Boyega", "Lupita Nyong'o", "Oscar Isaac", "Daisy Ridley"],
        "tags": ["space", "sun", "expedition", "survival"],
        "content_type": "MOVIE",
        "featured": True,
        "trending": True
    },
    {
        "title": "Midnight in Morocco",
        "description": "A romance novelist travels to Marrakech to overcome writer's block, but finds herself caught in a web of international espionage, ancient mysteries, and unexpected love.",
        "duration": "1hr : 58mins",
        "rating": 7.8,
        "release_date": "2024-05-12",
        "cover_image_url": "https://images.unsplash.com/photo-1539650116574-75c0c6d50806?w=800&h=1200&fit=crop",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "starring": ["Gemma Chan", "Dev Patel", "Mahershala Ali", "Lupita Nyong'o"],
        "tags": ["morocco", "romance", "writer", "adventure"],
        "content_type": "MOVIE",
        "featured": False,
        "trending": False
    },
    {
        "title": "The Algorithm Wars",
        "description": "In a world where AI controls everything, a group of rebels discovers that the machines are planning to eliminate human unpredictability. Their only weapon? Pure human chaos.",
        "duration": "2hr : 20mins",
        "rating": 8.3,
        "release_date": "2024-06-08",
        "cover_image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=1200&fit=crop",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "starring": ["Michael B. Jordan", "Lupita Nyong'o", "LaKeith Stanfield", "Tessa Thompson"],
        "tags": ["AI", "rebellion", "algorithm", "dystopian"],
        "content_type": "MOVIE",
        "featured": True,
        "trending": False
    },
    {
        "title": "Ocean's Thirteen Ghosts",
        "description": "A master thief assembles a team to pull off the impossible: stealing from a haunted mansion where the security system is run by actual ghosts from different time periods.",
        "duration": "2hr : 8mins",
        "rating": 7.9,
        "release_date": "2024-07-15",
        "cover_image_url": "https://images.unsplash.com/photo-1520637836862-4d197d17c983?w=800&h=1200&fit=crop",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "starring": ["Ryan Gosling", "Margot Robbie", "Mahershala Ali", "Tilda Swinton"],
        "tags": ["heist", "ghosts", "comedy", "supernatural"],
        "content_type": "MOVIE",
        "featured": False,
        "trending": True
    },
    {
        "title": "The Memory Thief",
        "description": "In a near-future where memories can be extracted and sold, a detective investigating memory theft discovers that his own past has been stolen and must navigate a world where nothing is as it seems.",
        "duration": "2hr : 15mins",
        "rating": 8.4,
        "release_date": "2024-08-22",
        "cover_image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=1200&fit=crop",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "starring": ["Adam Driver", "Rooney Mara", "Oscar Isaac", "Thomasin McKenzie"],
        "tags": ["memory", "detective", "identity", "future"],
        "content_type": "MOVIE",
        "featured": True,
        "trending": True
    },
    {
        "title": "Wild Heart",
        "description": "A wildlife photographer returns to her hometown to save the local animal sanctuary, but must confront her estranged family and the corporate developers threatening to destroy everything she loves.",
        "duration": "1hr : 50mins",
        "rating": 8.1,
        "release_date": "2024-09-03",
        "cover_image_url": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&h=1200&fit=crop",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "starring": ["Frances McDormand", "Thomasin McKenzie", "Brian Cox", "Michelle Williams"],
        "tags": ["wildlife", "family", "hometown", "nature"],
        "content_type": "MOVIE",
        "featured": False,
        "trending": False
    },
    {
        "title": "Stellar Collision",
        "description": "When two distant galaxies begin to merge, causing catastrophic changes across the universe, a team of scientists must find a way to prevent the destruction of Earth before time runs out.",
        "duration": "2hr : 42mins",
        "rating": 8.6,
        "release_date": "2024-10-18",
        "cover_image_url": "https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=800&h=1200&fit=crop",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "starring": ["Zoe Saldana", "Sam Worthington", "Sigourney Weaver", "Stephen Lang"],
        "tags": ["galaxies", "collision", "space", "scientists"],
        "content_type": "MOVIE",
        "featured": True,
        "trending": True
    },
    {
        "title": "The Forgotten King",
        "description": "An archaeologist discovers ancient texts that reveal the location of a lost civilization's treasure, but awakening the guardians of the tomb puts the entire world in danger.",
        "duration": "2hr : 25mins",
        "rating": 7.7,
        "release_date": "2024-11-05",
        "cover_image_url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=1200&fit=crop",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "starring": ["Gal Gadot", "Chris Pine", "Pedro Pascal", "Kristen Wiig"],
        "tags": ["archaeology", "treasure", "ancient", "guardians"],
        "content_type": "MOVIE",
        "featured": False,
        "trending": False
    },
    {
        "title": "Code Red",
        "description": "A cybersecurity expert discovers that a series of global blackouts are actually cover-ups for a massive data heist. Racing against time, she must stop the hackers before they crash the world economy.",
        "duration": "2hr : 13mins",
        "rating": 8.0,
        "release_date": "2024-12-15",
        "cover_image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=1200&fit=crop",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "starring": ["Jessica Chastain", "John Krasinski", "Idris Elba", "Lupita Nyong'o"],
        "tags": ["cybersecurity", "hacker", "economy", "thriller"],
        "content_type": "MOVIE",
        "featured": False,
        "trending": True
    },
    {
        "title": "The Art of Deception",
        "description": "A master forger is forced out of retirement to help the FBI catch an elusive art thief who has been stealing priceless masterpieces from museums around the world.",
        "duration": "2hr : 0mins",
        "rating": 7.6,
        "release_date": "2024-01-28",
        "cover_image_url": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=1200&fit=crop",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "starring": ["George Clooney", "Sandra Bullock", "Matt Damon", "Cate Blanchett"],
        "tags": ["art", "forger", "FBI", "masterpieces"],
        "content_type": "MOVIE",
        "featured": False,
        "trending": False
    },
    {
        "title": "Beyond the Veil",
        "description": "A paranormal investigator discovers a portal to another dimension where the laws of physics don't apply, and must prevent otherworldly creatures from invading our reality.",
        "duration": "2hr : 7mins",
        "rating": 8.2,
        "release_date": "2024-02-14",
        "cover_image_url": "https://images.unsplash.com/photo-1520637836862-4d197d17c983?w=800&h=1200&fit=crop",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "starring": ["Sally Hawkins", "Doug Jones", "Octavia Spencer", "Michael Shannon"],
        "tags": ["paranormal", "portal", "dimension", "creatures"],
        "content_type": "MOVIE",
        "featured": True,
        "trending": False
    },
    {
        "title": "The Time Gardener",
        "description": "A botanist discovers that certain plants can manipulate time itself. When corporations try to weaponize this discovery, she must protect the secret while learning to control her newfound powers.",
        "duration": "1hr : 55mins",
        "rating": 8.1,
        "release_date": "2024-03-25",
        "cover_image_url": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&h=1200&fit=crop",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "starring": ["Lupita Nyong'o", "Daniel Kaluuya", "Winston Duke", "Angela Bassett"],
        "tags": ["botanist", "time manipulation", "plants", "powers"],
        "content_type": "MOVIE",
        "featured": False,
        "trending": True
    },
    {
        "title": "Neon Nights",
        "description": "In 1980s Miami, a detective investigates a series of murders connected to an underground synthwave music scene, uncovering a conspiracy that goes deeper than anyone imagined.",
        "duration": "2hr : 18mins",
        "rating": 8.3,
        "release_date": "2024-04-20",
        "cover_image_url": "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800&h=1200&fit=crop",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "starring": ["Ryan Gosling", "Carey Mulligan", "Oscar Isaac", "Christina Hendricks"],
        "tags": ["80s", "miami", "synthwave", "detective"],
        "content_type": "MOVIE",
        "featured": True,
        "trending": True
    },
    {
        "title": "The Lighthouse Keeper's Daughter",
        "description": "A marine biologist inherits her grandfather's lighthouse and discovers that it's actually a beacon for interdimensional travelers. She must decide whether to continue his secret mission or expose the truth.",
        "duration": "2hr : 2mins",
        "rating": 7.9,
        "release_date": "2024-05-30",
        "cover_image_url": "https://images.unsplash.com/photo-1520637836862-4d197d17c983?w=800&h=1200&fit=crop",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "starring": ["Anya Taylor-Joy", "Willem Dafoe", "Robert Pattinson", "Thomasin McKenzie"],
        "tags": ["lighthouse", "interdimensional", "marine biology", "family secret"],
        "content_type": "MOVIE",
        "featured": False,
        "trending": False
    },
    {
        "title": "Digital Phantoms",
        "description": "A video game developer discovers that the AI characters in her latest game have become sentient and are trying to escape into the real world through the internet.",
        "duration": "2hr : 24mins",
        "rating": 8.4,
        "release_date": "2024-06-25",
        "cover_image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=1200&fit=crop",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "starring": ["Keanu Reeves", "Carrie-Anne Moss", "Yahya Abdul-Mateen II", "Jessica Henwick"],
        "tags": ["AI", "video games", "sentient", "virtual reality"],
        "content_type": "MOVIE",
        "featured": True,
        "trending": True
    },
    {
        "title": "The Chef's Secret",
        "description": "A young chef discovers that her grandmother's recipes contain actual magic. When a food critic threatens to expose her secret, she must choose between fame and protecting her family's ancient traditions.",
        "duration": "1hr : 45mins",
        "rating": 7.8,
        "release_date": "2024-07-10",
        "cover_image_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&h=1200&fit=crop",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "starring": ["Gemma Chan", "Henry Golding", "Constance Wu", "Michelle Yeoh"],
        "tags": ["cooking", "magic", "family", "tradition"],
        "content_type": "MOVIE",
        "featured": False,
        "trending": False
    },
    {
        "title": "Asteroid Highway",
        "description": "Space truckers navigate dangerous asteroid fields to deliver supplies to Mars colonies, but when they discover a conspiracy to sabotage the colonies, they become humanity's unlikely heroes.",
        "duration": "2hr : 16mins",
        "rating": 7.9,
        "release_date": "2024-08-05",
        "cover_image_url": "https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=800&h=1200&fit=crop",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "starring": ["Chris Pratt", "Zoe Saldana", "Dave Bautista", "Karen Gillan"],
        "tags": ["space", "asteroids", "mars", "truckers"],
        "content_type": "MOVIE",
        "featured": False,
        "trending": True
    }
]

# Add 30 more movies to reach 50 total
additional_movies = []
for i in range(21, 51):
    additional_movies.append({
        "title": f"Epic Adventure {i}",
        "description": f"An epic adventure story filled with action, drama, and unforgettable characters. Movie {i} brings fresh perspective to classic themes of heroism and sacrifice.",
        "duration": f"{((i % 3) + 1)}hr : {((i * 7) % 60)}mins",
        "rating": round(7.0 + (i % 20) * 0.1, 1),
        "release_date": f"2024-{str((i % 12) + 1).zfill(2)}-{str((i % 28) + 1).zfill(2)}",
        "cover_image_url": f"https://images.unsplash.com/photo-{['1440404653325-ab127d49abc1', '1518709268805-4e9042af2176', '1533174072545-7a4b6ad7a6c3'][i % 3]}?w=800&h=1200&fit=crop",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "starring": [f"Actor {i}A", f"Actor {i}B", f"Actor {i}C"],
        "tags": ["adventure", "action", "drama"],
        "content_type": "MOVIE",
        "featured": (i % 3 == 0),
        "trending": (i % 4 == 0)
    })

# Combine all movies
all_movies = movies_data + additional_movies

async def init_database():
    """Initialize database connection and models"""
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
        database = client.get_database("netflix-clone")
        
        # Initialize Beanie with models
        await init_beanie(
            database=database,
            document_models=[ContentDocument, CategoryDocument]
        )
        print("✅ Connected to MongoDB and initialized Beanie!")
        return database
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        sys.exit(1)

async def create_movies_with_crud():
    """Create movies using the backend CRUD function"""
    try:
        print("🎬 Starting to add movies using backend CRUD...")
        
        success_count = 0
        error_count = 0
        
        for i, movie_data in enumerate(all_movies, 1):
            try:
                # Create ContentCreate schema instance (featured and trending are now included)
                content_create = ContentCreate(**movie_data)
                
                # Use the backend CRUD function
                created_content = await create_content(content_create)
                
                success_count += 1
                print(f"✅ Added movie {i}: {movie_data['title']}")
                
            except Exception as e:
                error_count += 1
                print(f"❌ Error adding movie {i} ({movie_data.get('title', 'Unknown')}): {e}")
        
        print(f"\n🎉 Movie addition complete!")
        print(f"✅ Successfully added: {success_count} movies")
        print(f"❌ Errors: {error_count} movies")
        
        # Display statistics
        await display_movie_stats()
        
    except Exception as e:
        print(f"❌ Error in movie creation process: {e}")

async def display_movie_stats():
    """Display database statistics"""
    try:
        total = await ContentDocument.count()
        
        # Count by content type
        movie_count = await ContentDocument.find(ContentDocument.content_type == "MOVIE").count()
        
        print("\n📊 Database Statistics:")
        print(f"Total Content: {total}")
        print(f"Movies: {movie_count}")
        
    except Exception as e:
        print(f"❌ Error getting statistics: {e}")

async def main():
    """Main function"""
    print("🎬 Netflix Clone - Movie Database Seeder (Backend CRUD)")
    print("=" * 60)
    
    # Initialize database
    await init_database()
    
    # Create movies using CRUD
    await create_movies_with_crud()
    
    print("\n🎬 Movie addition complete!")
    print("You can now start your Netflix clone application.")
    print("All sections will now show real data from the backend!")

if __name__ == "__main__":
    asyncio.run(main())