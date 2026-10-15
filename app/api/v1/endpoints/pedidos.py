from datetime import date, timedelta
from json import JSONDecodeError
from typing import Annotated
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Request, UploadFile, status
from fastapi.exceptions import RequestValidationError
from starlette.concurrency import run_in_threadpool
from pydantic import ValidationError
from sqlalchemy import text
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
from app.services.storage import subir_foto_novedad_pedido, subir_evidencia_entrega_pedido, _extension_imagen


router = APIRouter()


TIPOS_NOVEDAD = {
    "cliente_no_disponible": "Cliente no disponible",
    "direccion_incorrecta": "Direccion incorrecta",
    "rechazado_por_cliente": "Rechazado por el cliente",
    "arreglo_danado": "Arreglo danado",
    "otra_novedad": "Otra novedad",
}

EVIDENCIA_MULTIPART_FIELDS = ("foto", "evidencia", "evidencia_foto", "evidencia_foto_url")


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


def _obtener_tenant_slug(db: Session, empresa_id: int) -> str:
    slug = db.execute(
        text(
            """
            select slug
            from empresa
            where id_empresa = :empresa_id
            limit 1
            """
        ),
        {"empresa_id": empresa_id},
    ).scalar_one_or_none()
    return slug or f"empresa-{empresa_id}"


def _archivo_evidencia_desde_form(form) -> UploadFile | None:
    for field_name in EVIDENCIA_MULTIPART_FIELDS:
        value = form.get(field_name)
        if hasattr(value, "file") and getattr(value, "filename", None):
            return value
    return None


async def _payload_novedad_desde_request(
    request: Request,
    *,
    db: Session,
    domiciliario: CurrentDomiciliario,
    numero_pedido: int,
) -> PedidoNovedadRequest:
    content_type = request.headers.get("content-type", "").lower()
    if "multipart/form-data" not in content_type and "application/x-www-form-urlencoded" not in content_type:
        try:
            return PedidoNovedadRequest.model_validate(await request.json())
        except ValidationError as exc:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.errors()) from exc

    form = await request.form()
    evidencia_foto_url = form.get("evidencia_foto_url")
    evidencia_file = _archivo_evidencia_desde_form(form)
    if evidencia_file is not None:
        tenant_slug = _obtener_tenant_slug(db, domiciliario.empresa_id)
        _, evidencia_foto_url = subir_foto_novedad_pedido(
            tenant_slug=tenant_slug,
            numero_pedido=numero_pedido,
            file=evidencia_file,
        )

    try:
        return PedidoNovedadRequest.model_validate(
            {
                "tipo_novedad": form.get("tipo_novedad"),
                "descripcion": form.get("descripcion"),
                "evidencia_foto_url": evidencia_foto_url,
            }
        )
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.errors()) from exc


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


async def _payload_entrega_desde_request(
    request: Request, *, db: Session, domiciliario: CurrentDomiciliario,
    numero_pedido: int,
) -> PedidoEntregadoRequest:
    content_type = request.headers.get("content-type", "").lower()
    try:
        if "multipart/form-data" not in content_type and "application/x-www-form-urlencoded" not in content_type:
            return PedidoEntregadoRequest.model_validate(await request.json())

        async with request.form() as form:
            data = dict(form)
            archivos = {}
            for field, target in (("foto", "evidencia_foto_url"), ("firma", "firma_imagen_url")):
                archivo = form.get(field)
                if archivo is not None:
                    if not hasattr(archivo, "file") or not getattr(archivo, "filename", None):
                        raise HTTPException(status_code=422, detail=f"{field} debe ser un archivo")
                    _extension_imagen(archivo)
                    archivos[field] = (target, archivo)
            payload = PedidoEntregadoRequest.model_validate(data)
            if archivos:
                tenant_slug = await run_in_threadpool(_obtener_tenant_slug, db, domiciliario.empresa_id)
                for tipo, (target, archivo) in archivos.items():
                    _, url = await run_in_threadpool(
                        subir_evidencia_entrega_pedido,
                        tenant_slug=tenant_slug, numero_pedido=numero_pedido,
                        file=archivo, tipo=tipo,
                    )
                    setattr(payload, target, url)
            return payload
    except ValidationError as exc:
        raise RequestValidationError(exc.errors()) from exc
    except JSONDecodeError as exc:
        raise HTTPException(status_code=422, detail="El cuerpo debe ser JSON valido o multipart/form-data") from exc


@router.post(
    "/{numero_pedido}/entregar", response_model=PedidoEstadoResponse,
    openapi_extra={"requestBody": {"required": True, "content": {
        "application/json": {"schema": PedidoEntregadoRequest.model_json_schema()},
        "multipart/form-data": {"schema": {
            **PedidoEntregadoRequest.model_json_schema(),
            "properties": {
                **PedidoEntregadoRequest.model_json_schema()["properties"],
                "foto": {"type": "string", "format": "binary"},
                "firma": {"type": "string", "format": "binary"},
            },
        }},
    }}},
)
async def entregar(
    numero_pedido: int,
    request: Request,
    domiciliario: Annotated[CurrentDomiciliario, Depends(get_current_domiciliario)],
    sucursal_id: Annotated[int | None, Query(gt=0)] = None,
    db: Session = Depends(get_db),
) -> dict:
    payload = await _payload_entrega_desde_request(
        request, db=db, domiciliario=domiciliario, numero_pedido=numero_pedido,
    )
    resultado = await run_in_threadpool(
        entregar_pedido,
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
async def reportar_novedad(
    numero_pedido: int,
    request: Request,
    domiciliario: Annotated[CurrentDomiciliario, Depends(get_current_domiciliario)],
    sucursal_id: Annotated[int | None, Query(gt=0)] = None,
    db: Session = Depends(get_db),
) -> dict:
    payload = await _payload_novedad_desde_request(
        request,
        db=db,
        domiciliario=domiciliario,
        numero_pedido=numero_pedido,
    )
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
