import json
from datetime import date

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.security import CurrentDomiciliario


def _obtener_estado_entrega_id(db: Session, codigo: str) -> int:
    estado_id = db.execute(
        text("select id_estado_entrega from estado_entrega where codigo = :codigo limit 1"),
        {"codigo": codigo},
    ).scalar_one_or_none()

    if estado_id is None:
        raise ValueError(f"No existe el estado de entrega {codigo}")
    return int(estado_id)


def _transicion_entrega_permitida(
    db: Session,
    *,
    empresa_id: int,
    estado_origen_id: int,
    estado_destino_id: int,
) -> bool:
    existe = db.execute(
        text(
            """
            select 1
            from transicion_estado_entrega
            where empresa_id = :empresa_id
                and estado_origen_id = :estado_origen_id
                and estado_destino_id = :estado_destino_id
            limit 1
            """
        ),
        {
            "empresa_id": empresa_id,
            "estado_origen_id": estado_origen_id,
            "estado_destino_id": estado_destino_id,
        },
    ).scalar_one_or_none()
    return existe is not None


def _buscar_pedido_domiciliario_para_estado(
    db: Session,
    *,
    numero_pedido: int,
    domiciliario: CurrentDomiciliario,
    estado_origen: str,
    sucursal_id: int | None = None,
) -> list[dict]:
    sucursal_filtro = sucursal_id or domiciliario.sucursal_id
    return [
        dict(row)
        for row in db.execute(
            text(
                r"""
                select
                    p.id_pedido,
                    p.numero_pedido,
                    p.sucursal_id,
                    e.id_entrega,
                    e.estadoentregaid,
                    ee.codigo as estado_actual
                from pedido p
                join entrega e
                    on e.pedido_id = p.id_pedido
                    and e.empresa_id = p.empresa_id
                join estado_entrega ee
                    on ee.id_estado_entrega = e.estadoentregaid
                where p.empresa_id = :empresa_id
                    and p.numero_pedido = :numero_pedido
                    and e.domiciliarioid = :domiciliario_id
                    and ee.codigo = :estado_origen
                    and (cast(:sucursal_id as bigint) is null or p.sucursal_id = cast(:sucursal_id as bigint))
                for update of e
                """
            ),
            {
                "empresa_id": domiciliario.empresa_id,
                "numero_pedido": numero_pedido,
                "domiciliario_id": domiciliario.id_empleado,
                "estado_origen": estado_origen,
                "sucursal_id": sucursal_filtro,
            },
        )
        .mappings()
        .all()
    ]


def _auditar_cambio_entrega(
    db: Session,
    *,
    pedido: dict,
    domiciliario: CurrentDomiciliario,
    accion: str,
    estado_nuevo: str,
    detalle: dict,
) -> None:
    db.execute(
        text(
            """
            insert into domicilio_auditoria (
                empresa_id,
                sucursal_id,
                pedido_id,
                entrega_id,
                actor_login,
                domiciliario_id,
                accion,
                estado_anterior,
                estado_nuevo,
                detalle_json,
                created_at
            )
            values (
                :empresa_id,
                :sucursal_id,
                :pedido_id,
                :entrega_id,
                :actor_login,
                :domiciliario_id,
                :accion,
                :estado_anterior,
                :estado_nuevo,
                :detalle_json,
                timezone('America/Bogota', now())
            )
            """
        ),
        {
            "empresa_id": domiciliario.empresa_id,
            "sucursal_id": pedido["sucursal_id"],
            "pedido_id": pedido["id_pedido"],
            "entrega_id": pedido["id_entrega"],
            "actor_login": domiciliario.usuario,
            "domiciliario_id": domiciliario.id_empleado,
            "accion": accion,
            "estado_anterior": pedido["estado_actual"],
            "estado_nuevo": estado_nuevo,
            "detalle_json": json.dumps(detalle),
        },
    )


