from typing import Annotated
from typing import Literal

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.dates import today_local
from app.core.security import CurrentDomiciliario, get_current_domiciliario
from app.db.session import get_db
from app.schemas.auth import (
    DomiciliarioDesempenoResponse,
    DomiciliarioDocumentosResponse,
    DomiciliarioFotoRequest,
    DomiciliarioLoginRequest,
    DomiciliarioLoginResponse,
    DomiciliarioPerfilHomeResponse,
    DomiciliarioPerfilResponse,
    DomiciliarioSoporteResponse,
    DomiciliarioVehiculoResponse,
)
from app.services.auth import (
    actualizar_foto_domiciliario,
    login_domiciliario,
    obtener_desempeno_domiciliario,
    obtener_documentos_domiciliario,
    obtener_perfil_home_domiciliario,
    obtener_perfil_domiciliario,
    obtener_soporte_domiciliario,
    obtener_vehiculo_perfil,
    subir_y_actualizar_foto_domiciliario,
)


router = APIRouter()


def _rango_periodo(periodo: Literal["hoy", "semana", "mes", "anio", "todos"]):
    from datetime import timedelta

    hoy = today_local()
    if periodo == "hoy":
        return hoy, hoy
    if periodo == "semana":
        return hoy - timedelta(days=hoy.weekday()), hoy
    if periodo == "mes":
        return hoy.replace(day=1), hoy
    if periodo == "anio":
        return hoy.replace(month=1, day=1), hoy
    return None, None


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


@router.get("/domiciliarios/me/perfil", response_model=DomiciliarioPerfilHomeResponse)
def perfil_home_domiciliario(
    domiciliario: Annotated[CurrentDomiciliario, Depends(get_current_domiciliario)],
    db: Session = Depends(get_db),
) -> dict:
    return obtener_perfil_home_domiciliario(db, domiciliario, today_local())


@router.get("/domiciliarios/me/desempeno", response_model=DomiciliarioDesempenoResponse)
def desempeno_domiciliario(
    domiciliario: Annotated[CurrentDomiciliario, Depends(get_current_domiciliario)],
    periodo: Literal["hoy", "semana", "mes", "anio", "todos"] = "mes",
    db: Session = Depends(get_db),
) -> dict:
    fecha_desde, fecha_hasta = _rango_periodo(periodo)
    return obtener_desempeno_domiciliario(
        db,
        domiciliario,
        periodo=periodo,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
    )


@router.get("/domiciliarios/me/documentos", response_model=DomiciliarioDocumentosResponse)
def documentos_domiciliario(
    domiciliario: Annotated[CurrentDomiciliario, Depends(get_current_domiciliario)],
    db: Session = Depends(get_db),
) -> dict:
    return obtener_documentos_domiciliario(db, domiciliario)


@router.get("/domiciliarios/me/vehiculo", response_model=DomiciliarioVehiculoResponse)
def vehiculo_domiciliario(
    domiciliario: Annotated[CurrentDomiciliario, Depends(get_current_domiciliario)],
    db: Session = Depends(get_db),
) -> dict:
    return obtener_vehiculo_perfil(db, domiciliario)


@router.get("/domiciliarios/me/soporte", response_model=DomiciliarioSoporteResponse)
def soporte_domiciliario(
    domiciliario: Annotated[CurrentDomiciliario, Depends(get_current_domiciliario)],
    db: Session = Depends(get_db),
) -> dict:
    return obtener_soporte_domiciliario(db, domiciliario)


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
