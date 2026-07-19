from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dates import today_local
from app.core.security import CurrentDomiciliario, get_current_domiciliario
from app.core.tenant import TenantContext, get_tenant_context
from app.db.session import get_db
from app.schemas.pedidos import (
    PedidoEntregadoRequest,
    PedidoAsignadoResponse,
    PedidoDevueltoResponse,
    PedidoDisponible,
    PedidoEstadoResponse,
    PedidoNoEntregadoRequest,
    PedidoNovedadRequest,
)
from app.services.pedidos import (
    asignar_pedido_a_domiciliario,
    devolver_pedido_asignado,
    entregar_pedido,
    iniciar_entrega_pedido,
    listar_pedidos_asignados,
    listar_pedidos_disponibles,
    marcar_pedido_no_entregado,
)


router = APIRouter()


TIPOS_NOVEDAD = {
    "cliente_no_disponible": "Cliente no disponible",
    "direccion_incorrecta": "Direccion incorrecta",
    "rechazado_por_cliente": "Rechazado por el cliente",
    "arreglo_danado": "Arreglo danado",
    "otra_novedad": "Otra novedad",
}


@router.get("/disponibles", response_model=list[PedidoDisponible])
def pedidos_disponibles(
    tenant: Annotated[TenantContext, Depends(get_tenant_context)],
    fecha: Annotated[
        date | None,
        Query(description="Fecha de entrega en formato YYYY-MM-DD. Por defecto usa la fecha actual."),
    ] = None,
    limit: Annotated[int, Query(gt=0, le=500)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
    db: Session = Depends(get_db),
) -> list[dict]:
    fecha = fecha or today_local()

    return listar_pedidos_disponibles(
        db,
        empresa_id=tenant.empresa_id,
        sucursal_id=tenant.sucursal_id,
        fecha=fecha,
        limit=limit,
        offset=offset,
    )


@router.get("/asignados", response_model=list[PedidoDisponible])
def pedidos_asignados(
    domiciliario: Annotated[CurrentDomiciliario, Depends(get_current_domiciliario)],
    fecha: Annotated[
        date | None,
        Query(description="Fecha de entrega en formato YYYY-MM-DD. Por defecto usa la fecha actual."),
    ] = None,
    limit: Annotated[int, Query(gt=0, le=500)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
    db: Session = Depends(get_db),
) -> list[dict]:
    fecha = fecha or today_local()
    return listar_pedidos_asignados(
        db,
        domiciliario=domiciliario,
        fecha=fecha,
        limit=limit,
        offset=offset,
    )


@router.post("/{numero_pedido}/asignarme", response_model=PedidoAsignadoResponse)
def asignarme_pedido(
    numero_pedido: int,
    domiciliario: Annotated[CurrentDomiciliario, Depends(get_current_domiciliario)],
    sucursal_id: Annotated[int | None, Query(gt=0)] = None,
    db: Session = Depends(get_db),
) -> dict:
    resultado = asignar_pedido_a_domiciliario(
        db,
        numero_pedido=numero_pedido,
        domiciliario=domiciliario,
        sucursal_id=sucursal_id,
    )

    if resultado["status"] == "not_found":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=resultado["message"],
        )
    if resultado["status"] == "ambiguous":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=resultado["message"],
        )
    return resultado


@router.post("/{numero_pedido}/devolver", response_model=PedidoDevueltoResponse)
def devolver_pedido(
    numero_pedido: int,
    domiciliario: Annotated[CurrentDomiciliario, Depends(get_current_domiciliario)],
    sucursal_id: Annotated[int | None, Query(gt=0)] = None,
    db: Session = Depends(get_db),
) -> dict:
    resultado = devolver_pedido_asignado(
        db,
        numero_pedido=numero_pedido,
        domiciliario=domiciliario,
        sucursal_id=sucursal_id,
    )

    if resultado["status"] == "not_found":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=resultado["message"],
        )
    if resultado["status"] == "ambiguous":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=resultado["message"],
        )
    return resultado


