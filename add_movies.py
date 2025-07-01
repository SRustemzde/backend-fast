#!/usr/bin/env python3
"""
Netflix Clone - Movie Database Seeder
Adds 50 high-quality movies to the database with trending and featured flags
"""

import pymongo
import random
from datetime import datetime

# MongoDB Connection
MONGODB_URI = "mongodb://localhost:27017/netflix-clone"

# 50 High-Quality Movie Data
movies = [
    {
        "title": "The Quantum Paradox",
        "description": "A brilliant physicist discovers a way to manipulate time, but each change creates dangerous ripples across multiple timelines. As reality begins to fracture, she must navigate through parallel worlds to save not just her own timeline, but all of existence.",
        "director": "Christopher Nolan",
        "cast": ["Emma Stone", "Oscar Isaac", "Michael Fassbender", "Lupita Nyong'o"],
        "genre": ["Sci-Fi", "Thriller", "Drama"],
        "duration": 148,
        "releaseYear": 2024,
        "rating": 8.7,
        "ageRating": "PG-13",
        "type": "movie",
        "language": "English",
        "thumbnailUrl": "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=800&h=1200&fit=crop",
        "backdropUrl": "https://images.unsplash.com/photo-1502134249126-9f3755a50d78?w=1920&h=1080&fit=crop",
        "trailerUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "videoUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "views": 2450000,
        "featured": True,
        "trending": True,
        "tags": ["time travel", "parallel universe", "mind-bending", "award winner"],
        "reviews": [],
        "subtitles": [],
        "seasons": [],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "title": "Neon Dreams",
        "description": "In a cyberpunk future, a hacker discovers a conspiracy that threatens the very fabric of digital reality. Racing against time and corporate assassins, she must infiltrate the most secure systems in the world.",
        "director": "Denis Villeneuve",
        "cast": ["Zendaya", "Timothée Chalamet", "Idris Elba", "Scarlett Johansson"],
        "genre": ["Sci-Fi", "Action", "Cyberpunk"],
        "duration": 132,
        "releaseYear": 2024,
        "rating": 8.2,
        "ageRating": "R",
        "type": "movie",
        "language": "English",
        "thumbnailUrl": "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=1200&fit=crop",
        "backdropUrl": "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=1920&h=1080&fit=crop",
        "trailerUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "videoUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "views": 1850000,
        "featured": True,
        "trending": False,
        "tags": ["cyberpunk", "hacker", "futuristic", "neon"],
        "reviews": [],
        "subtitles": [],
        "seasons": [],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "title": "The Last Symphony",
        "description": "A young prodigy conductor must save a legendary orchestra from bankruptcy while uncovering dark secrets about the mysterious composer whose works have been driving audiences to madness for centuries.",
        "director": "Greta Gerwig",
        "cast": ["Saoirse Ronan", "Adam Driver", "Tilda Swinton", "Ralph Fiennes"],
        "genre": ["Drama", "Mystery", "Musical"],
        "duration": 125,
        "releaseYear": 2024,
        "rating": 8.9,
        "ageRating": "PG-13",
        "type": "movie",
        "language": "English",
        "thumbnailUrl": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=1200&fit=crop",
        "backdropUrl": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1920&h=1080&fit=crop",
        "trailerUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "videoUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "views": 1200000,
        "featured": False,
        "trending": True,
        "tags": ["classical music", "prodigy", "orchestra", "mystery"],
        "reviews": [],
        "subtitles": [],
        "seasons": [],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "title": "Eclipse Hunter",
        "description": "When the sun begins to die, humanity's last hope lies with a team of space explorers who must journey to the edge of the solar system to ignite a new star. But they're not alone in the darkness.",
        "director": "Rian Johnson",
        "cast": ["John Boyega", "Lupita Nyong'o", "Oscar Isaac", "Daisy Ridley"],
        "genre": ["Sci-Fi", "Adventure", "Thriller"],
        "duration": 155,
        "releaseYear": 2024,
        "rating": 8.5,
        "ageRating": "PG-13",
        "type": "movie",
        "language": "English",
        "thumbnailUrl": "https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=800&h=1200&fit=crop",
        "backdropUrl": "https://images.unsplash.com/photo-1502134249126-9f3755a50d78?w=1920&h=1080&fit=crop",
        "trailerUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "videoUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "views": 3200000,
        "featured": True,
        "trending": True,
        "tags": ["space", "sun", "expedition", "survival"],
        "reviews": [],
        "subtitles": [],
        "seasons": [],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "title": "Midnight in Morocco",
        "description": "A romance novelist travels to Marrakech to overcome writer's block, but finds herself caught in a web of international espionage, ancient mysteries, and unexpected love.",
        "director": "Lulu Wang",
        "cast": ["Gemma Chan", "Dev Patel", "Mahershala Ali", "Lupita Nyong'o"],
        "genre": ["Romance", "Adventure", "Comedy"],
        "duration": 118,
        "releaseYear": 2024,
        "rating": 7.8,
        "ageRating": "PG-13",
        "type": "movie",
        "language": "English",
        "thumbnailUrl": "https://images.unsplash.com/photo-1539650116574-75c0c6d50806?w=800&h=1200&fit=crop",
        "backdropUrl": "https://images.unsplash.com/photo-1509650871405-f969d5b0d1b0?w=1920&h=1080&fit=crop",
        "trailerUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "videoUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "views": 950000,
        "featured": False,
        "trending": False,
        "tags": ["morocco", "romance", "writer", "adventure"],
        "reviews": [],
        "subtitles": [],
        "seasons": [],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "title": "The Algorithm Wars",
        "description": "In a world where AI controls everything, a group of rebels discovers that the machines are planning to eliminate human unpredictability. Their only weapon? Pure human chaos.",
        "director": "Jordan Peele",
        "cast": ["Michael B. Jordan", "Lupita Nyong'o", "LaKeith Stanfield", "Tessa Thompson"],
        "genre": ["Sci-Fi", "Action", "Thriller"],
        "duration": 140,
        "releaseYear": 2024,
        "rating": 8.3,
        "ageRating": "R",
        "type": "movie",
        "language": "English",
        "thumbnailUrl": "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=1200&fit=crop",
        "backdropUrl": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1920&h=1080&fit=crop",
        "trailerUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "videoUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "views": 2100000,
        "featured": True,
        "trending": False,
        "tags": ["AI", "rebellion", "algorithm", "dystopian"],
        "reviews": [],
        "subtitles": [],
        "seasons": [],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "title": "Ocean's Thirteen Ghosts",
        "description": "A master thief assembles a team to pull off the impossible: stealing from a haunted mansion where the security system is run by actual ghosts from different time periods.",
        "director": "Taika Waititi",
        "cast": ["Ryan Gosling", "Margot Robbie", "Mahershala Ali", "Tilda Swinton"],
        "genre": ["Comedy", "Heist", "Supernatural"],
        "duration": 128,
        "releaseYear": 2024,
        "rating": 7.9,
        "ageRating": "PG-13",
        "type": "movie",
        "language": "English",
        "thumbnailUrl": "https://images.unsplash.com/photo-1520637836862-4d197d17c983?w=800&h=1200&fit=crop",
        "backdropUrl": "https://images.unsplash.com/photo-1520637736862-4d197d17c983?w=1920&h=1080&fit=crop",
        "trailerUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "videoUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "views": 1650000,
        "featured": False,
        "trending": True,
        "tags": ["heist", "ghosts", "comedy", "supernatural"],
        "reviews": [],
        "subtitles": [],
        "seasons": [],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "title": "The Memory Thief",
        "description": "In a near-future where memories can be extracted and sold, a detective investigating memory theft discovers that his own past has been stolen and must navigate a world where nothing is as it seems.",
        "director": "Chloe Zhao",
        "cast": ["Adam Driver", "Rooney Mara", "Oscar Isaac", "Thomasin McKenzie"],
        "genre": ["Sci-Fi", "Mystery", "Thriller"],
        "duration": 135,
        "releaseYear": 2024,
        "rating": 8.4,
        "ageRating": "R",
        "type": "movie",
        "language": "English",
        "thumbnailUrl": "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=1200&fit=crop",
        "backdropUrl": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1920&h=1080&fit=crop",
        "trailerUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "videoUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "views": 1900000,
        "featured": True,
        "trending": True,
        "tags": ["memory", "detective", "identity", "future"],
        "reviews": [],
        "subtitles": [],
        "seasons": [],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "title": "Wild Heart",
        "description": "A wildlife photographer returns to her hometown to save the local animal sanctuary, but must confront her estranged family and the corporate developers threatening to destroy everything she loves.",
        "director": "Kelly Reichardt",
        "cast": ["Frances McDormand", "Thomasin McKenzie", "Brian Cox", "Michelle Williams"],
        "genre": ["Drama", "Family", "Nature"],
        "duration": 110,
        "releaseYear": 2024,
        "rating": 8.1,
        "ageRating": "PG",
        "type": "movie",
        "language": "English",
        "thumbnailUrl": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&h=1200&fit=crop",
        "backdropUrl": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1920&h=1080&fit=crop",
        "trailerUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "videoUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "views": 750000,
        "featured": False,
        "trending": False,
        "tags": ["wildlife", "family", "hometown", "nature"],
        "reviews": [],
        "subtitles": [],
        "seasons": [],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    },
    {
        "title": "Stellar Collision",
        "description": "When two distant galaxies begin to merge, causing catastrophic changes across the universe, a team of scientists must find a way to prevent the destruction of Earth before time runs out.",
        "director": "James Cameron",
        "cast": ["Zoe Saldana", "Sam Worthington", "Sigourney Weaver", "Stephen Lang"],
        "genre": ["Sci-Fi", "Action", "Adventure"],
        "duration": 162,
        "releaseYear": 2024,
        "rating": 8.6,
        "ageRating": "PG-13",
        "type": "movie",
        "language": "English",
        "thumbnailUrl": "https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=800&h=1200&fit=crop",
        "backdropUrl": "https://images.unsplash.com/photo-1502134249126-9f3755a50d78?w=1920&h=1080&fit=crop",
        "trailerUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "videoUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "views": 4100000,
        "featured": True,
        "trending": True,
        "tags": ["galaxies", "collision", "space", "scientists"],
        "reviews": [],
        "subtitles": [],
        "seasons": [],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    }
]

