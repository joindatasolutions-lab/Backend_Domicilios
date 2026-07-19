from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.security import CurrentDomiciliario, get_current_domiciliario
from app.db.session import get_db
from app.schemas.auth import (
    DomiciliarioFotoRequest,
    DomiciliarioLoginRequest,
    DomiciliarioLoginResponse,
    DomiciliarioPerfilResponse,
)
from app.services.auth import (
    actualizar_foto_domiciliario,
    login_domiciliario,
    obtener_perfil_domiciliario,
    subir_y_actualizar_foto_domiciliario,
)


router = APIRouter()


@router.post("/domiciliarios/login", response_model=DomiciliarioLoginResponse)
def login_domiciliarios(
    credentials: DomiciliarioLoginRequest,
    db: Session = Depends(get_db),
) -> dict:
    return login_domiciliario(db, credentials)


@router.get("/domiciliarios/me", response_model=DomiciliarioPerfilResponse)
def perfil_domiciliario(
    domiciliario: Annotated[CurrentDomiciliario, Depends(get_current_domiciliario)],
    db: Session = Depends(get_db),
) -> dict:
    return obtener_perfil_domiciliario(db, domiciliario)


@router.patch("/domiciliarios/me/foto", response_model=DomiciliarioPerfilResponse)
def actualizar_foto(
    payload: DomiciliarioFotoRequest,
    domiciliario: Annotated[CurrentDomiciliario, Depends(get_current_domiciliario)],
    db: Session = Depends(get_db),
) -> dict:
    return actualizar_foto_domiciliario(
        db,
        domiciliario=domiciliario,
        foto_url=payload.foto_url,
    )


@router.post("/domiciliarios/me/foto", response_model=DomiciliarioPerfilResponse)
def subir_foto(
    domiciliario: Annotated[CurrentDomiciliario, Depends(get_current_domiciliario)],
    foto: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> dict:
    return subir_y_actualizar_foto_domiciliario(
        db,
        domiciliario=domiciliario,
        file=foto,
    )
