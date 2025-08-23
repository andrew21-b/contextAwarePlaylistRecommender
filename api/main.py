from fastapi import FastAPI
from context.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)


@app.get("/")
def root():
    return {"message": settings.PROJECT_NAME, "status": "running"}
