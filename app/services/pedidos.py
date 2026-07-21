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
) -> int:
    return int(
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
            returning id_audit
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
        ).scalar_one()
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
        join estado_pedido ep
            on ep.id_estado_pedido = p.estado_pedido_id
        where e.empresa_id = :empresa_id
            and (cast(:sucursal_id as bigint) is null or p.sucursal_id = cast(:sucursal_id as bigint))
            and e.domiciliarioid is null
            and ee.codigo = 'pendiente'
            and lower(regexp_replace(trim(ep.nombre_estado), '\s+', ' ', 'g')) = 'aprobado'
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
            and ee.codigo in ('asignado', 'en_ruta')
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


def listar_historial_pedidos(
    db: Session,
    *,
    domiciliario: CurrentDomiciliario,
    fecha_desde: date | None = None,
    fecha_hasta: date | None = None,
    q: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    query = text(
        r"""
        with historial as (
            select
                p.numero_pedido,
                e.destinatario as cliente,
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
                coalesce(e.fechaasignacion, da.asignado_en) as fecha_asignacion,
                coalesce(e.fechaasignacion, da.asignado_en) as asignado_en,
                case
                    when lua.accion = 'DEVOLVER_DOMICILIO'
                        then lua.created_at
                    when ee.codigo = 'entregado'
                        then coalesce(e.fechaentrega, de.entregado_en, lua.created_at)
                    when ee.codigo in ('no_entregado', 'cancelado', 'cancelada')
                        then coalesce(lua.created_at, e.updatedat)
                end as fecha_entrega,
                case
                    when lua.accion = 'DEVOLVER_DOMICILIO'
                        then lua.created_at
                    when ee.codigo = 'entregado'
                        then coalesce(e.fechaentrega, de.entregado_en, lua.created_at)
                    when ee.codigo in ('no_entregado', 'cancelado', 'cancelada')
                        then coalesce(lua.created_at, e.updatedat)
                end as entregado_en,
                to_char(coalesce(e.fechaasignacion, da.asignado_en), 'HH24:MI') as hora_asignado,
                to_char(
                    case
                        when lua.accion = 'DEVOLVER_DOMICILIO'
                            then lua.created_at
                        when ee.codigo = 'entregado'
                            then coalesce(e.fechaentrega, de.entregado_en, lua.created_at)
                        when ee.codigo in ('no_entregado', 'cancelado', 'cancelada')
                            then coalesce(lua.created_at, e.updatedat)
                    end,
                    'HH24:MI'
                ) as hora_entregado,
                case
                    when lua.accion = 'DEVOLVER_DOMICILIO' then 'reasignado'
                    when ee.codigo = 'no_entregado' then 'con_novedad'
                    when ee.codigo in ('cancelado', 'cancelada') then 'cancelado'
                    else ee.codigo
                end as estado_final,
                ee.codigo as estado_entrega,
                e.motivonoentregado as novedad,
                coalesce(nov.novedades, '[]'::jsonb) as novedades,
                e.evidenciafotourl as evidencia_entrega_url,
                e.firmaimagenurl as evidencia_firma_url,
                e.firmanombre as firma_nombre,
                e.firmadocumento as firma_documento,
                coalesce(e.observaciones, e.observaciongeneral) as observaciones,
                coalesce(
                    case
                        when lua.accion = 'DEVOLVER_DOMICILIO'
                            then lua.created_at
                        when ee.codigo = 'entregado'
                            then coalesce(e.fechaentrega, de.entregado_en, lua.created_at)
                        when ee.codigo in ('no_entregado', 'cancelado', 'cancelada')
                            then coalesce(lua.created_at, e.updatedat)
                    end,
                    e.updatedat,
                    e.fechaentrega,
                    e.fechaasignacion,
                    e.createdat
                ) as fecha_historial
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
                    and domiciliario_id = :domiciliario_id
                    and estado_nuevo = 'asignado'
            ) da on true
            left join lateral (
                select min(created_at) as entregado_en
                from domicilio_auditoria
                where empresa_id = e.empresa_id
                    and entrega_id = e.id_entrega
                    and domiciliario_id = :domiciliario_id
                    and estado_nuevo = 'entregado'
            ) de on true
            left join lateral (
                select accion, estado_nuevo, created_at
                from domicilio_auditoria
                where empresa_id = e.empresa_id
                    and entrega_id = e.id_entrega
                    and domiciliario_id = :domiciliario_id
                order by created_at desc, id_audit desc
                limit 1
            ) lua on true
            left join lateral (
                select jsonb_agg(
                    jsonb_build_object(
                        'accion', accion,
                        'estado_anterior', estado_anterior,
                        'estado_nuevo', estado_nuevo,
                        'detalle', detalle_json,
                        'registrada_en', created_at
                    )
                    order by created_at
                ) as novedades
                from domicilio_auditoria
                where empresa_id = e.empresa_id
                    and entrega_id = e.id_entrega
                    and domiciliario_id = :domiciliario_id
                    and (
                        accion in ('MARCAR_NO_ENTREGADO', 'DEVOLVER_DOMICILIO')
                        or estado_nuevo in ('no_entregado', 'pendiente')
                    )
            ) nov on true
            where e.empresa_id = :empresa_id
                and (cast(:sucursal_id as bigint) is null or p.sucursal_id = cast(:sucursal_id as bigint))
                and (
                    e.domiciliarioid = :domiciliario_id
                    or da.asignado_en is not null
                )
                and (
                    ee.codigo in ('entregado', 'no_entregado', 'cancelado', 'cancelada')
                    or lua.accion = 'DEVOLVER_DOMICILIO'
                )
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
                e.fechaasignacion,
                e.fechaentrega,
                e.updatedat,
                e.createdat,
                e.motivonoentregado,
                e.evidenciafotourl,
                e.firmaimagenurl,
                e.firmanombre,
                e.firmadocumento,
                e.observaciones,
                e.observaciongeneral,
                da.asignado_en,
                de.entregado_en,
                lua.accion,
                lua.created_at,
                ee.codigo,
                nov.novedades
        )
        select *
        from historial
        where (cast(:fecha_desde as date) is null or fecha_historial::date >= cast(:fecha_desde as date))
            and (cast(:fecha_hasta as date) is null or fecha_historial::date <= cast(:fecha_hasta as date))
            and (
                cast(:q as text) is null
                or numero_pedido::text ilike '%' || cast(:q as text) || '%'
                or cliente ilike '%' || cast(:q as text) || '%'
                or coalesce(arreglo, '') ilike '%' || cast(:q as text) || '%'
            )
        order by fecha_historial desc nulls last, numero_pedido desc
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
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta,
            "q": q.strip() if q and q.strip() else None,
            "limit": limit,
            "offset": offset,
        },
    )
    return [dict(row) for row in result.mappings().all()]


def listar_novedades_pedidos(
    db: Session,
    *,
    domiciliario: CurrentDomiciliario,
    estado: str = "abierta",
    fecha_desde: date | None = None,
    fecha_hasta: date | None = None,
    q: str | None = None,
    numero_pedido: int | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    query = text(
        r"""
        with novedades as (
            select
                dn.id_novedad,
                p.numero_pedido,
                e.destinatario as cliente,
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
                dn.tipo_novedad,
                coalesce(dn.descripcion, e.observaciones) as descripcion,
                coalesce(dn.motivo, e.motivonoentregado) as motivo,
                da.detalle_json,
                coalesce(dn.evidencia_foto_url, e.evidenciafotourl) as evidencia_foto_url,
                dn.estado as estado_novedad,
                ee.codigo as estado_pedido,
                dn.reportada_en,
                dn.resuelta_en,
                dn.estado = 'abierta' and ee.codigo = 'no_entregado' as puede_reintentar,
                nullif(e.telefonodestino, '') is not null as puede_contactar_cliente
            from domicilio_novedad dn
            join entrega e
                on e.id_entrega = dn.entrega_id
                and e.empresa_id = dn.empresa_id
            join pedido p
                on p.id_pedido = dn.pedido_id
                and p.empresa_id = dn.empresa_id
            join estado_entrega ee
                on ee.id_estado_entrega = e.estadoentregaid
            left join domicilio_auditoria da
                on da.id_audit = dn.auditoria_reporte_id
                and da.empresa_id = dn.empresa_id
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
            where dn.empresa_id = :empresa_id
                and dn.domiciliario_id = :domiciliario_id
                and (cast(:sucursal_id as bigint) is null or p.sucursal_id = cast(:sucursal_id as bigint))
                and (cast(:numero_pedido as bigint) is null or p.numero_pedido = cast(:numero_pedido as bigint))
                and lower(regexp_replace(trim(coalesce(e.direccion, '')), '\s+', ' ', 'g')) <> 'recoger en tienda'
                and lower(regexp_replace(trim(coalesce(e.barrionombre, '')), '\s+', ' ', 'g')) <> 'recoger en tienda'
            group by
                dn.id_novedad,
                p.id_pedido,
                p.numero_pedido,
                e.id_entrega,
                e.destinatario,
                e.telefonodestino,
                e.direccion,
                e.barrionombre,
                b.nombre_barrio,
                b.zona_id,
                da.detalle_json,
                dn.tipo_novedad,
                dn.descripcion,
                dn.motivo,
                dn.evidencia_foto_url,
                dn.estado,
                dn.reportada_en,
                dn.resuelta_en,
                e.observaciones,
                e.motivonoentregado,
                e.evidenciafotourl,
                ee.codigo
        )
        select *
        from novedades
        where (cast(:fecha_desde as date) is null or reportada_en::date >= cast(:fecha_desde as date))
            and (cast(:fecha_hasta as date) is null or reportada_en::date <= cast(:fecha_hasta as date))
            and (
                :estado = 'todas'
                or estado_novedad = :estado
            )
            and (
                cast(:q as text) is null
                or numero_pedido::text ilike '%' || cast(:q as text) || '%'
                or cliente ilike '%' || cast(:q as text) || '%'
                or coalesce(arreglo, '') ilike '%' || cast(:q as text) || '%'
            )
        order by reportada_en desc, numero_pedido desc
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
            "numero_pedido": numero_pedido,
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta,
            "estado": estado,
            "q": q.strip() if q and q.strip() else None,
            "limit": limit,
            "offset": offset,
        },
    )
    return [dict(row) for row in result.mappings().all()]


