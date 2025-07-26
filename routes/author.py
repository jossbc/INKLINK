from fastapi import APIRouter
from models.author import Author
from utils.security import validateadmin
from controllers.author import (
    create_author,
    get_all_authors,
    get_author_by_id,
)
from utils.security import validateadmin
from controllers.author import get_authors_with_book_count

router = APIRouter(prefix="/authors", tags=["authors"])

@router.get("/", response_model=list[Author])
async def endpoint_get_all_authors():
    return await get_all_authors()

@router.post("/", response_model=Author)
@validateadmin
async def endpoint_create_author(author: Author):
    return await create_author(author)

@router.get("/stats/books") 
async def authors_book_count():
    return await get_authors_with_book_count()

@router.get("/{author_id}", response_model=Author)
async def endpoint_get_author_by_id(author_id: str):
    return await get_author_by_id(author_id)
