"""
Pytest configuration and fixtures for backend tests.
"""
import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import Movie, Actor, Director, Genre
from app import create_app


@pytest.fixture(scope='session')
def app():
    """Create application for testing."""
    from config import TestingConfig
    app = create_app(TestingConfig)
    return app


@pytest.fixture(scope='session')
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture(scope='function')
def db_session():
    """Create a test database session."""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def sample_director(db_session):
    """Create a sample director."""
    director = Director(
        name="Test Director",
        bio="A test director bio",
        birth_date=date(1970, 1, 1),
        nationality="American"
    )
    db_session.add(director)
    db_session.commit()
    db_session.refresh(director)
    return director


@pytest.fixture
def sample_actor(db_session):
    """Create a sample actor."""
    actor = Actor(
        name="Test Actor",
        bio="A test actor bio",
        birth_date=date(1980, 1, 1),
        nationality="British"
    )
    db_session.add(actor)
    db_session.commit()
    db_session.refresh(actor)
    return actor


@pytest.fixture
def sample_genre(db_session):
    """Create a sample genre."""
    genre = Genre(
        name="Action",
        description="Action movies"
    )
    db_session.add(genre)
    db_session.commit()
    db_session.refresh(genre)
    return genre


@pytest.fixture
def sample_movie(db_session, sample_director, sample_actor, sample_genre):
    """Create a sample movie with relationships."""
    movie = Movie(
        title="Test Movie",
        description="A test movie description",
        release_year=2020,
        duration_minutes=120,
        rating=7.5,
        director_id=sample_director.id
    )
    movie.actors.append(sample_actor)
    movie.genres.append(sample_genre)
    
    db_session.add(movie)
    db_session.commit()
    db_session.refresh(movie)
    return movie


@pytest.fixture
def multiple_movies(db_session, sample_director):
    """Create multiple movies for testing pagination and filtering."""
    movies = []
    
    # Create genres
    scifi = Genre(name="Sci-Fi", description="Science Fiction")
    drama = Genre(name="Drama", description="Drama movies")
    db_session.add_all([scifi, drama])
    db_session.commit()
    
    # Create actors
    actor1 = Actor(name="Actor One")
    actor2 = Actor(name="Actor Two")
    db_session.add_all([actor1, actor2])
    db_session.commit()
    
    # Create movies
    for i in range(5):
        movie = Movie(
            title=f"Movie {i+1}",
            description=f"Description {i+1}",
            release_year=2020 + i,
            rating=7.0 + (i * 0.5),
            director_id=sample_director.id
        )
        
        # Add genres
        if i % 2 == 0:
            movie.genres.append(scifi)
        else:
            movie.genres.append(drama)
        
        # Add actors
        if i < 3:
            movie.actors.append(actor1)
        else:
            movie.actors.append(actor2)
        
        db_session.add(movie)
        movies.append(movie)
    
    db_session.commit()
    return movies