def listar_pedidos_disponibles(
    db: Session,
    *,
    empresa_id: int,
    sucursal_id: int | None = None,
    fecha: date,
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    query = text(
        r"""
        select
            p.numero_pedido,
            e.destinatario,
            e.telefonodestino as telefono_destinatario,
            string_agg(pr.nombre_producto, ', ' order by pd.id_pedido_detalle) as arreglo,
            (array_remove(array_agg(ps.imagen_url order by pd.id_pedido_detalle), null))[1] as imagen_arreglo,
            coalesce(
                array_remove(array_agg(ps.imagen_url order by pd.id_pedido_detalle), null),
                array[]::varchar[]
            ) as imagenes_arreglo,
            e.direccion,
            coalesce(e.barrionombre, b.nombre_barrio) as barrio,
            b.zona_id::text as zona,
            coalesce(
                e.rangohora,
                to_char(coalesce(e.fechaentregaprogramada, e.fechaentrega), 'HH24:MI')
            ) as hora_entrega,
            coalesce(e.fechaentregaprogramada, e.fechaentrega)::date as fecha_entrega,
            e.fechaasignacion as asignado_en,
            e.fechasalida as en_ruta_en,
            e.fechaentrega as entregado_en,
            to_char(e.fechaasignacion, 'HH24:MI') as hora_asignado,
            to_char(e.fechasalida, 'HH24:MI') as hora_en_ruta,
            to_char(e.fechaentrega, 'HH24:MI') as hora_entregado
        from entrega e
        join pedido p
            on p.id_pedido = e.pedido_id
            and p.empresa_id = e.empresa_id
        left join barrio b
            on b.id_barrio = e.barrioid
            and b.empresa_id = e.empresa_id
        left join pedido_detalle pd
            on pd.pedido_id = p.id_pedido
            and pd.empresa_id = p.empresa_id
        left join producto pr
            on pr.id_producto = pd.producto_id
            and pr.empresa_id = pd.empresa_id
        left join producto_sucursal ps
            on ps.producto_id = pd.producto_id
            and ps.sucursal_id = pd.sucursal_id
        join estado_entrega ee
            on ee.id_estado_entrega = e.estadoentregaid
        where e.empresa_id = :empresa_id
            and (cast(:sucursal_id as bigint) is null or p.sucursal_id = cast(:sucursal_id as bigint))
            and e.domiciliarioid is null
            and ee.codigo = 'pendiente'
            and coalesce(e.fechaentregaprogramada, e.fechaentrega)::date = :fecha
            and lower(regexp_replace(trim(coalesce(e.direccion, '')), '\s+', ' ', 'g')) <> 'recoger en tienda'
            and lower(regexp_replace(trim(coalesce(e.barrionombre, '')), '\s+', ' ', 'g')) <> 'recoger en tienda'
        group by
            p.id_pedido,
            p.numero_pedido,
            e.id_entrega,
            e.destinatario,
            e.telefonodestino,
            e.direccion,
            e.barrionombre,
            b.nombre_barrio,
            b.zona_id,
            e.rangohora,
            e.fechaentregaprogramada,
            e.fechaentrega,
            e.fechaasignacion,
            e.fechasalida
        order by
            coalesce(e.fechaentregaprogramada, e.fechaentrega) nulls last,
            p.numero_pedido
        limit :limit
        offset :offset;
        """
    )
    result = db.execute(
        query,
        {
            "empresa_id": empresa_id,
            "sucursal_id": sucursal_id,
            "fecha": fecha,
            "limit": limit,
            "offset": offset,
        },
    )
    return [dict(row) for row in result.mappings().all()]


def listar_pedidos_asignados(
    db: Session,
    *,
    domiciliario: CurrentDomiciliario,
    fecha: date,
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    query = text(
        r"""
        select
            p.numero_pedido,
            e.destinatario,
            e.telefonodestino as telefono_destinatario,
            string_agg(pr.nombre_producto, ', ' order by pd.id_pedido_detalle) as arreglo,
            (array_remove(array_agg(ps.imagen_url order by pd.id_pedido_detalle), null))[1] as imagen_arreglo,
            coalesce(
                array_remove(array_agg(ps.imagen_url order by pd.id_pedido_detalle), null),
                array[]::varchar[]
            ) as imagenes_arreglo,
            e.direccion,
            coalesce(e.barrionombre, b.nombre_barrio) as barrio,
            b.zona_id::text as zona,
            coalesce(
                e.rangohora,
                to_char(coalesce(e.fechaentregaprogramada, e.fechaentrega), 'HH24:MI')
            ) as hora_entrega,
            coalesce(e.fechaentregaprogramada, e.fechaentrega)::date as fecha_entrega,
            ee.codigo as estado_entrega,
            coalesce(e.fechaasignacion, da.asignado_en) as asignado_en,
            e.fechasalida as en_ruta_en,
            case
                when ee.codigo = 'entregado'
                    then coalesce(
                        e.fechaentrega::date + nullif(e.fechaentrega::time, time '00:00'),
                        de.entregado_en
                    )
            end as entregado_en,
            to_char(coalesce(e.fechaasignacion, da.asignado_en), 'HH24:MI') as hora_asignado,
            to_char(e.fechasalida, 'HH24:MI') as hora_en_ruta,
            case
                when ee.codigo = 'entregado'
                    then to_char(
                        coalesce(
                            e.fechaentrega::date + nullif(e.fechaentrega::time, time '00:00'),
                            de.entregado_en
                        ),
                        'HH24:MI'
                    )
            end as hora_entregado
        from entrega e
        join pedido p
            on p.id_pedido = e.pedido_id
            and p.empresa_id = e.empresa_id
        join estado_entrega ee
            on ee.id_estado_entrega = e.estadoentregaid
        left join barrio b
            on b.id_barrio = e.barrioid
            and b.empresa_id = e.empresa_id
        left join pedido_detalle pd
            on pd.pedido_id = p.id_pedido
            and pd.empresa_id = p.empresa_id
        left join producto pr
            on pr.id_producto = pd.producto_id
            and pr.empresa_id = pd.empresa_id
        left join producto_sucursal ps
            on ps.producto_id = pd.producto_id
            and ps.sucursal_id = pd.sucursal_id
        left join lateral (
            select min(created_at) as asignado_en
            from domicilio_auditoria
            where empresa_id = e.empresa_id
                and entrega_id = e.id_entrega
                and estado_nuevo = 'asignado'
        ) da on true
        left join lateral (
            select min(created_at) as entregado_en
            from domicilio_auditoria
            where empresa_id = e.empresa_id
                and entrega_id = e.id_entrega
                and estado_nuevo = 'entregado'
        ) de on true
        where e.empresa_id = :empresa_id
            and e.domiciliarioid = :domiciliario_id
            and (cast(:sucursal_id as bigint) is null or p.sucursal_id = cast(:sucursal_id as bigint))
            and ee.codigo in ('asignado', 'en_ruta', 'entregado', 'no_entregado')
            and coalesce(e.fechaentregaprogramada, e.fechaentrega)::date = :fecha
            and lower(regexp_replace(trim(coalesce(e.direccion, '')), '\s+', ' ', 'g')) <> 'recoger en tienda'
            and lower(regexp_replace(trim(coalesce(e.barrionombre, '')), '\s+', ' ', 'g')) <> 'recoger en tienda'
        group by
            p.id_pedido,
            p.numero_pedido,
            e.id_entrega,
            e.destinatario,
            e.telefonodestino,
            e.direccion,
            e.barrionombre,
            b.nombre_barrio,
            b.zona_id,
            e.rangohora,
            e.fechaentregaprogramada,
            e.fechaentrega,
            e.fechaasignacion,
            e.fechasalida,
            da.asignado_en,
            de.entregado_en,
            ee.codigo
        order by
            coalesce(e.fechaentregaprogramada, e.fechaentrega) nulls last,
            p.numero_pedido
        limit :limit
        offset :offset;
        """
    )
    result = db.execute(
        query,
        {
            "empresa_id": domiciliario.empresa_id,
            "domiciliario_id": domiciliario.id_empleado,
            "sucursal_id": domiciliario.sucursal_id,
            "fecha": fecha,
            "limit": limit,
            "offset": offset,
        },
    )
    return [dict(row) for row in result.mappings().all()]


def asignar_pedido_a_domiciliario(
    db: Session,
    *,
    numero_pedido: int,
    domiciliario: CurrentDomiciliario,
    sucursal_id: int | None = None,
) -> dict:
    sucursal_filtro = sucursal_id or domiciliario.sucursal_id
    asignado = db.execute(
        text("select id_estado_entrega from estado_entrega where codigo = 'asignado' limit 1")
    ).scalar_one_or_none()

    if asignado is None:
        raise ValueError("No existe el estado de entrega asignado")

    candidatos = db.execute(
        text(
            r"""
            select
                p.id_pedido,
                p.numero_pedido,
                p.sucursal_id,
                e.id_entrega,
                e.estadoentregaid,
                ee.codigo as estado_actual
            from pedido p
            join entrega e
                on e.pedido_id = p.id_pedido
                and e.empresa_id = p.empresa_id
            join estado_entrega ee
                on ee.id_estado_entrega = e.estadoentregaid
            where p.empresa_id = :empresa_id
                and p.numero_pedido = :numero_pedido
                and (cast(:sucursal_id as bigint) is null or p.sucursal_id = cast(:sucursal_id as bigint))
                and e.domiciliarioid is null
                and ee.codigo = 'pendiente'
                and lower(regexp_replace(trim(coalesce(e.direccion, '')), '\s+', ' ', 'g')) <> 'recoger en tienda'
                and lower(regexp_replace(trim(coalesce(e.barrionombre, '')), '\s+', ' ', 'g')) <> 'recoger en tienda'
            for update of e
            """
        ),
        {
            "empresa_id": domiciliario.empresa_id,
            "numero_pedido": numero_pedido,
            "sucursal_id": sucursal_filtro,
        },
    ).mappings().all()

    if not candidatos:
        return {
            "status": "not_found",
            "message": "El pedido no esta disponible para asignacion",
        }

    if len(candidatos) > 1:
        return {
            "status": "ambiguous",
            "message": "Debe especificar sucursal_id para asignar este pedido",
        }

    pedido = candidatos[0]
    db.execute(
        text(
            """
            update entrega
            set
                domiciliarioid = :domiciliario_id,
                estadoentregaid = :estado_asignado_id,
                fechaasignacion = timezone('America/Bogota', now()),
                updatedat = timezone('America/Bogota', now())
            where id_entrega = :id_entrega
                and domiciliarioid is null
            """
        ),
        {
            "domiciliario_id": domiciliario.id_empleado,
            "estado_asignado_id": asignado,
            "id_entrega": pedido["id_entrega"],
        },
    )
    asignacion = db.execute(
        text(
            """
            select
                fechaasignacion,
                to_char(fechaasignacion, 'HH24:MI') as hora_asignado
            from entrega
            where id_entrega = :id_entrega
            """
        ),
        {"id_entrega": pedido["id_entrega"]},
    ).mappings().one()
    db.execute(
        text(
            """
            insert into domicilio_auditoria (
                empresa_id,
                sucursal_id,
                pedido_id,
                entrega_id,
                actor_login,
                domiciliario_id,
                accion,
                estado_anterior,
                estado_nuevo,
                detalle_json,
                created_at
            )
            values (
                :empresa_id,
                :sucursal_id,
                :pedido_id,
                :entrega_id,
                :actor_login,
                :domiciliario_id,
                'ASIGNAR_DOMICILIARIO',
                :estado_anterior,
                'asignado',
                :detalle_json,
                timezone('America/Bogota', now())
            )
            """
        ),
        {
            "empresa_id": domiciliario.empresa_id,
            "sucursal_id": pedido["sucursal_id"],
            "pedido_id": pedido["id_pedido"],
            "entrega_id": pedido["id_entrega"],
            "actor_login": domiciliario.usuario,
            "domiciliario_id": domiciliario.id_empleado,
            "estado_anterior": pedido["estado_actual"],
            "detalle_json": f'{{"numero_pedido": {numero_pedido}}}',
        },
    )
    db.commit()

    return {
        "status": "ok",
        "numero_pedido": pedido["numero_pedido"],
        "id_pedido": pedido["id_pedido"],
        "id_entrega": pedido["id_entrega"],
        "estado": "asignado",
        "domiciliario_id": domiciliario.id_empleado,
        "asignado_en": asignacion["fechaasignacion"],
        "hora_asignado": asignacion["hora_asignado"],
        "mensaje": "Pedido asignado correctamente",
    }


def devolver_pedido_asignado(
    db: Session,
    *,
    numero_pedido: int,
    domiciliario: CurrentDomiciliario,
    sucursal_id: int | None = None,
) -> dict:
    sucursal_filtro = sucursal_id or domiciliario.sucursal_id
    pendiente = db.execute(
        text("select id_estado_entrega from estado_entrega where codigo = 'pendiente' limit 1")
    ).scalar_one_or_none()

    if pendiente is None:
        raise ValueError("No existe el estado de entrega pendiente")

    candidatos = db.execute(
        text(
            r"""
            select
                p.id_pedido,
                p.numero_pedido,
                p.sucursal_id,
                e.id_entrega,
                ee.codigo as estado_actual
            from pedido p
            join entrega e
                on e.pedido_id = p.id_pedido
                and e.empresa_id = p.empresa_id
            join estado_entrega ee
                on ee.id_estado_entrega = e.estadoentregaid
            where p.empresa_id = :empresa_id
                and p.numero_pedido = :numero_pedido
                and e.domiciliarioid = :domiciliario_id
                and ee.codigo = 'asignado'
                and (cast(:sucursal_id as bigint) is null or p.sucursal_id = cast(:sucursal_id as bigint))
            for update of e
            """
        ),
        {
            "empresa_id": domiciliario.empresa_id,
            "numero_pedido": numero_pedido,
            "domiciliario_id": domiciliario.id_empleado,
            "sucursal_id": sucursal_filtro,
        },
    ).mappings().all()

    if not candidatos:
        return {
            "status": "not_found",
            "message": "El pedido no esta asignado a este domiciliario",
        }

    if len(candidatos) > 1:
        return {
            "status": "ambiguous",
            "message": "Debe especificar sucursal_id para devolver este pedido",
        }

    pedido = candidatos[0]
    db.execute(
        text(
            """
            update entrega
            set
                domiciliarioid = null,
                estadoentregaid = :estado_pendiente_id,
                fechaasignacion = null,
                updatedat = timezone('America/Bogota', now())
            where id_entrega = :id_entrega
                and domiciliarioid = :domiciliario_id
            """
        ),
        {
            "estado_pendiente_id": pendiente,
            "id_entrega": pedido["id_entrega"],
            "domiciliario_id": domiciliario.id_empleado,
        },
    )
    db.execute(
        text(
            """
            insert into domicilio_auditoria (
                empresa_id,
                sucursal_id,
                pedido_id,
                entrega_id,
                actor_login,
                domiciliario_id,
                accion,
                estado_anterior,
                estado_nuevo,
                detalle_json,
                created_at
            )
            values (
                :empresa_id,
                :sucursal_id,
                :pedido_id,
                :entrega_id,
                :actor_login,
                :domiciliario_id,
                'DEVOLVER_DOMICILIO',
                :estado_anterior,
                'pendiente',
                :detalle_json,
                timezone('America/Bogota', now())
            )
            """
        ),
        {
            "empresa_id": domiciliario.empresa_id,
            "sucursal_id": pedido["sucursal_id"],
            "pedido_id": pedido["id_pedido"],
            "entrega_id": pedido["id_entrega"],
            "actor_login": domiciliario.usuario,
            "domiciliario_id": domiciliario.id_empleado,
            "estado_anterior": pedido["estado_actual"],
            "detalle_json": f'{{"numero_pedido": {numero_pedido}}}',
        },
    )
    db.commit()

    return {
        "status": "ok",
        "numero_pedido": pedido["numero_pedido"],
        "id_pedido": pedido["id_pedido"],
        "id_entrega": pedido["id_entrega"],
        "estado": "pendiente",
        "domiciliario_id": None,
        "mensaje": "Pedido devuelto correctamente",
    }


def _cambiar_estado_pedido_domiciliario(
    db: Session,
    *,
    numero_pedido: int,
    domiciliario: CurrentDomiciliario,
    estado_origen: str,
    estado_destino: str,
    accion: str,
    mensaje: str,
    sucursal_id: int | None = None,
    update_sql: str = "updatedat = timezone('America/Bogota', now())",
    update_params: dict | None = None,
    detalle: dict | None = None,
) -> dict:
    estado_destino_id = _obtener_estado_entrega_id(db, estado_destino)

    candidatos = _buscar_pedido_domiciliario_para_estado(
        db,
        numero_pedido=numero_pedido,
        domiciliario=domiciliario,
        estado_origen=estado_origen,
        sucursal_id=sucursal_id,
    )

    if not candidatos:
        return {
            "status": "not_found",
            "message": f"El pedido no esta en estado {estado_origen} para este domiciliario",
        }

    if len(candidatos) > 1:
        return {
            "status": "ambiguous",
            "message": f"Debe especificar sucursal_id para cambiar este pedido a {estado_destino}",
        }

    pedido = candidatos[0]
    if not _transicion_entrega_permitida(
        db,
        empresa_id=domiciliario.empresa_id,
        estado_origen_id=pedido["estadoentregaid"],
        estado_destino_id=estado_destino_id,
    ):
        return {
            "status": "invalid_transition",
            "message": f"No esta permitida la transicion {estado_origen} -> {estado_destino}",
        }

    params = {
        "estado_destino_id": estado_destino_id,
        "id_entrega": pedido["id_entrega"],
        "domiciliario_id": domiciliario.id_empleado,
    }
    params.update(update_params or {})
    db.execute(
        text(
            f"""
            update entrega
            set
                estadoentregaid = :estado_destino_id,
                {update_sql}
            where id_entrega = :id_entrega
                and domiciliarioid = :domiciliario_id
            """
        ),
        params,
    )

    timestamps = db.execute(
        text(
            """
            select
                coalesce(e.fechaasignacion, da.asignado_en) as fechaasignacion,
                e.fechasalida,
                case when ee.codigo = 'entregado' then e.fechaentrega end as fechaentrega,
                to_char(coalesce(e.fechaasignacion, da.asignado_en), 'HH24:MI') as hora_asignado,
                to_char(e.fechasalida, 'HH24:MI') as hora_en_ruta,
                case when ee.codigo = 'entregado' then to_char(e.fechaentrega, 'HH24:MI') end as hora_entregado
            from entrega e
            join estado_entrega ee
                on ee.id_estado_entrega = e.estadoentregaid
            left join lateral (
                select min(created_at) as asignado_en
                from domicilio_auditoria
                where empresa_id = e.empresa_id
                    and entrega_id = e.id_entrega
                    and estado_nuevo = 'asignado'
            ) da on true
            where e.id_entrega = :id_entrega
            """
        ),
        {"id_entrega": pedido["id_entrega"]},
    ).mappings().one()
    _auditar_cambio_entrega(
        db,
        pedido=pedido,
        domiciliario=domiciliario,
        accion=accion,
        estado_nuevo=estado_destino,
        detalle={"numero_pedido": numero_pedido, **(detalle or {})},
    )
    db.commit()

    return {
        "status": "ok",
        "numero_pedido": pedido["numero_pedido"],
        "id_pedido": pedido["id_pedido"],
        "id_entrega": pedido["id_entrega"],
        "estado": estado_destino,
        "domiciliario_id": domiciliario.id_empleado,
        "asignado_en": timestamps["fechaasignacion"],
        "en_ruta_en": timestamps["fechasalida"],
        "entregado_en": timestamps["fechaentrega"],
        "hora_asignado": timestamps["hora_asignado"],
        "hora_en_ruta": timestamps["hora_en_ruta"],
        "hora_entregado": timestamps["hora_entregado"],
        "fecha_inicio_entrega": timestamps["fechasalida"],
        "fecha_entrega": timestamps["fechaentrega"],
        "mensaje": mensaje,
    }


def iniciar_entrega_pedido(
    db: Session,
    *,
    numero_pedido: int,
    domiciliario: CurrentDomiciliario,
    sucursal_id: int | None = None,
) -> dict:
    return _cambiar_estado_pedido_domiciliario(
        db,
        numero_pedido=numero_pedido,
        domiciliario=domiciliario,
        estado_origen="asignado",
        estado_destino="en_ruta",
        accion="INICIAR_ENTREGA",
        mensaje="Entrega iniciada correctamente",
        sucursal_id=sucursal_id,
        update_sql=(
            "fechaasignacion = coalesce(fechaasignacion, timezone('America/Bogota', now())), "
            "fechasalida = coalesce(fechasalida, timezone('America/Bogota', now())), "
            "updatedat = timezone('America/Bogota', now())"
        ),
    )


def entregar_pedido(
    db: Session,
    *,
    numero_pedido: int,
    domiciliario: CurrentDomiciliario,
    firma_nombre: str | None = None,
    firma_documento: str | None = None,
    firma_imagen_url: str | None = None,
    evidencia_foto_url: str | None = None,
    observaciones: str | None = None,
    sucursal_id: int | None = None,
) -> dict:
    return _cambiar_estado_pedido_domiciliario(
        db,
        numero_pedido=numero_pedido,
        domiciliario=domiciliario,
        estado_origen="en_ruta",
        estado_destino="entregado",
        accion="CONFIRMAR_ENTREGA",
        mensaje="Entrega confirmada correctamente",
        sucursal_id=sucursal_id,
        update_sql=(
            "fechaentrega = timezone('America/Bogota', now()), "
            "firmanombre = :firma_nombre, "
            "firmadocumento = :firma_documento, "
            "firmaimagenurl = :firma_imagen_url, "
            "evidenciafotourl = :evidencia_foto_url, "
            "observaciones = :observaciones, "
            "updatedat = timezone('America/Bogota', now())"
        ),
        update_params={
            "firma_nombre": firma_nombre,
            "firma_documento": firma_documento,
            "firma_imagen_url": firma_imagen_url,
            "evidencia_foto_url": evidencia_foto_url,
            "observaciones": observaciones,
        },
        detalle={
            "firma_nombre": firma_nombre,
            "firma_documento": firma_documento,
            "evidencia_foto_url": evidencia_foto_url,
        },
    )


def marcar_pedido_no_entregado(
    db: Session,
    *,
    numero_pedido: int,
    domiciliario: CurrentDomiciliario,
    motivo: str,
    evidencia_foto_url: str | None = None,
    observaciones: str | None = None,
    sucursal_id: int | None = None,
    detalle_extra: dict | None = None,
) -> dict:
    return _cambiar_estado_pedido_domiciliario(
        db,
        numero_pedido=numero_pedido,
        domiciliario=domiciliario,
        estado_origen="en_ruta",
        estado_destino="no_entregado",
        accion="MARCAR_NO_ENTREGADO",
        mensaje="Entrega marcada como no entregada",
        sucursal_id=sucursal_id,
        update_sql=(
            "motivonoentregado = :motivo, "
            "evidenciafotourl = :evidencia_foto_url, "
            "observaciones = :observaciones, "
            "updatedat = timezone('America/Bogota', now())"
        ),
        update_params={
            "motivo": motivo,
            "evidencia_foto_url": evidencia_foto_url,
            "observaciones": observaciones,
        },
        detalle={
            "motivo": motivo,
            "evidencia_foto_url": evidencia_foto_url,
            **(detalle_extra or {}),
        },
    )
