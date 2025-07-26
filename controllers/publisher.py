import logging
from fastapi import HTTPException
from models.publisher import Publisher
from utils.mongodb import get_collection
from bson import ObjectId

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_publisher(publisher: Publisher) -> Publisher:
    try:
        coll = get_collection("publishers")

        existing = coll.find_one({
            "name": {
                "$regex": f"^{publisher.name}$",
                "$options": "i"
            }
        })

        if existing:
            raise HTTPException(status_code=400, detail="Ya existe un publisher con este nombre")

        publisher_dict = publisher.model_dump(exclude={"id"})
        inserted = coll.insert_one(publisher_dict)
        publisher.id = str(inserted.inserted_id)
        return publisher
    except Exception as e:
        logger.error(f"Error creating publisher: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_all_publishers() -> list[Publisher]:
    try:
        coll = get_collection("publishers")
        publishers = []
        for doc in coll.find():
            doc["id"] = str(doc["_id"])
            publishers.append(Publisher(**doc))
        return publishers
    except Exception as e:
        logger.error(f"Error fetching publishers: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_publisher_by_id(publisher_id: str) -> Publisher:
    try:
        coll = get_collection("publishers")
        doc = coll.find_one({"_id": ObjectId(publisher_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Publisher no encontrado")
        doc["id"] = str(doc["_id"])
        return Publisher(**doc)
    except Exception as e:
        logger.error(f"Error fetching publisher by id: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
