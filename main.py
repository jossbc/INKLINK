import uvicorn
import logging
import os
from fastapi import FastAPI

from routes.book import router as books_router
from routes.author import router as authors_router
from routes.publisher import router as publisher_router
from routes.user import router as user_router
from routes.login import router as login_router

from dotenv import load_dotenv
load_dotenv()

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("secrets/inklink-firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

app = FastAPI(title="InkLink API", version="1.0")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
def read_root():
    return {"version": "0.0.0"}

app.include_router(user_router)
app.include_router(login_router)
app.include_router(authors_router)
app.include_router(publisher_router)
app.include_router(books_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)