@router.post("/{numero_pedido}/iniciar-entrega", response_model=PedidoEstadoResponse)
def iniciar_entrega(
    numero_pedido: int,
    domiciliario: Annotated[CurrentDomiciliario, Depends(get_current_domiciliario)],
    sucursal_id: Annotated[int | None, Query(gt=0)] = None,
    db: Session = Depends(get_db),
) -> dict:
    resultado = iniciar_entrega_pedido(
        db,
        numero_pedido=numero_pedido,
        domiciliario=domiciliario,
        sucursal_id=sucursal_id,
    )

    if resultado["status"] == "not_found":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=resultado["message"],
        )
    if resultado["status"] == "ambiguous":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=resultado["message"],
        )
    if resultado["status"] == "invalid_transition":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=resultado["message"],
        )
    return resultado


@router.post("/{numero_pedido}/entregar", response_model=PedidoEstadoResponse)
def entregar(
    numero_pedido: int,
    payload: PedidoEntregadoRequest,
    domiciliario: Annotated[CurrentDomiciliario, Depends(get_current_domiciliario)],
    sucursal_id: Annotated[int | None, Query(gt=0)] = None,
    db: Session = Depends(get_db),
) -> dict:
    resultado = entregar_pedido(
        db,
        numero_pedido=numero_pedido,
        domiciliario=domiciliario,
        sucursal_id=sucursal_id,
        firma_nombre=payload.firma_nombre,
        firma_documento=payload.firma_documento,
        firma_imagen_url=payload.firma_imagen_url,
        evidencia_foto_url=payload.evidencia_foto_url,
        observaciones=payload.observaciones,
    )

    if resultado["status"] == "not_found":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=resultado["message"],
        )
    if resultado["status"] == "ambiguous":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=resultado["message"],
        )
    if resultado["status"] == "invalid_transition":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=resultado["message"],
        )
    return resultado


@router.post("/{numero_pedido}/no-entregado", response_model=PedidoEstadoResponse)
def no_entregado(
    numero_pedido: int,
    payload: PedidoNoEntregadoRequest,
    domiciliario: Annotated[CurrentDomiciliario, Depends(get_current_domiciliario)],
    sucursal_id: Annotated[int | None, Query(gt=0)] = None,
    db: Session = Depends(get_db),
) -> dict:
    resultado = marcar_pedido_no_entregado(
        db,
        numero_pedido=numero_pedido,
        domiciliario=domiciliario,
        sucursal_id=sucursal_id,
        motivo=payload.motivo,
        evidencia_foto_url=payload.evidencia_foto_url,
        observaciones=payload.observaciones,
    )

    if resultado["status"] == "not_found":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=resultado["message"],
        )
    if resultado["status"] == "ambiguous":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=resultado["message"],
        )
    if resultado["status"] == "invalid_transition":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=resultado["message"],
        )
    return resultado


@router.post("/{numero_pedido}/novedad", response_model=PedidoEstadoResponse)
def reportar_novedad(
    numero_pedido: int,
    payload: PedidoNovedadRequest,
    domiciliario: Annotated[CurrentDomiciliario, Depends(get_current_domiciliario)],
    sucursal_id: Annotated[int | None, Query(gt=0)] = None,
    db: Session = Depends(get_db),
) -> dict:
    motivo = TIPOS_NOVEDAD[payload.tipo_novedad]
    observaciones = payload.descripcion
    resultado = marcar_pedido_no_entregado(
        db,
        numero_pedido=numero_pedido,
        domiciliario=domiciliario,
        sucursal_id=sucursal_id,
        motivo=motivo,
        evidencia_foto_url=payload.evidencia_foto_url,
        observaciones=observaciones,
        detalle_extra={
            "tipo_novedad": payload.tipo_novedad,
            "descripcion": payload.descripcion,
        },
    )

    if resultado["status"] == "not_found":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=resultado["message"],
        )
    if resultado["status"] == "ambiguous":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=resultado["message"],
        )
    if resultado["status"] == "invalid_transition":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=resultado["message"],
        )
    return resultado
