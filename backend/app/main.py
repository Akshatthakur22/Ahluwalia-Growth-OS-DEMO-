from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.api.v1 import (
    auth, users, attendance, sites, contacts, meetings,
    assignments, showroom_visits, opportunities, search, dashboard, audit,
)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

app.add_middleware(GZipMiddleware, minimum_size=500)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_uploads = Path(__file__).resolve().parents[1] / "uploads"
_uploads.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(_uploads)), name="uploads")

# Include routers
app.include_router(auth.router, prefix=f"{settings.api_v1_prefix}/auth", tags=["authentication"])
app.include_router(users.router, prefix=f"{settings.api_v1_prefix}/users", tags=["users"])
app.include_router(attendance.router, prefix=f"{settings.api_v1_prefix}/attendance", tags=["attendance"])
app.include_router(sites.router, prefix=f"{settings.api_v1_prefix}/sites", tags=["sites"])
app.include_router(contacts.router, prefix=f"{settings.api_v1_prefix}/contacts", tags=["contacts"])
app.include_router(meetings.router, prefix=f"{settings.api_v1_prefix}/meetings", tags=["meetings"])
app.include_router(assignments.router, prefix=f"{settings.api_v1_prefix}/assignments", tags=["assignments"])
app.include_router(showroom_visits.router, prefix=f"{settings.api_v1_prefix}/showroom-visits", tags=["showroom-visits"])
app.include_router(opportunities.router, prefix=f"{settings.api_v1_prefix}/opportunities", tags=["opportunities"])
app.include_router(search.router, prefix=f"{settings.api_v1_prefix}/search", tags=["search"])
app.include_router(dashboard.router, prefix=f"{settings.api_v1_prefix}/dashboard", tags=["dashboard"])
app.include_router(audit.router, prefix=f"{settings.api_v1_prefix}/audit", tags=["audit"])


@app.get("/")
def root():
    """
    Root endpoint.
    """
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "status": "operational"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}
