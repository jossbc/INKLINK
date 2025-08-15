import uvicorn
import logging
import os
from fastapi import FastAPI

from routes.book import router as books_router
from routes.author import router as authors_router
from routes.publisher import router as publisher_router
from controllers.users import create_user, login
from models.login import Login
from models.users import User

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="InkLink API", version="1.0")

# Add CORS
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
def read_root():
    return {"status": "healthy", "version": "0.0.0", "service": "inklink-api"}

@app.get("/health")
def health_check():
    try:
        return {
            "status": "healthy", 
            "timestamp": "2025-08-02", 
            "service": "inklink-api",
            "environment": "production"
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/ready")
def readiness_check():
    try:
        from utils.mongodb import test_connection
        db_status = test_connection()
        return {
            "status": "ready" if db_status else "not_ready",
            "database": "connected" if db_status else "disconnected",
            "service": "inklink-api"
        }
    except Exception as e:
        return {"status": "not_ready", "error": str(e)}
    
@app.post("/users")
async def create_user_endpoint(user: User) -> User:
    return await create_user(user)

@app.post("/login")
async def login_access(l: Login) -> dict:
    return await login(l)

app.include_router(authors_router)
app.include_router(publisher_router)
app.include_router(books_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)