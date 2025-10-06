"""
Pydantic schemas for Actor model.
"""
from typing import Optional, List
from datetime import date
from pydantic import Field, field_validator
from schemas.base import BaseSchema


class ActorBase(BaseSchema):
    """Base actor schema with common fields."""
    name: str = Field(..., min_length=1, max_length=200, description="Actor's full name")
    bio: Optional[str] = Field(None, description="Actor biography")
    birth_date: Optional[date] = Field(None, description="Date of birth")
    nationality: Optional[str] = Field(None, max_length=100, description="Nationality")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate and normalize actor name."""
        if not v or not v.strip():
            raise ValueError('Actor name cannot be empty')
        return v.strip()
    
    @field_validator('birth_date')
    @classmethod
    def validate_birth_date(cls, v: Optional[date]) -> Optional[date]:
        """Validate birth date is not in the future."""
        if v and v > date.today():
            raise ValueError('Birth date cannot be in the future')
        return v


class ActorCreate(ActorBase):
    """Schema for creating a new actor."""
    pass


class ActorUpdate(BaseSchema):
    """Schema for updating an actor."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    bio: Optional[str] = None
    birth_date: Optional[date] = None
    nationality: Optional[str] = Field(None, max_length=100)


class ActorResponse(ActorBase):
    """Schema for actor response."""
    id: int = Field(..., description="Actor ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Leonardo DiCaprio",
                "bio": "American actor and film producer",
                "birth_date": "1974-11-11",
                "nationality": "American"
            }
        }


class ActorWithMovies(ActorResponse):
    """Schema for actor response with their movies."""
    movies: List['MovieSummary'] = Field(default_factory=list, description="Movies acted in")
    movie_count: int = Field(0, description="Total number of movies")
    genres: List[str] = Field(default_factory=list, description="Genres worked in")


# Avoid circular imports
from schemas.movie import MovieSummary
ActorWithMovies.model_rebuild()