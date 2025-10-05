"""
Unit tests for database models.
"""
import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import Movie, Actor, Director, Genre


@pytest.fixture
def db_session():
    """Create a test database session."""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


class TestDirectorModel:
    """Test cases for Director model."""
    
    def test_create_director(self, db_session):
        """Test creating a director."""
        director = Director(
            name="Christopher Nolan",
            bio="British-American film director",
            birth_date=date(1970, 7, 30),
            nationality="British-American"
        )
        db_session.add(director)
        db_session.commit()
        
        assert director.id is not None
        assert director.name == "Christopher Nolan"
        assert director.nationality == "British-American"
    
    def test_director_to_dict(self, db_session):
        """Test director to_dict method."""
        director = Director(name="Steven Spielberg")
        db_session.add(director)
        db_session.commit()
        
        data = director.to_dict()
        assert data['name'] == "Steven Spielberg"
        assert 'id' in data


class TestActorModel:
    """Test cases for Actor model."""
    
    def test_create_actor(self, db_session):
        """Test creating an actor."""
        actor = Actor(
            name="Leonardo DiCaprio",
            bio="American actor",
            birth_date=date(1974, 11, 11),
            nationality="American"
        )
        db_session.add(actor)
        db_session.commit()
        
        assert actor.id is not None
        assert actor.name == "Leonardo DiCaprio"
    
    def test_actor_to_dict(self, db_session):
        """Test actor to_dict method."""
        actor = Actor(name="Tom Hanks")
        db_session.add(actor)
        db_session.commit()
        
        data = actor.to_dict()
        assert data['name'] == "Tom Hanks"
        assert 'id' in data


class TestGenreModel:
    """Test cases for Genre model."""
    
    def test_create_genre(self, db_session):
        """Test creating a genre."""
        genre = Genre(
            name="Action",
            description="Action-packed movies"
        )
        db_session.add(genre)
        db_session.commit()
        
        assert genre.id is not None
        assert genre.name == "Action"
    
    def test_genre_unique_name(self, db_session):
        """Test that genre names are unique."""
        genre1 = Genre(name="Comedy")
        db_session.add(genre1)
        db_session.commit()
        
        # This should raise an error due to unique constraint
        genre2 = Genre(name="Comedy")
        db_session.add(genre2)
        
        with pytest.raises(Exception):
            db_session.commit()


class TestMovieModel:
    """Test cases for Movie model."""
    
    def test_create_movie(self, db_session):
        """Test creating a movie."""
        director = Director(name="Christopher Nolan")
        db_session.add(director)
        db_session.commit()
        
        movie = Movie(
            title="Inception",
            description="A mind-bending thriller",
            release_year=2010,
            duration_minutes=148,
            rating=8.8,
            director_id=director.id
        )
        db_session.add(movie)
        db_session.commit()
        
        assert movie.id is not None
        assert movie.title == "Inception"
        assert movie.director.name == "Christopher Nolan"
    
    def test_movie_with_actors(self, db_session):
        """Test movie with actors (many-to-many)."""
        movie = Movie(
            title="The Dark Knight",
            release_year=2008,
            rating=9.0
        )
        actor1 = Actor(name="Christian Bale")
        actor2 = Actor(name="Heath Ledger")
        
        db_session.add_all([movie, actor1, actor2])
        db_session.commit()
        
        movie.actors.append(actor1)
        movie.actors.append(actor2)
        db_session.commit()
        
        assert movie.actors.count() == 2
        assert actor1.movies.count() == 1
    
    def test_movie_with_genres(self, db_session):
        """Test movie with genres (many-to-many)."""
        movie = Movie(
            title="Interstellar",
            release_year=2014,
            rating=8.6
        )
        genre1 = Genre(name="Sci-Fi")
        genre2 = Genre(name="Drama")
        
        db_session.add_all([movie, genre1, genre2])
        db_session.commit()
        
        movie.genres.append(genre1)
        movie.genres.append(genre2)
        db_session.commit()
        
        assert movie.genres.count() == 2
        assert genre1.movies.count() == 1
    
    def test_movie_rating_constraint(self, db_session):
        """Test that movie rating must be between 0 and 10."""
        movie = Movie(
            title="Test Movie",
            release_year=2020,
            rating=11.0  # Invalid rating
        )
        db_session.add(movie)
        
        with pytest.raises(Exception):
            db_session.commit()
    
    def test_movie_to_dict(self, db_session):
        """Test movie to_dict method."""
        director = Director(name="Quentin Tarantino")
        movie = Movie(
            title="Pulp Fiction",
            release_year=1994,
            rating=8.9,
            director=director
        )
        db_session.add_all([director, movie])
        db_session.commit()
        
        data = movie.to_dict(include_relations=True)
        assert data['title'] == "Pulp Fiction"
        assert data['director']['name'] == "Quentin Tarantino"
    
    def test_movie_to_summary_dict(self, db_session):
        """Test movie to_summary_dict method."""
        movie = Movie(
            title="Test Movie",
            release_year=2020,
            rating=7.5
        )
        db_session.add(movie)
        db_session.commit()
        
        summary = movie.to_summary_dict()
        assert summary['title'] == "Test Movie"
        assert summary['release_year'] == 2020
        assert 'genres' in summary