def registrar_novedad_operativa(
    db: Session,
    *,
    resultado_estado: dict,
    domiciliario: CurrentDomiciliario,
    tipo_novedad: str,
    motivo: str,
    descripcion: str | None = None,
    evidencia_foto_url: str | None = None,
) -> dict:
    auditoria_id = resultado_estado.get("auditoria_id")
    if auditoria_id is None:
        raise ValueError("No se puede registrar la novedad sin auditoria_id")

    novedad = db.execute(
        text(
            """
            insert into domicilio_novedad (
                id_novedad,
                empresa_id,
                sucursal_id,
                pedido_id,
                entrega_id,
                domiciliario_id,
                tipo_novedad,
                motivo,
                descripcion,
                evidencia_foto_url,
                estado,
                reportada_en,
                reportada_por_login,
                auditoria_reporte_id,
                created_at
            )
            values (
                :id_novedad,
                :empresa_id,
                :sucursal_id,
                :pedido_id,
                :entrega_id,
                :domiciliario_id,
                :tipo_novedad,
                :motivo,
                :descripcion,
                :evidencia_foto_url,
                'abierta',
                timezone('America/Bogota', now()),
                :reportada_por_login,
                :auditoria_reporte_id,
                timezone('America/Bogota', now())
            )
            on conflict (empresa_id, entrega_id) where estado = 'abierta'
            do update set
                tipo_novedad = excluded.tipo_novedad,
                motivo = excluded.motivo,
                descripcion = excluded.descripcion,
                evidencia_foto_url = coalesce(excluded.evidencia_foto_url, domicilio_novedad.evidencia_foto_url),
                auditoria_reporte_id = excluded.auditoria_reporte_id,
                updated_at = timezone('America/Bogota', now())
            returning id_novedad, estado
            """
        ),
        {
            "id_novedad": auditoria_id,
            "empresa_id": domiciliario.empresa_id,
            "sucursal_id": resultado_estado.get("sucursal_id") or domiciliario.sucursal_id,
            "pedido_id": resultado_estado["id_pedido"],
            "entrega_id": resultado_estado["id_entrega"],
            "domiciliario_id": domiciliario.id_empleado,
            "tipo_novedad": tipo_novedad,
            "motivo": motivo,
            "descripcion": descripcion,
            "evidencia_foto_url": evidencia_foto_url,
            "reportada_por_login": domiciliario.usuario,
            "auditoria_reporte_id": auditoria_id,
        },
    ).mappings().one()
    db.commit()
    return dict(novedad)


