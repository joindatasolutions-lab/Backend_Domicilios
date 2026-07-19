import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("")
def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.app_env}


@router.get("/db")
def database_health(db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        db.execute(text("select 1"))
    except SQLAlchemyError as exc:
        logger.exception(
            "Database health check failed for target %s",
            settings.database_connection_target,
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo conectar con la base de datos",
        ) from exc
    return {"status": "ok", "database": settings.db_name, "schema": settings.db_schema}
