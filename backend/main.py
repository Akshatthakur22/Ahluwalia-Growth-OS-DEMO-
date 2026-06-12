"""Entrypoint for `uvicorn main:app` (Render default start command)."""
from app.main import app

__all__ = ["app"]
