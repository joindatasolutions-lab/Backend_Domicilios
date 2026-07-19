from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db


router = APIRouter()


@router.get("")
def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.app_env}


@router.get("/db")
def database_health(db: Session = Depends(get_db)) -> dict[str, str]:
    db.execute(text("select 1"))
    return {"status": "ok", "database": settings.db_name, "schema": settings.db_schema}
