#!/usr/bin/env python
"""
Database seeding script.
Populates database with sample movies, actors, directors, and genres.
Data is loaded from JSON files in the seed/ directory.

Usage:
    python seed_data.py [--clear]
    
Options:
    --clear     Clear all existing data before seeding
"""
import sys
import argparse
from datetime import datetime
from database import SessionLocal, init_db
from models import Movie, Actor, Director, Genre
from seed import load_genres, load_directors, load_actors, load_movies


def clear_data(db):
    """Clear all data from the database."""
    print("Clearing existing data...")
    
    # Delete in order to respect foreign key constraints
    db.query(Movie).delete()
    db.query(Actor).delete()
    db.query(Director).delete()
    db.query(Genre).delete()
    
    db.commit()
    print("✓ All data cleared")


def seed_genres(db):
    """Seed genre data from JSON file."""
    print("\nSeeding genres...")
    
    genres_data = load_genres()
    
    if not genres_data:
        print("⚠ No genre data found")
        return {}
    
    genres = []
    for genre_data in genres_data:
        genre = Genre(**genre_data)
        db.add(genre)
        genres.append(genre)
    
    db.commit()
    print(f"✓ Created {len(genres)} genres")
    
    return {genre.name: genre for genre in genres}


def seed_directors(db):
    """Seed director data from JSON file."""
    print("\nSeeding directors...")
    
    directors_data = load_directors()
    
    if not directors_data:
        print("⚠ No director data found")
        return {}
    
    directors = []
    for director_data in directors_data:
        # Convert birth_date string to date object
        if 'birth_date' in director_data and director_data['birth_date']:
            director_data['birth_date'] = datetime.strptime(
                director_data['birth_date'], 
                '%Y-%m-%d'
            ).date()
        
        director = Director(**director_data)
        db.add(director)
        directors.append(director)
    
    db.commit()
    print(f"✓ Created {len(directors)} directors")
    
    return {director.name: director for director in directors}


def seed_actors(db):
    """Seed actor data from JSON file."""
    print("\nSeeding actors...")
    
    actors_data = load_actors()
    
    if not actors_data:
        print("⚠ No actor data found")
        return {}
    
    actors = []
    for actor_data in actors_data:
        # Convert birth_date string to date object
        if 'birth_date' in actor_data and actor_data['birth_date']:
            actor_data['birth_date'] = datetime.strptime(
                actor_data['birth_date'], 
                '%Y-%m-%d'
            ).date()
        
        actor = Actor(**actor_data)
        db.add(actor)
        actors.append(actor)
    
    db.commit()
    print(f"✓ Created {len(actors)} actors")
    
    return {actor.name: actor for actor in actors}


def seed_movies(db, directors, actors, genres):
    """Seed movie data from JSON file with relationships."""
    print("\nSeeding movies...")
    
    movies_data = load_movies()
    
    if not movies_data:
        print("⚠ No movie data found")
        return []
    
    movies = []
    skipped = 0
    
    for movie_data in movies_data:
        # Extract relationships
        director_name = movie_data.pop("director", None)
        actor_names = movie_data.pop("actors", [])
        genre_names = movie_data.pop("genres", [])
        
        # Create movie
        movie = Movie(**movie_data)
        
        # Set director
        if director_name and director_name in directors:
            movie.director = directors[director_name]
        elif director_name:
            print(f"⚠ Warning: Director '{director_name}' not found for movie '{movie.title}'")
        
        # Add actors
        for actor_name in actor_names:
            if actor_name in actors:
                movie.actors.append(actors[actor_name])
            else:
                print(f"⚠ Warning: Actor '{actor_name}' not found for movie '{movie.title}'")
        
        # Add genres
        for genre_name in genre_names:
            if genre_name in genres:
                movie.genres.append(genres[genre_name])
            else:
                print(f"⚠ Warning: Genre '{genre_name}' not found for movie '{movie.title}'")
        
        db.add(movie)
        movies.append(movie)
    
    db.commit()
    
    if skipped > 0:
        print(f"✓ Created {len(movies)} movies ({skipped} skipped due to missing data)")
    else:
        print(f"✓ Created {len(movies)} movies")
    
    return movies


def main():
    """Main function to seed database."""
    parser = argparse.ArgumentParser(
        description='Seed Movie Explorer database with sample data'
    )
    parser.add_argument(
        '--clear',
        action='store_true',
        help='Clear all existing data before seeding'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Movie Explorer Platform - Database Seeding")
    print("=" * 60)
    
    # Ensure tables exist
    print("\nEnsuring database tables exist...")
    init_db()
    
    # Create session
    db = SessionLocal()
    
    try:
        # Clear data if requested
        if args.clear:
            confirmation = input("\n⚠ This will delete all existing data. Type 'yes' to confirm: ")
            if confirmation.lower() != 'yes':
                print("Seeding cancelled")
                sys.exit(0)
            clear_data(db)
        
        # Seed data from JSON files
        genres = seed_genres(db)
        directors = seed_directors(db)
        actors = seed_actors(db)
        movies = seed_movies(db, directors, actors, genres)
        
        print("\n" + "=" * 60)
        print("✓ Database seeding completed successfully!")
        print("=" * 60)
        print(f"\nSeeded:")
        print(f"  • {len(genres)} genres")
        print(f"  • {len(directors)} directors")
        print(f"  • {len(actors)} actors")
        print(f"  • {len(movies)} movies")
        print("\nData loaded from:")
        print("  • seed/genres.json")
        print("  • seed/directors.json")
        print("  • seed/actors.json")
        print("  • seed/movies.json")
        print("\nNext step:")
        print("  Start the application: python app.py")
        
    except Exception as e:
        print(f"\n✗ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == '__main__':
    main()