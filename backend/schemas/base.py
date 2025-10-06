"""
Base schemas with common configurations.
"""
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    
    model_config = ConfigDict(
        from_attributes=True,  # Enable ORM mode for SQLAlchemy models
        populate_by_name=True,
        str_strip_whitespace=True,
        validate_assignment=True
    )