from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import create_db_and_tables
from app.routers import notes, tags


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create DB tables on startup (idempotent – safe to run every time)."""
    create_db_and_tables()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="A single-user note-taking API with tags and markdown support.",
    version="0.1.0",
    lifespan=lifespan,
)

# Allow all origins during development so any frontend (Vite, Next.js, etc.)
# can talk to the API without CORS errors.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes.router, prefix="/api")
app.include_router(tags.router, prefix="/api")


@app.get("/", include_in_schema=False)
def root():
    return {"message": f"Welcome to {settings.APP_NAME} API", "docs": "/docs"}
