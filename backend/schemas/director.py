"""
Pydantic schemas for Director model.
"""
from typing import Optional, List
from datetime import date
from pydantic import Field, field_validator
from schemas.base import BaseSchema


class DirectorBase(BaseSchema):
    """Base director schema with common fields."""
    name: str = Field(..., min_length=1, max_length=200, description="Director's full name")
    bio: Optional[str] = Field(None, description="Director biography")
    birth_date: Optional[date] = Field(None, description="Date of birth")
    nationality: Optional[str] = Field(None, max_length=100, description="Nationality")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate and normalize director name."""
        if not v or not v.strip():
            raise ValueError('Director name cannot be empty')
        return v.strip()
    
    @field_validator('birth_date')
    @classmethod
    def validate_birth_date(cls, v: Optional[date]) -> Optional[date]:
        """Validate birth date is not in the future."""
        if v and v > date.today():
            raise ValueError('Birth date cannot be in the future')
        return v


class DirectorCreate(DirectorBase):
    """Schema for creating a new director."""
    pass


class DirectorUpdate(BaseSchema):
    """Schema for updating a director."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    bio: Optional[str] = None
    birth_date: Optional[date] = None
    nationality: Optional[str] = Field(None, max_length=100)


class DirectorResponse(DirectorBase):
    """Schema for director response."""
    id: int = Field(..., description="Director ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Christopher Nolan",
                "bio": "British-American film director and screenwriter",
                "birth_date": "1970-07-30",
                "nationality": "British-American"
            }
        }


class DirectorWithMovies(DirectorResponse):
    """Schema for director response with their movies."""
    movies: List['MovieSummary'] = Field(default_factory=list, description="Movies directed")
    movie_count: int = Field(0, description="Total number of movies directed")


# Avoid circular imports
from schemas.movie import MovieSummary
DirectorWithMovies.model_rebuild()