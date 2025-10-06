"""
Unit tests for Pydantic schemas.
"""
import pytest
from datetime import date
from pydantic import ValidationError
from schemas import (
    MovieCreate,
    MovieUpdate,
    ActorCreate,
    DirectorCreate,
    GenreCreate
)


class TestMovieSchemas:
    """Test cases for Movie schemas."""
    
    def test_movie_create_valid(self):
        """Test creating a valid movie schema."""
        movie = MovieCreate(
            title="Inception",
            description="A mind-bending thriller",
            release_year=2010,
            duration_minutes=148,
            rating=8.8,
            director_id=1,
            actor_ids=[1, 2],
            genre_ids=[1, 2]
        )
        
        assert movie.title == "Inception"
        assert movie.release_year == 2010
        assert movie.rating == 8.8
        assert len(movie.actor_ids) == 2
    
    def test_movie_create_title_required(self):
        """Test that title is required."""
        with pytest.raises(ValidationError) as exc:
            MovieCreate(
                release_year=2010,
                rating=8.0
            )
        
        assert 'title' in str(exc.value)
    
    def test_movie_create_empty_title(self):
        """Test that empty title is rejected."""
        with pytest.raises(ValidationError) as exc:
            MovieCreate(
                title="   ",
                release_year=2010,
                rating=8.0
            )
        
        assert 'title' in str(exc.value).lower()
    
    def test_movie_invalid_year(self):
        """Test that invalid year is rejected."""
        with pytest.raises(ValidationError):
            MovieCreate(
                title="Test Movie",
                release_year=1800,  # Too old
                rating=8.0
            )
        
        with pytest.raises(ValidationError):
            MovieCreate(
                title="Test Movie",
                release_year=2200,  # Too far in future
                rating=8.0
            )
    
    def test_movie_invalid_rating(self):
        """Test that invalid rating is rejected."""
        with pytest.raises(ValidationError):
            MovieCreate(
                title="Test Movie",
                release_year=2010,
                rating=11.0  # Too high
            )
        
        with pytest.raises(ValidationError):
            MovieCreate(
                title="Test Movie",
                release_year=2010,
                rating=-1.0  # Too low
            )
    
    def test_movie_rating_rounding(self):
        """Test that rating is rounded to 1 decimal."""
        movie = MovieCreate(
            title="Test Movie",
            release_year=2010,
            rating=8.888
        )
        
        assert movie.rating == 8.9
    
    def test_movie_update_partial(self):
        """Test partial update schema."""
        update = MovieUpdate(
            title="Updated Title",
            rating=9.0
        )
        
        assert update.title == "Updated Title"
        assert update.rating == 9.0
        assert update.description is None


class TestActorSchemas:
    """Test cases for Actor schemas."""
    
    def test_actor_create_valid(self):
        """Test creating a valid actor schema."""
        actor = ActorCreate(
            name="Leonardo DiCaprio",
            bio="American actor",
            birth_date=date(1974, 11, 11),
            nationality="American"
        )
        
        assert actor.name == "Leonardo DiCaprio"
        assert actor.nationality == "American"
    
    def test_actor_name_required(self):
        """Test that actor name is required."""
        with pytest.raises(ValidationError) as exc:
            ActorCreate()
        
        assert 'name' in str(exc.value)
    
    def test_actor_empty_name(self):
        """Test that empty name is rejected."""
        with pytest.raises(ValidationError):
            ActorCreate(name="   ")
    
    def test_actor_name_trimmed(self):
        """Test that actor name is trimmed."""
        actor = ActorCreate(name="  Tom Hanks  ")
        assert actor.name == "Tom Hanks"
    
    def test_actor_future_birth_date(self):
        """Test that future birth date is rejected."""
        from datetime import timedelta
        future_date = date.today() + timedelta(days=365)
        
        with pytest.raises(ValidationError) as exc:
            ActorCreate(
                name="Test Actor",
                birth_date=future_date
            )
        
        assert 'birth_date' in str(exc.value).lower()


class TestDirectorSchemas:
    """Test cases for Director schemas."""
    
    def test_director_create_valid(self):
        """Test creating a valid director schema."""
        director = DirectorCreate(
            name="Christopher Nolan",
            bio="British-American director",
            birth_date=date(1970, 7, 30),
            nationality="British-American"
        )
        
        assert director.name == "Christopher Nolan"
        assert director.birth_date == date(1970, 7, 30)
    
    def test_director_name_required(self):
        """Test that director name is required."""
        with pytest.raises(ValidationError):
            DirectorCreate()
    
    def test_director_name_trimmed(self):
        """Test that director name is trimmed."""
        director = DirectorCreate(name="  Steven Spielberg  ")
        assert director.name == "Steven Spielberg"


class TestGenreSchemas:
    """Test cases for Genre schemas."""
    
    def test_genre_create_valid(self):
        """Test creating a valid genre schema."""
        genre = GenreCreate(
            name="Action",
            description="Action-packed movies"
        )
        
        assert genre.name == "Action"
        assert genre.description == "Action-packed movies"
    
    def test_genre_name_required(self):
        """Test that genre name is required."""
        with pytest.raises(ValidationError):
            GenreCreate()
    
    def test_genre_name_trimmed(self):
        """Test that genre name is trimmed."""
        genre = GenreCreate(name="  Comedy  ")
        assert genre.name == "Comedy"
    
    def test_genre_name_max_length(self):
        """Test genre name max length constraint."""
        with pytest.raises(ValidationError):
            GenreCreate(name="A" * 51)  # Too long


class TestSchemaIntegration:
    """Integration tests for schema relationships."""
    
    def test_movie_with_relations(self):
        """Test movie schema with all relations."""
        movie_data = {
            "title": "The Dark Knight",
            "description": "Batman fights the Joker",
            "release_year": 2008,
            "duration_minutes": 152,
            "rating": 9.0,
            "director_id": 1,
            "actor_ids": [1, 2, 3],
            "genre_ids": [1, 2]
        }
        
        movie = MovieCreate(**movie_data)
        
        assert movie.title == "The Dark Knight"
        assert len(movie.actor_ids) == 3
        assert len(movie.genre_ids) == 2
    
    def test_empty_lists_default(self):
        """Test that empty lists default properly."""
        movie = MovieCreate(
            title="Test Movie",
            release_year=2020,
            rating=7.0
        )
        
        assert movie.actor_ids == []
        assert movie.genre_ids == []