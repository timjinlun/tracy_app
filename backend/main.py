# backend/main.py

from fastapi import FastAPI
from app.core.config import settings
from app.api.api_v1.api import api_router
from app.db.session import engine
from app.db.base_class import Base

app = FastAPI(title=settings.PROJECT_NAME)
# Create database tables
Base.metadata.create_all(bind=engine)


# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)