import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import parking, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Retry DB connection in case postgres is still starting up
    for attempt in range(10):
        try:
            Base.metadata.create_all(bind=engine)
            break
        except Exception:
            if attempt < 9:
                print(f"DB not ready, retrying in 2s (attempt {attempt + 1}/10)...")
                time.sleep(2)
            else:
                raise
    yield


app = FastAPI(
    title="Smart Parking Finder API",
    description="Real-time parking availability for Atlanta",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(parking.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"message": "Smart Parking Finder API", "docs": "/docs"}
