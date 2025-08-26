from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.context.config import settings
from api.controller.routes import api_router

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {"message": settings.PROJECT_NAME, "status": "running"}