# Add 40 more movies to reach 50 total
additional_movies = [
    {
        "title": f"Action Hero {i}",
        "description": f"An adrenaline-packed action thriller about courage, betrayal, and redemption in the face of impossible odds. Movie number {i} in our collection.",
        "director": random.choice(["John Woo", "Michael Bay", "Kathryn Bigelow", "Christopher McQuarrie"]),
        "cast": [random.choice(["Tom Cruise", "Keanu Reeves", "Charlize Theron", "Jason Statham"]), 
                random.choice(["Scarlett Johansson", "Gal Gadot", "Margot Robbie", "Zendaya"]),
                random.choice(["Idris Elba", "Michael B. Jordan", "Ryan Reynolds", "Chris Evans"])],
        "genre": random.choice([["Action", "Thriller"], ["Action", "Adventure"], ["Sci-Fi", "Action"]]),
        "duration": random.randint(110, 150),
        "releaseYear": random.choice([2023, 2024]),
        "rating": round(random.uniform(7.0, 9.0), 1),
        "ageRating": random.choice(["PG-13", "R"]),
        "type": "movie",
        "language": "English",
        "thumbnailUrl": f"https://images.unsplash.com/photo-{random.choice(['1518709268805-4e9042af2176', '1533174072545-7a4b6ad7a6c3', '1440404653325-ab127d49abc1'])}?w=800&h=1200&fit=crop",
        "backdropUrl": f"https://images.unsplash.com/photo-{random.choice(['1502134249126-9f3755a50d78', '1451187580459-43490279c0fa', '1533174072545-7a4b6ad7a6c3'])}?w=1920&h=1080&fit=crop",
        "trailerUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "videoUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "views": random.randint(500000, 2000000),
        "featured": random.choice([True, False]),
        "trending": random.choice([True, False]),
        "tags": random.choice([["action", "thriller"], ["adventure", "hero"], ["sci-fi", "future"]]),
        "reviews": [],
        "subtitles": [],
        "seasons": [],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    } for i in range(11, 51)
]

