import logging
from fastapi import HTTPException
from models.author import Author
from utils.mongodb import get_collection
from bson import ObjectId

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

books_coll = get_collection("books")
authors_coll = get_collection("authors")

async def create_author(author: Author) -> Author:
    try:
        author_dict = author.model_dump(exclude={"id"})
        inserted = authors_coll.insert_one(author_dict)
        author.id = str(inserted.inserted_id)
        return author
    except Exception as e:
        logger.error(f"Error creating author: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_all_authors() -> list[Author]:
    try:
        authors = []
        for doc in authors_coll.find():
            doc["id"] = str(doc["_id"])
            authors.append(Author(**doc))
        return authors
    except Exception as e:
        logger.error(f"Error fetching authors: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_author_by_id(author_id: str) -> Author:
    try:
        doc = authors_coll.find_one({"_id": ObjectId(author_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Autor no encontrado")
        doc["id"] = str(doc["_id"])
        return Author(**doc)
    except Exception as e:
        logger.error(f"Error fetching author by id: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def delete_author(author_id: str):
    try:
        author = authors_coll.find_one({"_id": ObjectId(author_id)})
        if not author:
            raise HTTPException(status_code=404, detail="Autor no encontrado")

        books_with_author = books_coll.count_documents({"author_id": author_id})
        if books_with_author > 0:
            raise HTTPException(
                status_code=400,
                detail="No se puede eliminar un autor con libros asociados"
            )

        authors_coll.delete_one({"_id": ObjectId(author_id)})
        return {"message": "Autor eliminado correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting author: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