def resolver_novedad_pedido(
    db: Session,
    *,
    numero_pedido: int,
    id_novedad: int,
    domiciliario: CurrentDomiciliario,
    solucion: str,
    observaciones: str | None = None,
    nuevo_estado_pedido: str | None = None,
    evidencia_foto_url: str | None = None,
    firma_nombre: str | None = None,
    firma_documento: str | None = None,
    firma_imagen_url: str | None = None,
) -> dict:
    novedad = db.execute(
        text(
            r"""
            select
                dn.id_novedad,
                dn.empresa_id,
                dn.sucursal_id,
                dn.pedido_id,
                dn.entrega_id,
                dn.estado as estado_novedad,
                p.numero_pedido,
                e.domiciliarioid,
                e.estadoentregaid,
                ee.codigo as estado_actual
            from domicilio_novedad dn
            join pedido p
                on p.id_pedido = dn.pedido_id
                and p.empresa_id = dn.empresa_id
            join entrega e
                on e.id_entrega = dn.entrega_id
                and e.empresa_id = dn.empresa_id
            join estado_entrega ee
                on ee.id_estado_entrega = e.estadoentregaid
            where dn.empresa_id = :empresa_id
                and (
                    dn.id_novedad = :id_novedad
                    or dn.auditoria_reporte_id = :id_novedad
                )
                and p.numero_pedido = :numero_pedido
                and dn.domiciliario_id = :domiciliario_id
                and (cast(:sucursal_id as bigint) is null or dn.sucursal_id = cast(:sucursal_id as bigint))
            order by
                case when dn.id_novedad = :id_novedad then 0 else 1 end,
                dn.id_novedad desc
            limit 1
            for update of dn, e
            """
        ),
        {
            "empresa_id": domiciliario.empresa_id,
            "id_novedad": id_novedad,
            "numero_pedido": numero_pedido,
            "domiciliario_id": domiciliario.id_empleado,
            "sucursal_id": domiciliario.sucursal_id,
        },
    ).mappings().one_or_none()

    if novedad is None:
        return {
            "status": "not_found",
            "message": "La novedad no existe o no pertenece a este domiciliario",
        }

    if novedad["estado_novedad"] != "abierta":
        return {
            "status": "invalid_transition",
            "message": "La novedad ya fue resuelta o cancelada",
        }

    id_novedad_resuelta = novedad["id_novedad"]
    estado_final = nuevo_estado_pedido or novedad["estado_actual"]
    update_entrega_sql = "updatedat = timezone('America/Bogota', now())"
    update_entrega_params: dict = {
        "id_entrega": novedad["entrega_id"],
        "domiciliario_id": domiciliario.id_empleado,
    }

    if nuevo_estado_pedido:
        estado_destino_id = _obtener_estado_entrega_id(db, nuevo_estado_pedido)
        update_entrega_params["estado_destino_id"] = estado_destino_id

        if nuevo_estado_pedido == "entregado":
            update_entrega_sql = (
                "estadoentregaid = :estado_destino_id, "
                "domiciliarioid = :domiciliario_id, "
                "fechaentrega = timezone('America/Bogota', now()), "
                "evidenciafotourl = coalesce(:evidencia_foto_url, evidenciafotourl), "
                "firmanombre = coalesce(:firma_nombre, firmanombre), "
                "firmadocumento = coalesce(:firma_documento, firmadocumento), "
                "firmaimagenurl = coalesce(:firma_imagen_url, firmaimagenurl), "
                "observaciones = coalesce(:observaciones, observaciones), "
                "updatedat = timezone('America/Bogota', now())"
            )
            update_entrega_params.update(
                {
                    "evidencia_foto_url": evidencia_foto_url,
                    "firma_nombre": firma_nombre,
                    "firma_documento": firma_documento,
                    "firma_imagen_url": firma_imagen_url,
                    "observaciones": observaciones,
                }
            )
        elif nuevo_estado_pedido == "pendiente":
            update_entrega_sql = (
                "estadoentregaid = :estado_destino_id, "
                "domiciliarioid = null, "
                "fechaasignacion = null, "
                "fechasalida = null, "
                "updatedat = timezone('America/Bogota', now())"
            )
        elif nuevo_estado_pedido == "asignado":
            update_entrega_sql = (
                "estadoentregaid = :estado_destino_id, "
                "domiciliarioid = :domiciliario_id, "
                "fechaasignacion = coalesce(fechaasignacion, timezone('America/Bogota', now())), "
                "fechasalida = null, "
                "updatedat = timezone('America/Bogota', now())"
            )
        elif nuevo_estado_pedido == "en_ruta":
            update_entrega_sql = (
                "estadoentregaid = :estado_destino_id, "
                "domiciliarioid = :domiciliario_id, "
                "fechaasignacion = coalesce(fechaasignacion, timezone('America/Bogota', now())), "
                "fechasalida = coalesce(fechasalida, timezone('America/Bogota', now())), "
                "updatedat = timezone('America/Bogota', now())"
            )

    db.execute(
        text(
            f"""
            update entrega
            set {update_entrega_sql}
            where id_entrega = :id_entrega
            """
        ),
        update_entrega_params,
    )

    auditoria_id = db.execute(
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
                'RESOLVER_NOVEDAD',
                :estado_anterior,
                :estado_nuevo,
                :detalle_json,
                timezone('America/Bogota', now())
            )
            returning id_audit
            """
        ),
        {
            "empresa_id": domiciliario.empresa_id,
            "sucursal_id": novedad["sucursal_id"],
            "pedido_id": novedad["pedido_id"],
            "entrega_id": novedad["entrega_id"],
            "actor_login": domiciliario.usuario,
            "domiciliario_id": domiciliario.id_empleado,
            "estado_anterior": novedad["estado_actual"],
            "estado_nuevo": estado_final,
            "detalle_json": json.dumps(
                {
                    "id_novedad": id_novedad,
                    "id_novedad_resuelta": id_novedad_resuelta,
                    "numero_pedido": numero_pedido,
                    "solucion": solucion,
                    "observaciones": observaciones,
                    "nuevo_estado_pedido": nuevo_estado_pedido,
                    "evidencia_foto_url": evidencia_foto_url,
                }
            ),
        },
    ).scalar_one()

    resuelta = db.execute(
        text(
            """
            update domicilio_novedad
            set
                estado = 'resuelta',
                resuelta_en = timezone('America/Bogota', now()),
                resuelta_por_login = :resuelta_por_login,
                resuelta_por_empleado_id = :resuelta_por_empleado_id,
                solucion = :solucion,
                observaciones_resolucion = :observaciones,
                resultado_pedido_estado = :resultado_pedido_estado,
                auditoria_resolucion_id = :auditoria_resolucion_id,
                updated_at = timezone('America/Bogota', now())
            where id_novedad = :id_novedad
                and estado = 'abierta'
            returning resuelta_en
            """
        ),
        {
            "id_novedad": id_novedad_resuelta,
            "resuelta_por_login": domiciliario.usuario,
            "resuelta_por_empleado_id": domiciliario.id_empleado,
            "solucion": solucion,
            "observaciones": observaciones,
            "resultado_pedido_estado": estado_final,
            "auditoria_resolucion_id": auditoria_id,
        },
    ).mappings().one()
    db.commit()

    return {
        "status": "ok",
        "numero_pedido": numero_pedido,
        "id_novedad": id_novedad_resuelta,
        "estado_novedad": "resuelta",
        "estado_pedido": estado_final,
        "resuelta_en": resuelta["resuelta_en"],
        "mensaje": "Novedad resuelta correctamente",
    }


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
            join estado_pedido ep
                on ep.id_estado_pedido = p.estado_pedido_id
            where p.empresa_id = :empresa_id
                and p.numero_pedido = :numero_pedido
                and (cast(:sucursal_id as bigint) is null or p.sucursal_id = cast(:sucursal_id as bigint))
                and e.domiciliarioid is null
                and ee.codigo = 'pendiente'
                and lower(regexp_replace(trim(ep.nombre_estado), '\s+', ' ', 'g')) = 'aprobado'
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
    auditoria_id = _auditar_cambio_entrega(
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
        "sucursal_id": pedido["sucursal_id"],
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
        "auditoria_id": auditoria_id,
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
