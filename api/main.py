from fastapi import FastAPI
from api.context.config import settings
from api.controller.routes import api_router

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {"message": settings.PROJECT_NAME, "status": "running"}
