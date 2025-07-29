from fastapi import APIRouter, Query
from fastapi import Request
from models.book import Book
from utils.security import validateadmin
from bson import json_util
import json
from controllers.book import (
    create_book,
    get_all_books,
    get_book_by_id,
    update_book,
    delete_book,
    get_books_filtered
    
)

from pipelines.book_pipeline import (
    get_books_with_author_pipeline,
    count_books_by_genre_pipeline
)

from utils.mongodb import get_collection

books_coll = get_collection("books")

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/filtered")
async def get_filtered_books(
    title: str = Query(default=None, description="Filtrar por titulo"),
    genre: str = Query(default=None, description="Filtrar por genero"),
    skip: int = Query(default=0, ge=0, description="Numero de libros a omitir"),
    limit: int = Query(default=10, ge=1, le=100, description="Número de libros a retornar")
):
    books = await get_books_filtered(title, genre, skip, limit)
    return books

@router.get("/books dets.")
async def get_books_with_authors(skip: int = 0, limit: int = 10):
    pipeline = get_books_with_author_pipeline(skip, limit)
    books = list(books_coll.aggregate(pipeline))
    return json.loads(json_util.dumps(books))

@router.get("/stats/genres")
async def count_books_by_genre():
    pipeline = count_books_by_genre_pipeline()
    stats = list(books_coll.aggregate(pipeline))
    return stats

@router.post("/", response_model=Book)
@validateadmin
async def create_book_route(request:Request,  book: Book):
    return await create_book(book)

@router.get("/", response_model=list[Book])
async def get_books_route():
    return await get_all_books()

@router.get("/{book_id}", response_model=Book)
async def get_book_by_id_route(book_id: str):
    return await get_book_by_id(book_id)

@router.put("/{book_id}", response_model=Book)
@validateadmin
async def update_book_route(request: Request, book_id: str, book: Book):
    return await update_book(book_id, book)

@router.delete("/{book_id}")
@validateadmin
async def delete_book_route(request: Request, book_id: str):
    return await delete_book(book_id)
