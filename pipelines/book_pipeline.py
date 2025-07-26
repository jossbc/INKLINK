from bson import ObjectId

def get_books_with_author_pipeline(skip: int = 0, limit: int = 10) -> list:
    return [
        {
            "$addFields": {
                "author_obj_id": {"$toObjectId": "$author_id"}
            }
        },
        {
            "$lookup": {
                "from": "authors",
                "localField": "author_obj_id",
                "foreignField": "_id",
                "as": "author"
            }
        },
        {"$unwind": "$author"},
        {"$project": {
            "id": {"$toString": "$_id"},
            "title": 1,
            "publication_year": 1,
            "genre": 1,
            "author": {
                "id": {"$toString": "$author._id"},
                "name": "$author.name",
                "lastname": "$author.lastname"
            }
        }},
        {"$skip": skip},
        {"$limit": limit}
    ]
def count_books_by_genre_pipeline():
    return [
        {"$group": {
            "_id": "$genre",
            "total": {"$sum": 1}
        }},
        {"$sort": {"total": -1}},
        {"$project": {
            "genre": "$_id",
            "total_books": "$total",
            "_id": 0
        }}
    ]
def validate_author_exists_pipeline(author_id: str) -> list:
    return [
        {"$match": {
            "_id": ObjectId(author_id)
        }},
        {"$project": {
            "id": {"$toString": "$_id"},
            "name": 1,
            "lastname": 1
        }}
    ]
