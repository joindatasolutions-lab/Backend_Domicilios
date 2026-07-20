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
    resuelta_en,
    solucion,
    resultado_pedido_estado,
    created_at
)
select distinct on (da.empresa_id, da.entrega_id)
    da.id_audit,
    da.empresa_id,
    da.sucursal_id,
    da.pedido_id,
    da.entrega_id,
    da.domiciliario_id,
    coalesce(da.detalle_json::jsonb ->> 'tipo_novedad', da.accion),
    coalesce(da.detalle_json::jsonb ->> 'motivo', e.motivonoentregado),
    coalesce(da.detalle_json::jsonb ->> 'descripcion', e.observaciones),
    coalesce(da.detalle_json::jsonb ->> 'evidencia_foto_url', e.evidenciafotourl),
    case
        when ee.codigo = 'no_entregado' then 'abierta'
        else 'resuelta'
    end,
    da.created_at,
    da.actor_login,
    da.id_audit,
    case
        when ee.codigo = 'no_entregado' then null
        else coalesce(e.updatedat, e.fechaentrega, da.created_at)
    end,
    case
        when ee.codigo = 'no_entregado' then null
        else 'Resuelta por cambio de estado del pedido'
    end,
    ee.codigo,
    timezone('America/Bogota', now())
from domicilio_auditoria da
join entrega e
    on e.id_entrega = da.entrega_id
    and e.empresa_id = da.empresa_id
join estado_entrega ee
    on ee.id_estado_entrega = e.estadoentregaid
where (
        da.accion = 'MARCAR_NO_ENTREGADO'
        or da.estado_nuevo = 'no_entregado'
        or da.detalle_json::jsonb ? 'tipo_novedad'
    )
    and da.domiciliario_id is not null
    and not exists (
        select 1
        from domicilio_novedad dn
        where dn.id_novedad = da.id_audit
    )
order by da.empresa_id, da.entrega_id, da.created_at desc, da.id_audit desc
on conflict do nothing;

select setval(
    pg_get_serial_sequence('domicilio_novedad', 'id_novedad'),
    greatest(
        coalesce((select max(id_novedad) from domicilio_novedad), 1),
        coalesce((select last_value from domicilio_novedad_id_novedad_seq), 1)
    )
);
