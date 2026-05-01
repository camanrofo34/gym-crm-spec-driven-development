from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.routes.activities import router as activities_router
from src.api.routes.analytics import router as analytics_router
from src.api.routes.assignments import router as assignments_router
from src.api.routes.auth import router as auth_router
from src.api.routes.users import router as users_router
from src.db.database import init_db

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


app = FastAPI(title="Gym Analytics Management API", version="1.0.0", lifespan=lifespan)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(assignments_router)
app.include_router(activities_router)
app.include_router(analytics_router)
