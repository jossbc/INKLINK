def authors_with_book_count_pipeline():
    return [
        {
            "$lookup": {
                "from": "books",
                "localField": "_id",
                "foreignField": "author_id",
                "as": "books"
            }
        },
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "name": "$name",
                "lastname": "$lastname",
                "num_books": {"$size": "$books"}
            }
        }
    ]
