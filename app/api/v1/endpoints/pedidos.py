from datetime import date, timedelta
from typing import Annotated
from typing import Literal

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
    PedidoHistorial,
    PedidoNovedadItem,
    PedidoNovedadResolverRequest,
    PedidoNovedadResolverResponse,
    PedidoNoEntregadoRequest,
    PedidoNovedadRequest,
)
from app.services.pedidos import (
    asignar_pedido_a_domiciliario,
    devolver_pedido_asignado,
    entregar_pedido,
    iniciar_entrega_pedido,
    listar_historial_pedidos,
    listar_novedades_pedidos,
    listar_pedidos_asignados,
    listar_pedidos_disponibles,
    marcar_pedido_no_entregado,
    registrar_novedad_operativa,
    resolver_novedad_pedido,
)


router = APIRouter()


TIPOS_NOVEDAD = {
    "cliente_no_disponible": "Cliente no disponible",
    "direccion_incorrecta": "Direccion incorrecta",
    "rechazado_por_cliente": "Rechazado por el cliente",
    "arreglo_danado": "Arreglo danado",
    "otra_novedad": "Otra novedad",
}


def _rango_periodo(periodo: Literal["hoy", "semana", "mes", "anio", "todos"]) -> tuple[date | None, date | None]:
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


@router.get("/historial", response_model=list[PedidoHistorial])
def historial_pedidos(
    domiciliario: Annotated[CurrentDomiciliario, Depends(get_current_domiciliario)],
    periodo: Annotated[
        Literal["hoy", "semana", "mes", "anio", "todos"],
        Query(description="Filtro rapido: hoy, semana, mes, anio o todos."),
    ] = "hoy",
    q: Annotated[
        str | None,
        Query(description="Busqueda por numero de pedido, cliente o arreglo.", max_length=120),
    ] = None,
    limit: Annotated[int, Query(gt=0, le=500)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
    db: Session = Depends(get_db),
) -> list[dict]:
    fecha_desde, fecha_hasta = _rango_periodo(periodo)

    return listar_historial_pedidos(
        db,
        domiciliario=domiciliario,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        q=q,
        limit=limit,
        offset=offset,
    )


@router.get("/novedades", response_model=list[PedidoNovedadItem])
def novedades_pedidos(
    domiciliario: Annotated[CurrentDomiciliario, Depends(get_current_domiciliario)],
    estado: Annotated[
        Literal["abierta", "resuelta", "todas"],
        Query(description="Estado de la novedad: abierta, resuelta o todas."),
    ] = "abierta",
    periodo: Annotated[
        Literal["hoy", "semana", "mes", "anio", "todos"],
        Query(description="Filtro rapido: hoy, semana, mes, anio o todos."),
    ] = "hoy",
    q: Annotated[
        str | None,
        Query(description="Busqueda por numero de pedido, cliente o arreglo.", max_length=120),
    ] = None,
    limit: Annotated[int, Query(gt=0, le=500)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
    db: Session = Depends(get_db),
) -> list[dict]:
    fecha_desde, fecha_hasta = _rango_periodo(periodo)
    return listar_novedades_pedidos(
        db,
        domiciliario=domiciliario,
        estado=estado,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        q=q,
        limit=limit,
        offset=offset,
    )


@router.get("/{numero_pedido}/novedades", response_model=list[PedidoNovedadItem])
def novedades_pedido_detalle(
    numero_pedido: int,
    domiciliario: Annotated[CurrentDomiciliario, Depends(get_current_domiciliario)],
    estado: Annotated[
        Literal["abierta", "resuelta", "todas"],
        Query(description="Estado de la novedad: abierta, resuelta o todas."),
    ] = "todas",
    limit: Annotated[int, Query(gt=0, le=500)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
    db: Session = Depends(get_db),
) -> list[dict]:
    return listar_novedades_pedidos(
        db,
        domiciliario=domiciliario,
        estado=estado,
        numero_pedido=numero_pedido,
        limit=limit,
        offset=offset,
    )


@router.post("/{numero_pedido}/novedades/{id_novedad}/resolver", response_model=PedidoNovedadResolverResponse)
def resolver_novedad(
    numero_pedido: int,
    id_novedad: int,
    payload: PedidoNovedadResolverRequest,
    domiciliario: Annotated[CurrentDomiciliario, Depends(get_current_domiciliario)],
    db: Session = Depends(get_db),
) -> dict:
    resultado = resolver_novedad_pedido(
        db,
        numero_pedido=numero_pedido,
        id_novedad=id_novedad,
        domiciliario=domiciliario,
        solucion=payload.solucion,
        observaciones=payload.observaciones,
        nuevo_estado_pedido=payload.nuevo_estado_pedido,
        evidencia_foto_url=payload.evidencia_foto_url,
        firma_nombre=payload.firma_nombre,
        firma_documento=payload.firma_documento,
        firma_imagen_url=payload.firma_imagen_url,
    )

    if resultado["status"] == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=resultado["message"],
        )
    if resultado["status"] == "invalid_transition":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=resultado["message"],
        )
    return resultado


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
    novedad = registrar_novedad_operativa(
        db,
        resultado_estado=resultado,
        domiciliario=domiciliario,
        tipo_novedad=payload.tipo_novedad,
        motivo=motivo,
        descripcion=payload.descripcion,
        evidencia_foto_url=payload.evidencia_foto_url,
    )
    resultado["id_novedad"] = novedad["id_novedad"]
    resultado["estado_novedad"] = novedad["estado"]
    return resultado
