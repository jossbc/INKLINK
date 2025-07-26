from pydantic import BaseModel, Field, field_validator
from typing import Optional

VALID_GENRES = [
    "Fantasia", "Ciencia Ficcion", "Romance", "Drama", "Terror",
    "Misterio", "Historico", "Poesia", "Juvenil"
]

class Book(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="MongoDB ID - Se genera automáticamente desde el _id de MongoDB, no es necesario enviarlo en POST"
    )

    title: str = Field(
        description="Book title",
        pattern=r"^[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ¿¡«][A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ\s,:;'\"!?\-—\.¿¡«»]+$",
        examples=["The Love Hypothesis", "Travesuras de una niña mala"]
    )

    author_id: str = Field(
        description="Author ID",
        examples=["507f1f77bcf86cd799439012"]
    )

    publication_year: int = Field(
        description="Year the book was released",
        examples=[2021, 2006]
    )

    genre: str = Field(
        description="Genre of the book",
        examples=["Fantasia", "Romance"]
    )

    @field_validator("publication_year")
    @classmethod
    def validate_year(cls, year: int):
        if year < 1400 or year > 2025:
            raise ValueError("El año de publicación debe estar entre 1400 y 2025.")
        return year

    @field_validator("genre")
    @classmethod
    def validate_genre(cls, genre):
        if genre not in VALID_GENRES:
            raise ValueError(f"Genero no válido. Usa uno de: {', '.join(VALID_GENRES)}")
        return genre
