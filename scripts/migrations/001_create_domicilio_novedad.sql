create table if not exists domicilio_novedad (
    id_novedad bigserial primary key,
    empresa_id bigint not null references empresa(id_empresa),
    sucursal_id bigint references sucursal(id_sucursal),
    pedido_id bigint not null references pedido(id_pedido),
    entrega_id bigint not null references entrega(id_entrega),
    domiciliario_id bigint references empleado(id_empleado),
    tipo_novedad varchar(60) not null,
    motivo varchar(180),
    descripcion text,
    evidencia_foto_url text,
    estado varchar(20) not null default 'abierta',
    reportada_en timestamp without time zone not null default timezone('America/Bogota', now()),
    reportada_por_login varchar(120),
    auditoria_reporte_id bigint references domicilio_auditoria(id_audit),
    resuelta_en timestamp without time zone,
    resuelta_por_login varchar(120),
    resuelta_por_empleado_id bigint references empleado(id_empleado),
    solucion text,
    observaciones_resolucion text,
    resultado_pedido_estado varchar(40),
    auditoria_resolucion_id bigint references domicilio_auditoria(id_audit),
    created_at timestamp without time zone not null default timezone('America/Bogota', now()),
    updated_at timestamp without time zone,
    constraint domicilio_novedad_estado_check
        check (estado in ('abierta', 'resuelta', 'cancelada')),
    constraint domicilio_novedad_tipo_check
        check (length(trim(tipo_novedad)) > 0),
    constraint domicilio_novedad_resolucion_check
        check (
            estado = 'abierta'
            or (
                resuelta_en is not null
                and nullif(trim(coalesce(solucion, '')), '') is not null
            )
        )
);

create index if not exists idx_domicilio_novedad_empresa_estado_fecha
    on domicilio_novedad (empresa_id, estado, reportada_en desc);

create index if not exists idx_domicilio_novedad_pedido
    on domicilio_novedad (empresa_id, pedido_id);

create index if not exists idx_domicilio_novedad_entrega
    on domicilio_novedad (empresa_id, entrega_id);

create index if not exists idx_domicilio_novedad_domiciliario_fecha
    on domicilio_novedad (empresa_id, domiciliario_id, reportada_en desc);

create unique index if not exists ux_domicilio_novedad_entrega_abierta
    on domicilio_novedad (empresa_id, entrega_id)
    where estado = 'abierta';
