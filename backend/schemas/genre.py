"""
Pydantic schemas for Genre model.
"""
from typing import Optional, List
from pydantic import Field, field_validator
from schemas.base import BaseSchema


class GenreBase(BaseSchema):
    """Base genre schema with common fields."""
    name: str = Field(..., min_length=1, max_length=50, description="Genre name")
    description: Optional[str] = Field(None, max_length=500, description="Genre description")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate and normalize genre name."""
        if not v or not v.strip():
            raise ValueError('Genre name cannot be empty')
        return v.strip()


class GenreCreate(GenreBase):
    """Schema for creating a new genre."""
    pass


class GenreUpdate(BaseSchema):
    """Schema for updating a genre."""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=500)


class GenreResponse(GenreBase):
    """Schema for genre response."""
    id: int = Field(..., description="Genre ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Action",
                "description": "Action-packed movies with intense sequences"
            }
        }


class GenreWithMovies(GenreResponse):
    """Schema for genre response with movies."""
    movies: List['MovieSummary'] = Field(default_factory=list, description="Movies in this genre")


# Avoid circular imports - will be resolved when imported together
from schemas.movie import MovieSummary
GenreWithMovies.model_rebuild()