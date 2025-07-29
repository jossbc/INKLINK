from fastapi import HTTPException
from models.book import Book
from utils.mongodb import get_collection
from bson import ObjectId
from pipelines.author_pipeline import validate_author_exists_pipeline
  
coll = get_collection("books")
authors_coll = get_collection("authors")

async def create_book(book: Book) -> Book:
    try:
        pipeline = validate_author_exists_pipeline(book.author_id)
        author_result = list(authors_coll.aggregate(pipeline))
        if not author_result:
            raise HTTPException(status_code=400, detail="Autor no encontrado")

        book.title = book.title.strip()

        existing = coll.find_one({"title": {"$regex": f"^{book.title}$", "$options": "i"}})
        if existing:
            raise HTTPException(status_code=400, detail="Ya existe un libro con este título")

        book_dict = book.model_dump(exclude={"id"})
        inserted = coll.insert_one(book_dict)
        book.id = str(inserted.inserted_id)
        return book

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear libro: {str(e)}")

async def get_all_books() -> list[Book]:
    try:
        books = []
        for doc in coll.find():
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            books.append(Book(**doc))
        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener libros: {str(e)}")

async def get_book_by_id(book_id: str) -> Book:
    try:
        doc = coll.find_one({"_id": ObjectId(book_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        return Book(**doc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar libro: {str(e)}")

async def update_book(book_id: str, book: Book) -> Book:
    try:
        pipeline = validate_author_exists_pipeline(book.author_id)
        author_result = list(authors_coll.aggregate(pipeline))
        if not author_result:
            raise HTTPException(status_code=400, detail="Autor no encontrado")

        book.title = book.title.strip()

        duplicate = coll.find_one({
            "title": {"$regex": f"^{book.title}$", "$options": "i"},
            "_id": {"$ne": ObjectId(book_id)}
        })
        if duplicate:
            raise HTTPException(status_code=400, detail="Otro libro con este título ya existe")

        result = coll.update_one(
            {"_id": ObjectId(book_id)},
            {"$set": book.model_dump(exclude={"id"})}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Libro no encontrado")

        return await get_book_by_id(book_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar libro: {str(e)}")

async def delete_book(book_id: str):
    try:
        book = coll.find_one({"_id": ObjectId(book_id)})
        if not book:
            raise HTTPException(status_code=404, detail="Libro no encontrado")

        result = coll.delete_one({"_id": ObjectId(book_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        return {"message": "Libro eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar libro: {str(e)}")

async def get_books_filtered(title=None, genre=None, skip=0, limit=10):
    try:
        query = {}

        if title:
            query["title"] = {"$regex": title, "$options": "i"}

        if genre:
            query["genre"] = {"$regex": genre, "$options": "i"}

        docs = coll.find(query).skip(skip).limit(limit)
        books = []
        for doc in docs:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            books.append(Book(**doc))
        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al filtrar libros: {str(e)}")