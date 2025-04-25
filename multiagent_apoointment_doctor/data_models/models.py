import re
from pydantic import BaseModel, Field, field_validator
from typing import Annotated  # For better type hints


class DateTimeModel(BaseModel):
    date: Annotated[  # Sees str with metadata, Annotated lets us attach additional metadata to a type
        str,  # Base type
        Field(
            description="Properly formatted date in 'DD-MM-YYYY HH:MM' format",
            pattern=r'^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$',  # Metadata
            examples=["25-12-2023 14:30"]  # example for OpenAPI docs
        )
    ]

    @field_validator('date')
    @classmethod # decorator indicates that a method is a class method and makes the validator operate at the class level
    def validate_date_format(cls, v: str) -> str:  # Class reference = cls, Input value = v
        """Validate the date format matches DD-MM-YYYY HH:MM"""
        if not re.fullmatch(r'^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$', v):
            raise ValueError("Date must be in format 'DD-MM-YYYY HH:MM'")
        return v


class DateModel(BaseModel):
    date: Annotated[  # Consistent Annotated style
        str,
        Field(
            description="Properly formatted date in 'DD-MM-YYYY' format",
            pattern=r'^\d{2}-\d{2}-\d{4}$',
            examples=["25-12-2023"]
        )
    ]

    @field_validator('date')
    @classmethod
    def validate_date_format(cls, v: str) -> str:  # Added type hints
        if not re.fullmatch(r'^\d{2}-\d{2}-\d{4}$', v):  # Use fullmatch
            raise ValueError("Date must be in format 'DD-MM-YYYY'")
        return v


class IdentificationNumberModel(BaseModel):
    id: Annotated[
        int,
        Field(
            description="Identification number (7 or 8 digits long)",
            examples=[1234567, 12345678, 1000033, 1000014],
            ge=1_000_000,   # ge (Greater Than or Equal To) Ensures the ID is ≥ 1,000,000 (7-digit minimum)
            le=99_999_999 # le (Less Than or Equal To) Ensures the ID is ≤ 99,999,999 (8-digit maximum)
        )
    ]

    @field_validator('id')
    @classmethod
    def validate_id_format(cls, v: int) -> int:
        if not 1_000_000 <= v <= 99_999_999:  # More efficient than regex
            raise ValueError("ID must be 7 or 8 digits")
        return v
