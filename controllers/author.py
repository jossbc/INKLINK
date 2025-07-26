import logging
from fastapi import HTTPException
from models.author import Author
from utils.mongodb import get_collection
from bson import ObjectId
from pipelines.author_pipeline import authors_with_book_count_pipeline


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_author(author: Author) -> Author:
    try:
        coll = get_collection("authors")
        author_dict = author.model_dump(exclude={"id"})
        inserted = coll.insert_one(author_dict)
        author.id = str(inserted.inserted_id)
        return author
    except Exception as e:
        logger.error(f"Error creating author: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_all_authors() -> list[Author]:
    try:
        coll = get_collection("authors")
        authors = []
        for doc in coll.find():
            doc["id"] = str(doc["_id"])
            authors.append(Author(**doc))
        return authors
    except Exception as e:
        logger.error(f"Error fetching authors: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_author_by_id(author_id: str) -> Author:
    try:
        coll = get_collection("authors")
        doc = coll.find_one({"_id": ObjectId(author_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Autor no encontrado")
        doc["id"] = str(doc["_id"])
        return Author(**doc)
    except Exception as e:
        logger.error(f"Error fetching author by id: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_authors_with_book_count():
    try:
        coll = get_collection("authors")
        pipeline = authors_with_book_count_pipeline()
        results = list(coll.aggregate(pipeline))
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")
