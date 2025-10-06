"""
Pydantic schemas for Movie model.
"""
from typing import Optional, List
from pydantic import Field, field_validator
from schemas.base import BaseSchema
from utils.validators import validate_year, validate_rating


class MovieBase(BaseSchema):
    """Base movie schema with common fields."""
    title: str = Field(..., min_length=1, max_length=255, description="Movie title")
    description: Optional[str] = Field(None, description="Movie plot/synopsis")
    release_year: int = Field(..., ge=1888, le=2100, description="Release year")
    duration_minutes: Optional[int] = Field(None, gt=0, description="Duration in minutes")
    rating: float = Field(0.0, ge=0.0, le=10.0, description="Movie rating (0-10)")
    poster_url: Optional[str] = Field(None, max_length=500, description="Poster image URL")
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate and normalize movie title."""
        if not v or not v.strip():
            raise ValueError('Movie title cannot be empty')
        return v.strip()
    
    @field_validator('release_year')
    @classmethod
    def validate_release_year(cls, v: int) -> int:
        """Validate release year using custom validator."""
        if not validate_year(v):
            raise ValueError(f'Release year must be between 1888 and {2100}')
        return v
    
    @field_validator('rating')
    @classmethod
    def validate_movie_rating(cls, v: float) -> float:
        """Validate rating using custom validator."""
        if not validate_rating(v):
            raise ValueError('Rating must be between 0.0 and 10.0')
        return round(v, 1)  # Round to 1 decimal place


class MovieCreate(MovieBase):
    """Schema for creating a new movie."""
    director_id: Optional[int] = Field(None, description="Director ID")
    actor_ids: List[int] = Field(default_factory=list, description="List of actor IDs")
    genre_ids: List[int] = Field(default_factory=list, description="List of genre IDs")


class MovieUpdate(BaseSchema):
    """Schema for updating a movie."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    release_year: Optional[int] = Field(None, ge=1888, le=2100)
    duration_minutes: Optional[int] = Field(None, gt=0)
    rating: Optional[float] = Field(None, ge=0.0, le=10.0)
    poster_url: Optional[str] = Field(None, max_length=500)
    director_id: Optional[int] = None
    actor_ids: Optional[List[int]] = None
    genre_ids: Optional[List[int]] = None


class GenreSummary(BaseSchema):
    """Summary schema for genre in movie response."""
    id: int
    name: str


class ActorSummary(BaseSchema):
    """Summary schema for actor in movie response."""
    id: int
    name: str


class DirectorSummary(BaseSchema):
    """Summary schema for director in movie response."""
    id: int
    name: str


class MovieSummary(BaseSchema):
    """Summary schema for movie in list views."""
    id: int = Field(..., description="Movie ID")
    title: str = Field(..., description="Movie title")
    release_year: int = Field(..., description="Release year")
    rating: float = Field(..., description="Movie rating")
    poster_url: Optional[str] = Field(None, description="Poster URL")
    director: Optional[DirectorSummary] = None
    genres: List[str] = Field(default_factory=list, description="Genre names")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Inception",
                "release_year": 2010,
                "rating": 8.8,
                "poster_url": "https://example.com/inception.jpg",
                "director": {
                    "id": 1,
                    "name": "Christopher Nolan"
                },
                "genres": ["Sci-Fi", "Thriller"]
            }
        }


class MovieResponse(MovieBase):
    """Schema for detailed movie response."""
    id: int = Field(..., description="Movie ID")
    director: Optional[DirectorSummary] = None
    actors: List[ActorSummary] = Field(default_factory=list, description="Cast members")
    genres: List[GenreSummary] = Field(default_factory=list, description="Movie genres")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Inception",
                "description": "A thief who steals corporate secrets...",
                "release_year": 2010,
                "duration_minutes": 148,
                "rating": 8.8,
                "poster_url": "https://example.com/inception.jpg",
                "director": {
                    "id": 1,
                    "name": "Christopher Nolan"
                },
                "actors": [
                    {"id": 1, "name": "Leonardo DiCaprio"},
                    {"id": 2, "name": "Tom Hardy"}
                ],
                "genres": [
                    {"id": 1, "name": "Sci-Fi"},
                    {"id": 2, "name": "Thriller"}
                ]
            }
        }