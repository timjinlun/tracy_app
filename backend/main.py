# backend/main.py

from fastapi import FastAPI
from app.core.config import settings
from app.db.session import engine
from app.db.base_class import Base

app = FastAPI(title=settings.PROJECT_NAME)
Base.metadata.create_all(bind=engine)
@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)