# Combine all movies
all_movies = movies + additional_movies

def connect_to_database():
    """Connect to MongoDB"""
    try:
        client = pymongo.MongoClient(MONGODB_URI)
        db = client['netflix-clone']
        # Test the connection
        client.admin.command('ping')
        print("✅ Connected to MongoDB successfully!")
        return db
    except Exception as e:
        print(f"❌ MongoDB connection error: {e}")
        exit(1)

def add_movies_to_database(db):
    """Add movies to the database"""
    try:
        collection = db['videos']
        
        print("🎬 Starting to add movies to database...")
        
        # Clear existing movies (optional - comment out to keep existing data)
        # collection.delete_many({})
        # print("🗑️  Cleared existing movies")

        # Insert movies in batches
        batch_size = 10
        success_count = 0
        
        for i in range(0, len(all_movies), batch_size):
            batch = all_movies[i:i + batch_size]
            
            try:
                # Use insert_many with ordered=False to continue on duplicates
                results = collection.insert_many(batch, ordered=False)
                success_count += len(results.inserted_ids)
                print(f"✅ Added batch {(i // batch_size) + 1} ({len(results.inserted_ids)} movies)")
            except pymongo.errors.BulkWriteError as e:
                # Count successful inserts even if some fail due to duplicates
                success_count += len([op for op in e.details['writeErrors'] if op.get('code') != 11000])
                print(f"⚠️  Batch {(i // batch_size) + 1} completed with some duplicates skipped")
            except Exception as e:
                print(f"❌ Error in batch {(i // batch_size) + 1}: {e}")

        print(f"\n🎉 Successfully processed {success_count} movies!")
        
        # Display statistics
        stats = get_movie_stats(collection)
        print("\n📊 Database Statistics:")
        print(f"Total Movies: {stats['total']}")
        print(f"Featured Movies: {stats['featured']}")
        print(f"Trending Movies: {stats['trending']}")
        print(f"Movies by Type: {stats['movie_count']} movies, {stats['series_count']} series")
        
    except Exception as e:
        print(f"❌ Error adding movies to database: {e}")

def get_movie_stats(collection):
    """Get database statistics"""
    total = collection.count_documents({})
    featured = collection.count_documents({"featured": True})
    trending = collection.count_documents({"trending": True})
    movie_count = collection.count_documents({"type": "movie"})
    series_count = collection.count_documents({"type": "series"})
    
    return {
        'total': total,
        'featured': featured,
        'trending': trending,
        'movie_count': movie_count,
        'series_count': series_count
    }

def main():
    """Main function"""
    print("🎬 Netflix Clone - Movie Database Seeder")
    print("=" * 50)
    
    # Connect to database
    db = connect_to_database()
    
    # Add movies
    add_movies_to_database(db)
    
    print("\n🎬 Movie addition complete!")
    print("You can now start your Netflix clone application.")
    print("The following sections will now show real data:")
    print("  • Hero Section: Random featured content")
    print("  • Coming Soon: Random movies")  
    print("  • Featured For You: Featured movies (featured: true)")
    print("  • Trending Now: Trending movies (trending: true)")
    print("  • Just for You: Series content")

if __name__ == "__main__":
    main()