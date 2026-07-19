# Diccionario de Datos - Esquema `petalops`

Documento generado a partir de los metadatos del esquema PostgreSQL.

## Resumen

| Tablas/Vistas | Columnas | Restricciones |
| --- | --- | --- |
| 51 | 492 | 498 |

## Objetos

| Objeto | Tipo | Descripcion |
| --- | --- | --- |
| barrio | BASE TABLE | Pendiente documentar |
| caja | BASE TABLE | Pendiente documentar |
| canal_venta | BASE TABLE | Pendiente documentar |
| categoria | BASE TABLE | Pendiente documentar |
| cliente | BASE TABLE | Pendiente documentar |
| domicilio_auditoria | BASE TABLE | Pendiente documentar |
| empleado | BASE TABLE | Pendiente documentar |
| empresa | BASE TABLE | Pendiente documentar |
| empresa_menu | BASE TABLE | Pendiente documentar |
| empresa_modulo | BASE TABLE | Pendiente documentar |
| entrega | BASE TABLE | Pendiente documentar |
| estado_entrega | BASE TABLE | Pendiente documentar |
| estado_pago | BASE TABLE | Pendiente documentar |
| estado_pedido | BASE TABLE | Pendiente documentar |
| estado_produccion | BASE TABLE | Pendiente documentar |
| factura | BASE TABLE | Pendiente documentar |
| insumo | BASE TABLE | Pendiente documentar |
| inventario | BASE TABLE | Pendiente documentar |
| metodo_pago_catalogo | BASE TABLE | Pendiente documentar |
| modulo | BASE TABLE | Pendiente documentar |
| movimiento_inventario | BASE TABLE | Pendiente documentar |
| pago | BASE TABLE | Pendiente documentar |
| pago_metodo | BASE TABLE | Pendiente documentar |
| pedido | BASE TABLE | Pendiente documentar |
| pedido_auditoria | BASE TABLE | Pendiente documentar |
| pedido_canal_venta | BASE TABLE | Pendiente documentar |
| pedido_detalle | BASE TABLE | Pendiente documentar |
| pedido_whatsapp_outbox | BASE TABLE | Pendiente documentar |
| perfil_florista | BASE TABLE | Pendiente documentar |
| permiso_modulo | BASE TABLE | Pendiente documentar |
| plan | BASE TABLE | Pendiente documentar |
| plan_modulo | BASE TABLE | Pendiente documentar |
| produccion | BASE TABLE | Pendiente documentar |
| produccion_historial | BASE TABLE | Pendiente documentar |
| producto | BASE TABLE | Pendiente documentar |
| producto_sucursal | BASE TABLE | Pendiente documentar |
| proveedor | BASE TABLE | Pendiente documentar |
| receta | BASE TABLE | Pendiente documentar |
| receta_detalle | BASE TABLE | Pendiente documentar |
| rol | BASE TABLE | Pendiente documentar |
| sucursal | BASE TABLE | Pendiente documentar |
| sucursal_contador_pedido | BASE TABLE | Pendiente documentar |
| tipo_movimiento | BASE TABLE | Pendiente documentar |
| transicion_estado_entrega | BASE TABLE | Pendiente documentar |
| transicion_estado_pedido | BASE TABLE | Pendiente documentar |
| transicion_estado_produccion | BASE TABLE | Pendiente documentar |
| usuario | BASE TABLE | Pendiente documentar |
| usuario_auditoria | BASE TABLE | Pendiente documentar |
| usuario_modulo | BASE TABLE | Pendiente documentar |
| vw_contabilidad_resumen_ventas_diario | VIEW | Resumen diario de ventas por empresa y sucursal. Siempre filtrar por empresa_id y, de ser necesario, por fecha y sucursal. |
| vw_contabilidad_venta_pedido | VIEW | Vista base contable por pedido. Se usa para resumir ventas y efectivo sin duplicar informacion que ya vive en pedido/pago/pago_metodo. |

## `barrio`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_barrio | integer | No | nextval('"Barrio_idBarrio_seq"'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | sucursal_id | bigint | Si |  | Pendiente documentar |
| 4 | zona_id | bigint | No |  | Pendiente documentar |
| 5 | nombre_barrio | character varying(150) | No |  | Pendiente documentar |
| 6 | costo_domicilio | numeric(12,2) | No |  | Pendiente documentar |
| 7 | activo | integer | No |  | Pendiente documentar |
| 8 | created_at | timestamp without time zone | No |  | Pendiente documentar |
| 9 | updated_at | timestamp without time zone | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| Barrio_activo_not_null | CHECK |  | petalops.barrio(activo) |
| Barrio_costoDomicilio_not_null | CHECK |  | petalops.barrio(costo_domicilio) |
| Barrio_createdAt_not_null | CHECK |  | petalops.barrio(created_at) |
| Barrio_empresaID_not_null | CHECK |  | petalops.barrio(empresa_id) |
| Barrio_idBarrio_not_null | CHECK |  | petalops.barrio(id_barrio) |
| Barrio_nombreBarrio_not_null | CHECK |  | petalops.barrio(nombre_barrio) |
| Barrio_zonaID_not_null | CHECK |  | petalops.barrio(zona_id) |
| fk_barrio_empresa | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| fk_barrio_sucursal | FOREIGN KEY | sucursal_id | petalops.sucursal(id_sucursal) |
| Barrio_pkey | PRIMARY KEY | id_barrio | petalops.barrio(id_barrio) |

### Indices

| Nombre | Definicion |
| --- | --- |
| Barrio_pkey | `CREATE UNIQUE INDEX "Barrio_pkey" ON petalops.barrio USING btree (id_barrio)` |
| fk_barrio_sucursal | `CREATE INDEX fk_barrio_sucursal ON petalops.barrio USING btree (sucursal_id)` |
| uk_barrio_empresa_sucursal_nombre | `CREATE UNIQUE INDEX uk_barrio_empresa_sucursal_nombre ON petalops.barrio USING btree (empresa_id, sucursal_id, nombre_barrio)` |

## `caja`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_caja | bigint | No | nextval('caja_id_caja_seq'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | sucursal_id | bigint | No |  | Pendiente documentar |
| 4 | fecha | date | No |  | Pendiente documentar |
| 5 | base | numeric | No | 0 | Pendiente documentar |
| 6 | efectivo | numeric | No | 0 | Pendiente documentar |
| 7 | gasto | numeric | No | 0 | Pendiente documentar |
| 8 | total_efectivo | numeric | No | 0 | Pendiente documentar |
| 9 | guardado | numeric | No | 0 | Pendiente documentar |
| 10 | nueva_base | numeric | No | 0 | Pendiente documentar |
| 11 | observacion | text | Si |  | Pendiente documentar |
| 12 | usuario_id | bigint | Si |  | Pendiente documentar |
| 13 | created_at | timestamp without time zone | No | CURRENT_TIMESTAMP | Pendiente documentar |
| 14 | updated_at | timestamp without time zone | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| caja_base_not_null | CHECK |  | petalops.caja(base) |
| caja_created_at_not_null | CHECK |  | petalops.caja(created_at) |
| caja_efectivo_not_null | CHECK |  | petalops.caja(efectivo) |
| caja_empresa_id_not_null | CHECK |  | petalops.caja(empresa_id) |
| caja_fecha_not_null | CHECK |  | petalops.caja(fecha) |
| caja_gasto_not_null | CHECK |  | petalops.caja(gasto) |
| caja_guardado_not_null | CHECK |  | petalops.caja(guardado) |
| caja_id_caja_not_null | CHECK |  | petalops.caja(id_caja) |
| caja_nueva_base_not_null | CHECK |  | petalops.caja(nueva_base) |
| caja_sucursal_id_not_null | CHECK |  | petalops.caja(sucursal_id) |
| caja_total_efectivo_not_null | CHECK |  | petalops.caja(total_efectivo) |
| caja_empresa_fk | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| caja_sucursal_fk | FOREIGN KEY | sucursal_id | petalops.sucursal(id_sucursal) |
| caja_usuario_fk | FOREIGN KEY | usuario_id | petalops.usuario(id_usuario) |
| caja_pkey | PRIMARY KEY | id_caja | petalops.caja(id_caja) |
| caja_empresa_sucursal_fecha_uk | UNIQUE | empresa_id | petalops.caja(fecha) |
| caja_empresa_sucursal_fecha_uk | UNIQUE | empresa_id | petalops.caja(sucursal_id) |
| caja_empresa_sucursal_fecha_uk | UNIQUE | empresa_id | petalops.caja(empresa_id) |
| caja_empresa_sucursal_fecha_uk | UNIQUE | sucursal_id | petalops.caja(fecha) |
| caja_empresa_sucursal_fecha_uk | UNIQUE | sucursal_id | petalops.caja(sucursal_id) |
| caja_empresa_sucursal_fecha_uk | UNIQUE | sucursal_id | petalops.caja(empresa_id) |
| caja_empresa_sucursal_fecha_uk | UNIQUE | fecha | petalops.caja(empresa_id) |
| caja_empresa_sucursal_fecha_uk | UNIQUE | fecha | petalops.caja(fecha) |
| caja_empresa_sucursal_fecha_uk | UNIQUE | fecha | petalops.caja(sucursal_id) |

### Indices

| Nombre | Definicion |
| --- | --- |
| caja_empresa_sucursal_fecha_uk | `CREATE UNIQUE INDEX caja_empresa_sucursal_fecha_uk ON petalops.caja USING btree (empresa_id, sucursal_id, fecha)` |
| caja_pkey | `CREATE UNIQUE INDEX caja_pkey ON petalops.caja USING btree (id_caja)` |
| idx_caja_empresa_sucursal_fecha | `CREATE INDEX idx_caja_empresa_sucursal_fecha ON petalops.caja USING btree (empresa_id, sucursal_id, fecha DESC)` |

## `canal_venta`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_canal_venta | bigint | No | nextval('canal_venta_id_canal_venta_seq'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | codigo | character varying(80) | No |  | Pendiente documentar |
| 4 | nombre | character varying(120) | No |  | Pendiente documentar |
| 5 | orden | integer | No | 0 | Pendiente documentar |
| 6 | activo | boolean | No | true | Pendiente documentar |
| 7 | created_at | timestamp without time zone | No | now() | Pendiente documentar |
| 8 | updated_at | timestamp without time zone | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| canal_venta_activo_not_null | CHECK |  | petalops.canal_venta(activo) |
| canal_venta_codigo_not_null | CHECK |  | petalops.canal_venta(codigo) |
| canal_venta_created_at_not_null | CHECK |  | petalops.canal_venta(created_at) |
| canal_venta_empresa_id_not_null | CHECK |  | petalops.canal_venta(empresa_id) |
| canal_venta_id_canal_venta_not_null | CHECK |  | petalops.canal_venta(id_canal_venta) |
| canal_venta_nombre_not_null | CHECK |  | petalops.canal_venta(nombre) |
| canal_venta_orden_not_null | CHECK |  | petalops.canal_venta(orden) |
| canal_venta_pkey | PRIMARY KEY | id_canal_venta | petalops.canal_venta(id_canal_venta) |

### Indices

| Nombre | Definicion |
| --- | --- |
| canal_venta_pkey | `CREATE UNIQUE INDEX canal_venta_pkey ON petalops.canal_venta USING btree (id_canal_venta)` |
| ux_canal_venta_empresa_codigo | `CREATE UNIQUE INDEX ux_canal_venta_empresa_codigo ON petalops.canal_venta USING btree (empresa_id, codigo)` |
| ux_canal_venta_empresa_nombre | `CREATE UNIQUE INDEX ux_canal_venta_empresa_nombre ON petalops.canal_venta USING btree (empresa_id, nombre)` |

## `categoria`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_categoria | bigint | No | nextval('categorias_id_categoria_seq'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | nombre | character varying(120) | No |  | Pendiente documentar |
| 4 | created_at | timestamp with time zone | No | now() | Pendiente documentar |
| 5 | activo | boolean | No | true | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| categoria_activo_not_null | CHECK |  | petalops.categoria(activo) |
| categorias_created_at_not_null | CHECK |  | petalops.categoria(created_at) |
| categorias_empresaID_not_null | CHECK |  | petalops.categoria(empresa_id) |
| categorias_id_categoria_not_null | CHECK |  | petalops.categoria(id_categoria) |
| categorias_nombre_not_null | CHECK |  | petalops.categoria(nombre) |
| categorias_empresaID_fkey | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| categorias_pkey | PRIMARY KEY | id_categoria | petalops.categoria(id_categoria) |

### Indices

| Nombre | Definicion |
| --- | --- |
| categorias_pkey | `CREATE UNIQUE INDEX categorias_pkey ON petalops.categoria USING btree (id_categoria)` |
| ix_categorias_empresaID | `CREATE INDEX "ix_categorias_empresaID" ON petalops.categoria USING btree (empresa_id)` |
| ux_categorias_empresaid_nombre_normalizado | `CREATE UNIQUE INDEX ux_categorias_empresaid_nombre_normalizado ON petalops.categoria USING btree (empresa_id, lower(btrim((nombre)::text)))` |

## `cliente`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | cliente_id | integer | No | nextval('cliente_cliente_id_seq'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | tipo_ident | character varying(30) | Si |  | Pendiente documentar |
| 4 | identificacion | character varying(50) | No |  | Pendiente documentar |
| 5 | indicativo | character varying(10) | Si |  | Pendiente documentar |
| 6 | telefono_completo | character varying(40) | Si |  | Pendiente documentar |
| 7 | nombre_completo | character varying(200) | No |  | Pendiente documentar |
| 8 | telefono | character varying(30) | Si |  | Pendiente documentar |
| 9 | email | character varying(150) | Si |  | Pendiente documentar |
| 10 | activo | integer | No |  | Pendiente documentar |
| 11 | created_at | timestamp without time zone | No |  | Pendiente documentar |
| 12 | updated_at | timestamp without time zone | Si |  | Pendiente documentar |
| 13 | fecha_cumpleanos | date | Si |  | Pendiente documentar |
| 14 | fecha_aniversario | date | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| Cliente_activo_not_null | CHECK |  | petalops.cliente(activo) |
| Cliente_createdAt_not_null | CHECK |  | petalops.cliente(created_at) |
| Cliente_empresaID_not_null | CHECK |  | petalops.cliente(empresa_id) |
| Cliente_idCliente_not_null | CHECK |  | petalops.cliente(cliente_id) |
| Cliente_identificacion_not_null | CHECK |  | petalops.cliente(identificacion) |
| Cliente_nombreCompleto_not_null | CHECK |  | petalops.cliente(nombre_completo) |
| fk_cliente_empresa | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| Cliente_pkey | PRIMARY KEY | cliente_id | petalops.cliente(cliente_id) |

### Indices

| Nombre | Definicion |
| --- | --- |
| Cliente_pkey | `CREATE UNIQUE INDEX "Cliente_pkey" ON petalops.cliente USING btree (cliente_id)` |
| uk_cliente_empresa_identificacion | `CREATE UNIQUE INDEX uk_cliente_empresa_identificacion ON petalops.cliente USING btree (empresa_id, identificacion)` |

## `domicilio_auditoria`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_audit | bigint | No | nextval('domicilio_auditoria_id_audit_seq'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | sucursal_id | bigint | Si |  | Pendiente documentar |
| 4 | pedido_id | bigint | No |  | Pendiente documentar |
| 5 | entrega_id | bigint | No |  | Pendiente documentar |
| 6 | actor_user_id | bigint | Si |  | Pendiente documentar |
| 7 | actor_login | character varying(120) | No |  | Pendiente documentar |
| 8 | domiciliario_id | bigint | Si |  | Pendiente documentar |
| 9 | accion | character varying(60) | No |  | Pendiente documentar |
| 10 | estado_anterior | character varying(40) | Si |  | Pendiente documentar |
| 11 | estado_nuevo | character varying(40) | Si |  | Pendiente documentar |
| 12 | detalle_json | text | Si |  | Pendiente documentar |
| 13 | created_at | timestamp without time zone | No | CURRENT_TIMESTAMP | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| domicilio_auditoria_accion_not_null | CHECK |  | petalops.domicilio_auditoria(accion) |
| domicilio_auditoria_actor_login_not_null | CHECK |  | petalops.domicilio_auditoria(actor_login) |
| domicilio_auditoria_created_at_not_null | CHECK |  | petalops.domicilio_auditoria(created_at) |
| domicilio_auditoria_empresa_id_not_null | CHECK |  | petalops.domicilio_auditoria(empresa_id) |
| domicilio_auditoria_entrega_id_not_null | CHECK |  | petalops.domicilio_auditoria(entrega_id) |
| domicilio_auditoria_id_audit_not_null | CHECK |  | petalops.domicilio_auditoria(id_audit) |
| domicilio_auditoria_pedido_id_not_null | CHECK |  | petalops.domicilio_auditoria(pedido_id) |
| domicilio_auditoria_pkey | PRIMARY KEY | id_audit | petalops.domicilio_auditoria(id_audit) |

### Indices

| Nombre | Definicion |
| --- | --- |
| domicilio_auditoria_pkey | `CREATE UNIQUE INDEX domicilio_auditoria_pkey ON petalops.domicilio_auditoria USING btree (id_audit)` |
| idx_domicilio_auditoria_empresa_fecha | `CREATE INDEX idx_domicilio_auditoria_empresa_fecha ON petalops.domicilio_auditoria USING btree (empresa_id, created_at DESC)` |
| idx_domicilio_auditoria_pedido | `CREATE INDEX idx_domicilio_auditoria_pedido ON petalops.domicilio_auditoria USING btree (empresa_id, pedido_id)` |

## `empleado`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_empleado | integer | No | nextval('"Empleado_idEmpleado_seq"'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | sucursal_id | bigint | Si |  | Pendiente documentar |
| 4 | nombre_empleado | character varying(150) | No |  | Pendiente documentar |
| 5 | cargo | character varying(100) | No |  | Pendiente documentar |
| 6 | activo | integer | No |  | Pendiente documentar |
| 7 | created_at | timestamp without time zone | No |  | Pendiente documentar |
| 8 | updated_at | timestamp without time zone | Si |  | Pendiente documentar |
| 9 | usuario | character varying(120) | Si |  | Pendiente documentar |
| 10 | email | character varying(255) | Si |  | Pendiente documentar |
| 11 | password_hash | character varying(255) | Si |  | Pendiente documentar |
| 12 | identificacion | character varying(50) | Si |  | Pendiente documentar |
| 13 | last_login | timestamp without time zone | Si |  | Pendiente documentar |
| 14 | usuario_id | bigint | Si |  | Pendiente documentar |
| 15 | is_superuser | integer | Si | 0 | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| Empleado_activo_not_null | CHECK |  | petalops.empleado(activo) |
| Empleado_createdAt_not_null | CHECK |  | petalops.empleado(created_at) |
| Empleado_empresaID_not_null | CHECK |  | petalops.empleado(empresa_id) |
| Empleado_idEmpleado_not_null | CHECK |  | petalops.empleado(id_empleado) |
| Empleado_nombreEmpleado_not_null | CHECK |  | petalops.empleado(nombre_empleado) |
| Empleado_rol_not_null | CHECK |  | petalops.empleado(cargo) |
| empleado_usuario_id_fkey | FOREIGN KEY | usuario_id | petalops.usuario(id_usuario) |
| fk_empleado_empresa_id | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| fk_empleado_sucursal_id | FOREIGN KEY | sucursal_id | petalops.sucursal(id_sucursal) |
| Empleado_pkey | PRIMARY KEY | id_empleado | petalops.empleado(id_empleado) |

### Indices

| Nombre | Definicion |
| --- | --- |
| Empleado_pkey | `CREATE UNIQUE INDEX "Empleado_pkey" ON petalops.empleado USING btree (id_empleado)` |
| fk_empleado_empresa | `CREATE INDEX fk_empleado_empresa ON petalops.empleado USING btree (empresa_id)` |
| fk_empleado_sucursal | `CREATE INDEX fk_empleado_sucursal ON petalops.empleado USING btree (sucursal_id)` |
| ux_empleado_email_empresa | `CREATE UNIQUE INDEX ux_empleado_email_empresa ON petalops.empleado USING btree (email, empresa_id)` |
| ux_empleado_identificacion_empresa | `CREATE UNIQUE INDEX ux_empleado_identificacion_empresa ON petalops.empleado USING btree (identificacion, empresa_id)` |
| ux_empleado_usuario_empresa | `CREATE UNIQUE INDEX ux_empleado_usuario_empresa ON petalops.empleado USING btree (usuario, empresa_id)` |

## `empresa`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_empresa | integer | No | nextval('"Empresa_idEmpresa_seq"'::regclass) | Pendiente documentar |
| 2 | nombre_empresa | character varying(150) | No |  | Pendiente documentar |
| 3 | nit | character varying(30) | No |  | Pendiente documentar |
| 4 | estado | integer | No |  | Pendiente documentar |
| 5 | created_at | timestamp without time zone | No |  | Pendiente documentar |
| 6 | updated_at | timestamp without time zone | No |  | Pendiente documentar |
| 9 | dominio | character varying(120) | Si |  | Pendiente documentar |
| 10 | slug | character varying(50) | Si |  | Pendiente documentar |
| 11 | logo_url | character varying(500) | Si |  | Pendiente documentar |
| 12 | nombre_comercial | character varying(180) | Si |  | Pendiente documentar |
| 13 | plan_id | bigint | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| Empresa_createdAt_not_null | CHECK |  | petalops.empresa(created_at) |
| Empresa_estado_not_null | CHECK |  | petalops.empresa(estado) |
| Empresa_idEmpresa_not_null | CHECK |  | petalops.empresa(id_empresa) |
| Empresa_nit_not_null | CHECK |  | petalops.empresa(nit) |
| Empresa_nombreEmpresa_not_null | CHECK |  | petalops.empresa(nombre_empresa) |
| Empresa_updatedAt_not_null | CHECK |  | petalops.empresa(updated_at) |
| fk_empresa_plan | FOREIGN KEY | plan_id | petalops.plan(id_plan) |
| Empresa_pkey | PRIMARY KEY | id_empresa | petalops.empresa(id_empresa) |

### Indices

| Nombre | Definicion |
| --- | --- |
| Empresa_pkey | `CREATE UNIQUE INDEX "Empresa_pkey" ON petalops.empresa USING btree (id_empresa)` |
| idx_empresa_dominio | `CREATE INDEX idx_empresa_dominio ON petalops.empresa USING btree (dominio)` |
| ix_Empresa_slug | `CREATE INDEX "ix_Empresa_slug" ON petalops.empresa USING btree (slug)` |
| uk_empresa_nit | `CREATE UNIQUE INDEX uk_empresa_nit ON petalops.empresa USING btree (nit)` |
| uk_empresa_nombre | `CREATE UNIQUE INDEX uk_empresa_nombre ON petalops.empresa USING btree (nombre_empresa)` |
| uk_empresa_slug | `CREATE UNIQUE INDEX uk_empresa_slug ON petalops.empresa USING btree (slug)` |

## `empresa_menu`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_empresa_menu | bigint | No | nextval('empresa_menu_id_empresa_menu_seq'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | codigo | character varying(80) | No |  | Pendiente documentar |
| 4 | titulo | character varying(120) | No |  | Pendiente documentar |
| 5 | seccion | character varying(80) | No | 'pedido_detalle'::character varying | Pendiente documentar |
| 6 | tipo_control | character varying(40) | No |  | Pendiente documentar |
| 7 | opciones_json | jsonb | Si |  | Pendiente documentar |
| 8 | requerido_aprobacion | boolean | No | false | Pendiente documentar |
| 9 | activo | boolean | No | true | Pendiente documentar |
| 10 | orden | integer | No | 0 | Pendiente documentar |
| 11 | created_at | timestamp without time zone | No | now() | Pendiente documentar |
| 12 | updated_at | timestamp without time zone | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| empresa_menu_activo_not_null | CHECK |  | petalops.empresa_menu(activo) |
| empresa_menu_codigo_not_null | CHECK |  | petalops.empresa_menu(codigo) |
| empresa_menu_created_at_not_null | CHECK |  | petalops.empresa_menu(created_at) |
| empresa_menu_empresa_id_not_null | CHECK |  | petalops.empresa_menu(empresa_id) |
| empresa_menu_id_empresa_menu_not_null | CHECK |  | petalops.empresa_menu(id_empresa_menu) |
| empresa_menu_orden_not_null | CHECK |  | petalops.empresa_menu(orden) |
| empresa_menu_requerido_aprobacion_not_null | CHECK |  | petalops.empresa_menu(requerido_aprobacion) |
| empresa_menu_seccion_not_null | CHECK |  | petalops.empresa_menu(seccion) |
| empresa_menu_tipo_control_not_null | CHECK |  | petalops.empresa_menu(tipo_control) |
| empresa_menu_titulo_not_null | CHECK |  | petalops.empresa_menu(titulo) |
| empresa_menu_pkey | PRIMARY KEY | id_empresa_menu | petalops.empresa_menu(id_empresa_menu) |

### Indices

| Nombre | Definicion |
| --- | --- |
| empresa_menu_pkey | `CREATE UNIQUE INDEX empresa_menu_pkey ON petalops.empresa_menu USING btree (id_empresa_menu)` |
| ux_empresa_menu_empresa_codigo_seccion | `CREATE UNIQUE INDEX ux_empresa_menu_empresa_codigo_seccion ON petalops.empresa_menu USING btree (empresa_id, codigo, seccion)` |

## `empresa_modulo`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | empresa_id | bigint | No |  | Pendiente documentar |
| 2 | modulo | character varying(80) | No |  | Pendiente documentar |
| 3 | activo | integer | No |  | Pendiente documentar |
| 4 | updatedat | timestamp without time zone | No |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| EmpresaModulo_activo_not_null | CHECK |  | petalops.empresa_modulo(activo) |
| EmpresaModulo_empresaID_not_null | CHECK |  | petalops.empresa_modulo(empresa_id) |
| EmpresaModulo_modulo_not_null | CHECK |  | petalops.empresa_modulo(modulo) |
| EmpresaModulo_updatedAt_not_null | CHECK |  | petalops.empresa_modulo(updatedat) |
| fk_empresa_modulo_empresa_id | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| EmpresaModulo_pkey | PRIMARY KEY | empresa_id | petalops.empresa_modulo(modulo) |
| EmpresaModulo_pkey | PRIMARY KEY | empresa_id | petalops.empresa_modulo(empresa_id) |
| EmpresaModulo_pkey | PRIMARY KEY | modulo | petalops.empresa_modulo(modulo) |
| EmpresaModulo_pkey | PRIMARY KEY | modulo | petalops.empresa_modulo(empresa_id) |

### Indices

| Nombre | Definicion |
| --- | --- |
| EmpresaModulo_pkey | `CREATE UNIQUE INDEX "EmpresaModulo_pkey" ON petalops.empresa_modulo USING btree (empresa_id, modulo)` |
| idx_empresa_modulo_activo | `CREATE INDEX idx_empresa_modulo_activo ON petalops.empresa_modulo USING btree (empresa_id, activo)` |

## `entrega`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_entrega | integer | No | nextval('"Entrega_idEntrega_seq"'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | pedido_id | bigint | No |  | Pendiente documentar |
| 4 | empleado_id | bigint | Si |  | Pendiente documentar |
| 5 | estadoentregaid | bigint | No |  | Pendiente documentar |
| 6 | tipoentrega | character varying(30) | Si |  | Pendiente documentar |
| 7 | destinatario | character varying(200) | Si |  | Pendiente documentar |
| 8 | telefonodestino | character varying(30) | Si |  | Pendiente documentar |
| 9 | direccion | character varying(250) | Si |  | Pendiente documentar |
| 10 | barrioid | bigint | Si |  | Pendiente documentar |
| 11 | barrionombre | character varying(150) | Si |  | Pendiente documentar |
| 12 | fechasalida | timestamp without time zone | Si |  | Pendiente documentar |
| 13 | fechaentrega | timestamp without time zone | Si |  | Pendiente documentar |
| 14 | rangohora | character varying(100) | Si |  | Pendiente documentar |
| 15 | mensaje | text | Si |  | Pendiente documentar |
| 16 | firma | character varying(150) | Si |  | Pendiente documentar |
| 17 | observaciongeneral | text | Si |  | Pendiente documentar |
| 18 | createdat | timestamp without time zone | No |  | Pendiente documentar |
| 19 | updatedat | timestamp without time zone | Si |  | Pendiente documentar |
| 20 | sucursalid | bigint | Si |  | Pendiente documentar |
| 21 | produccionid | bigint | Si |  | Pendiente documentar |
| 22 | domiciliarioid | bigint | Si |  | Pendiente documentar |
| 23 | fechaasignacion | timestamp without time zone | Si |  | Pendiente documentar |
| 24 | fechaentregaprogramada | timestamp without time zone | Si |  | Pendiente documentar |
| 26 | latitudentrega | numeric(10,7) | Si |  | Pendiente documentar |
| 27 | longitudentrega | numeric(10,7) | Si |  | Pendiente documentar |
| 28 | firmanombre | character varying(180) | Si |  | Pendiente documentar |
| 29 | firmadocumento | character varying(50) | Si |  | Pendiente documentar |
| 30 | firmaimagenurl | text | Si |  | Pendiente documentar |
| 31 | evidenciafotourl | text | Si |  | Pendiente documentar |
| 32 | observaciones | text | Si |  | Pendiente documentar |
| 33 | motivonoentregado | text | Si |  | Pendiente documentar |
| 34 | intentonumero | integer | No |  | Pendiente documentar |
| 35 | reprogramadapara | timestamp without time zone | Si |  | Pendiente documentar |
| 36 | latituddestino | numeric(10,7) | Si |  | Coordenada snapshot del destino usada para cálculo de distancia y trazabilidad operativa. |
| 37 | longituddestino | numeric(10,7) | Si |  | Coordenada snapshot del destino usada para cálculo de distancia y trazabilidad operativa. |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| Entrega_createdAt_not_null | CHECK |  | petalops.entrega(createdat) |
| Entrega_empresaID_not_null | CHECK |  | petalops.entrega(empresa_id) |
| Entrega_estadoEntregaID_not_null | CHECK |  | petalops.entrega(estadoentregaid) |
| Entrega_idEntrega_not_null | CHECK |  | petalops.entrega(id_entrega) |
| Entrega_intentoNumero_not_null | CHECK |  | petalops.entrega(intentonumero) |
| Entrega_pedidoID_not_null | CHECK |  | petalops.entrega(pedido_id) |
| fk_entrega_domiciliario | FOREIGN KEY | domiciliarioid | petalops.empleado(id_empleado) |
| fk_entrega_empleado_id | FOREIGN KEY | empleado_id | petalops.empleado(id_empleado) |
| fk_entrega_empresa_id | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| fk_entrega_estado | FOREIGN KEY | estadoentregaid | petalops.estado_entrega(id_estado_entrega) |
| fk_entrega_pedido_id | FOREIGN KEY | pedido_id | petalops.pedido(id_pedido) |
| fk_entrega_produccion | FOREIGN KEY | produccionid | petalops.produccion(id_produccion) |
| Entrega_pkey | PRIMARY KEY | id_entrega | petalops.entrega(id_entrega) |

### Indices

| Nombre | Definicion |
| --- | --- |
| Entrega_pkey | `CREATE UNIQUE INDEX "Entrega_pkey" ON petalops.entrega USING btree (id_entrega)` |
| fk_entrega_empleado | `CREATE INDEX fk_entrega_empleado ON petalops.entrega USING btree (empleado_id)` |
| fk_entrega_pedido | `CREATE INDEX fk_entrega_pedido ON petalops.entrega USING btree (pedido_id)` |
| idx_entrega_empresa_fecha | `CREATE INDEX idx_entrega_empresa_fecha ON petalops.entrega USING btree (empresa_id, fechaentrega)` |
| idx_entrega_empresa_fecha_programada | `CREATE INDEX idx_entrega_empresa_fecha_programada ON petalops.entrega USING btree (empresa_id, fechaentregaprogramada)` |
| idx_entrega_produccion | `CREATE INDEX idx_entrega_produccion ON petalops.entrega USING btree (produccionid)` |

## `estado_entrega`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_estado_entrega | integer | No | nextval('estado_entrega_id_estado_entrega_seq'::regclass) | Pendiente documentar |
| 2 | codigo | character varying(30) | No |  | Pendiente documentar |
| 3 | nombre | character varying(50) | No |  | Pendiente documentar |
| 4 | orden | integer | Si |  | Pendiente documentar |
| 5 | created_at | timestamp without time zone | Si | now() | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| estado_entrega_codigo_not_null | CHECK |  | petalops.estado_entrega(codigo) |
| estado_entrega_id_estado_entrega_not_null | CHECK |  | petalops.estado_entrega(id_estado_entrega) |
| estado_entrega_nombre_not_null | CHECK |  | petalops.estado_entrega(nombre) |
| estado_entrega_pkey | PRIMARY KEY | id_estado_entrega | petalops.estado_entrega(id_estado_entrega) |
| estado_entrega_codigo_key | UNIQUE | codigo | petalops.estado_entrega(codigo) |

### Indices

| Nombre | Definicion |
| --- | --- |
| estado_entrega_codigo_key | `CREATE UNIQUE INDEX estado_entrega_codigo_key ON petalops.estado_entrega USING btree (codigo)` |
| estado_entrega_pkey | `CREATE UNIQUE INDEX estado_entrega_pkey ON petalops.estado_entrega USING btree (id_estado_entrega)` |

## `estado_pago`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_estado_pago | integer | No | nextval('estado_pago_id_estado_pago_seq'::regclass) | Pendiente documentar |
| 2 | codigo | character varying(30) | Si |  | Pendiente documentar |
| 3 | nombre | character varying(50) | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| estado_pago_id_estado_pago_not_null | CHECK |  | petalops.estado_pago(id_estado_pago) |
| estado_pago_pkey | PRIMARY KEY | id_estado_pago | petalops.estado_pago(id_estado_pago) |
| estado_pago_codigo_key | UNIQUE | codigo | petalops.estado_pago(codigo) |

### Indices

| Nombre | Definicion |
| --- | --- |
| estado_pago_codigo_key | `CREATE UNIQUE INDEX estado_pago_codigo_key ON petalops.estado_pago USING btree (codigo)` |
| estado_pago_pkey | `CREATE UNIQUE INDEX estado_pago_pkey ON petalops.estado_pago USING btree (id_estado_pago)` |

## `estado_pedido`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_estado_pedido | integer | No | nextval('"EstadoPedido_idEstadoPedido_seq"'::regclass) | Pendiente documentar |
| 2 | nombre_estado | character varying(100) | No |  | Pendiente documentar |
| 3 | descripcion | character varying(250) | Si |  | Pendiente documentar |
| 4 | orden | integer | Si |  | Pendiente documentar |
| 5 | activo | integer | Si |  | Pendiente documentar |
| 6 | created_at | timestamp without time zone | Si |  | Pendiente documentar |
| 7 | updated_at | timestamp without time zone | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| EstadoPedido_idEstadoPedido_not_null | CHECK |  | petalops.estado_pedido(id_estado_pedido) |
| EstadoPedido_nombreEstado_not_null | CHECK |  | petalops.estado_pedido(nombre_estado) |
| EstadoPedido_pkey | PRIMARY KEY | id_estado_pedido | petalops.estado_pedido(id_estado_pedido) |

### Indices

| Nombre | Definicion |
| --- | --- |
| EstadoPedido_pkey | `CREATE UNIQUE INDEX "EstadoPedido_pkey" ON petalops.estado_pedido USING btree (id_estado_pedido)` |

## `estado_produccion`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_estado_produccion | integer | No | nextval('estado_produccion_id_estado_produccion_seq'::regclass) | Pendiente documentar |
| 2 | codigo | character varying(30) | No |  | Pendiente documentar |
| 3 | nombre | character varying(50) | No |  | Pendiente documentar |
| 4 | orden | integer | Si |  | Pendiente documentar |
| 5 | created_at | timestamp without time zone | Si | CURRENT_TIMESTAMP | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| estado_produccion_codigo_not_null | CHECK |  | petalops.estado_produccion(codigo) |
| estado_produccion_id_estado_produccion_not_null | CHECK |  | petalops.estado_produccion(id_estado_produccion) |
| estado_produccion_nombre_not_null | CHECK |  | petalops.estado_produccion(nombre) |
| estado_produccion_pkey | PRIMARY KEY | id_estado_produccion | petalops.estado_produccion(id_estado_produccion) |
| estado_produccion_codigo_key | UNIQUE | codigo | petalops.estado_produccion(codigo) |

### Indices

| Nombre | Definicion |
| --- | --- |
| estado_produccion_codigo_key | `CREATE UNIQUE INDEX estado_produccion_codigo_key ON petalops.estado_produccion USING btree (codigo)` |
| estado_produccion_pkey | `CREATE UNIQUE INDEX estado_produccion_pkey ON petalops.estado_produccion USING btree (id_estado_produccion)` |

## `factura`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_factura | integer | No | nextval('"Factura_idFactura_seq"'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | pedido_id | bigint | No |  | Pendiente documentar |
| 4 | numero_factura | character varying(50) | No |  | Pendiente documentar |
| 5 | fecha_factura | timestamp without time zone | No | now() | Pendiente documentar |
| 6 | total_factura | numeric(14,2) | No |  | Pendiente documentar |
| 7 | created_at | timestamp without time zone | No | now() | Pendiente documentar |
| 8 | updated_at | timestamp without time zone | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| Factura_createdAt_not_null | CHECK |  | petalops.factura(created_at) |
| Factura_empresaID_not_null | CHECK |  | petalops.factura(empresa_id) |
| Factura_fechaFactura_not_null | CHECK |  | petalops.factura(fecha_factura) |
| Factura_idFactura_not_null | CHECK |  | petalops.factura(id_factura) |
| Factura_numeroFactura_not_null | CHECK |  | petalops.factura(numero_factura) |
| Factura_pedidoID_not_null | CHECK |  | petalops.factura(pedido_id) |
| Factura_totalFactura_not_null | CHECK |  | petalops.factura(total_factura) |
| fk_factura_empresa | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| fk_factura_pedido | FOREIGN KEY | pedido_id | petalops.pedido(id_pedido) |
| Factura_pkey | PRIMARY KEY | id_factura | petalops.factura(id_factura) |
| uk_factura_empresa_numero | UNIQUE | empresa_id | petalops.factura(empresa_id) |
| uk_factura_empresa_numero | UNIQUE | empresa_id | petalops.factura(numero_factura) |
| uk_factura_empresa_numero | UNIQUE | numero_factura | petalops.factura(empresa_id) |
| uk_factura_empresa_numero | UNIQUE | numero_factura | petalops.factura(numero_factura) |
| uk_factura_pedido | UNIQUE | pedido_id | petalops.factura(pedido_id) |

### Indices

| Nombre | Definicion |
| --- | --- |
| Factura_pkey | `CREATE UNIQUE INDEX "Factura_pkey" ON petalops.factura USING btree (id_factura)` |
| fk_factura_pedido | `CREATE INDEX fk_factura_pedido ON petalops.factura USING btree (pedido_id)` |
| uk_factura_empresa_numero | `CREATE UNIQUE INDEX uk_factura_empresa_numero ON petalops.factura USING btree (empresa_id, numero_factura)` |
| uk_factura_pedido | `CREATE UNIQUE INDEX uk_factura_pedido ON petalops.factura USING btree (pedido_id)` |

## `insumo`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_insumo | integer | No | nextval('insumo_id_insumo_seq'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | codigo_barra | character varying(100) | Si |  | Pendiente documentar |
| 4 | nombre_insumo | character varying(200) | No |  | Pendiente documentar |
| 5 | unidad_medida | character varying(50) | No |  | Pendiente documentar |
| 6 | activo | boolean | No | true | Pendiente documentar |
| 7 | created_at | timestamp without time zone | No | now() | Pendiente documentar |
| 8 | updated_at | timestamp without time zone | Si |  | Pendiente documentar |
| 9 | proveedor_id | integer | Si |  | Pendiente documentar |
| 10 | categoria | character varying(80) | Si |  | Pendiente documentar |
| 11 | subcategoria | character varying(80) | Si |  | Pendiente documentar |
| 12 | color | character varying(80) | Si |  | Pendiente documentar |
| 13 | descripcion | text | Si |  | Pendiente documentar |
| 14 | tamano | character varying(50) | Si |  | Pendiente documentar |
| 15 | fecha_vencimiento | date | Si |  | Pendiente documentar |
| 16 | marca | character varying(100) | Si |  | Marca del producto (uso principal: módulo Adicionales) |
| 17 | precio_venta | numeric(12,2) | Si |  | Precio de venta (uso principal: módulo Adicionales — permite calcular utilidad) |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| insumo_activo_not_null | CHECK |  | petalops.insumo(activo) |
| insumo_created_at_not_null | CHECK |  | petalops.insumo(created_at) |
| insumo_empresa_id_not_null | CHECK |  | petalops.insumo(empresa_id) |
| insumo_id_insumo_not_null | CHECK |  | petalops.insumo(id_insumo) |
| insumo_nombre_insumo_not_null | CHECK |  | petalops.insumo(nombre_insumo) |
| insumo_unidad_medida_not_null | CHECK |  | petalops.insumo(unidad_medida) |
| fk_insumo_empresa | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| insumo_proveedor_id_fkey | FOREIGN KEY | proveedor_id | petalops.proveedor(id_proveedor) |
| insumo_pkey | PRIMARY KEY | id_insumo | petalops.insumo(id_insumo) |
| uk_insumo_empresa_codigo_barra | UNIQUE | empresa_id | petalops.insumo(codigo_barra) |
| uk_insumo_empresa_codigo_barra | UNIQUE | empresa_id | petalops.insumo(empresa_id) |
| uk_insumo_empresa_codigo_barra | UNIQUE | codigo_barra | petalops.insumo(codigo_barra) |
| uk_insumo_empresa_codigo_barra | UNIQUE | codigo_barra | petalops.insumo(empresa_id) |
| uk_insumo_empresa_nombre | UNIQUE | empresa_id | petalops.insumo(nombre_insumo) |
| uk_insumo_empresa_nombre | UNIQUE | empresa_id | petalops.insumo(empresa_id) |
| uk_insumo_empresa_nombre | UNIQUE | nombre_insumo | petalops.insumo(nombre_insumo) |
| uk_insumo_empresa_nombre | UNIQUE | nombre_insumo | petalops.insumo(empresa_id) |

### Indices

| Nombre | Definicion |
| --- | --- |
| idx_insumo_empresa_categoria | `CREATE INDEX idx_insumo_empresa_categoria ON petalops.insumo USING btree (empresa_id, categoria)` |
| insumo_pkey | `CREATE UNIQUE INDEX insumo_pkey ON petalops.insumo USING btree (id_insumo)` |
| uk_insumo_empresa_codigo_barra | `CREATE UNIQUE INDEX uk_insumo_empresa_codigo_barra ON petalops.insumo USING btree (empresa_id, codigo_barra)` |
| uk_insumo_empresa_nombre | `CREATE UNIQUE INDEX uk_insumo_empresa_nombre ON petalops.insumo USING btree (empresa_id, nombre_insumo)` |

## `inventario`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_inventario | integer | No | nextval('"Inventario_idInventario_seq"'::regclass) | Pendiente documentar |
| 4 | sucursal_id | bigint | No |  | Pendiente documentar |
| 5 | stock_actual | numeric(12,4) | No |  | Pendiente documentar |
| 6 | stock_reservado | numeric(12,4) | No |  | Pendiente documentar |
| 7 | created_at | timestamp without time zone | No |  | Pendiente documentar |
| 8 | updated_at | timestamp without time zone | Si |  | Pendiente documentar |
| 17 | stock_minimo | numeric(12,2) | No |  | Pendiente documentar |
| 18 | valor_unitario | numeric(12,2) | No |  | Pendiente documentar |
| 19 | activo | boolean | No |  | Pendiente documentar |
| 20 | fechaultimaactualizacion | timestamp without time zone | Si |  | Pendiente documentar |
| 21 | empresa_id | bigint | Si |  | Pendiente documentar |
| 22 | insumo_id | bigint | No |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| Inventario_activo_not_null | CHECK |  | petalops.inventario(activo) |
| Inventario_createdAt_not_null | CHECK |  | petalops.inventario(created_at) |
| Inventario_idInventario_not_null | CHECK |  | petalops.inventario(id_inventario) |
| Inventario_stockActual_not_null | CHECK |  | petalops.inventario(stock_actual) |
| Inventario_stockMinimo_not_null | CHECK |  | petalops.inventario(stock_minimo) |
| Inventario_stockReservado_not_null | CHECK |  | petalops.inventario(stock_reservado) |
| Inventario_sucursalID_not_null | CHECK |  | petalops.inventario(sucursal_id) |
| Inventario_valorUnitario_not_null | CHECK |  | petalops.inventario(valor_unitario) |
| inventario_insumo_id_not_null | CHECK |  | petalops.inventario(insumo_id) |
| fk_inventario_empresa | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| fk_inventario_sucursal | FOREIGN KEY | sucursal_id | petalops.sucursal(id_sucursal) |
| inventario_insumo_id_fkey | FOREIGN KEY | insumo_id | petalops.insumo(id_insumo) |
| Inventario_pkey | PRIMARY KEY | id_inventario | petalops.inventario(id_inventario) |
| uq_inventario_empresa | UNIQUE | id_inventario | petalops.inventario(empresa_id) |
| uq_inventario_empresa | UNIQUE | id_inventario | petalops.inventario(id_inventario) |
| uq_inventario_empresa | UNIQUE | empresa_id | petalops.inventario(id_inventario) |
| uq_inventario_empresa | UNIQUE | empresa_id | petalops.inventario(empresa_id) |
| uq_inventario_sucursal_insumo | UNIQUE | sucursal_id | petalops.inventario(sucursal_id) |
| uq_inventario_sucursal_insumo | UNIQUE | sucursal_id | petalops.inventario(insumo_id) |
| uq_inventario_sucursal_insumo | UNIQUE | insumo_id | petalops.inventario(insumo_id) |
| uq_inventario_sucursal_insumo | UNIQUE | insumo_id | petalops.inventario(sucursal_id) |

### Indices

| Nombre | Definicion |
| --- | --- |
| Inventario_pkey | `CREATE UNIQUE INDEX "Inventario_pkey" ON petalops.inventario USING btree (id_inventario)` |
| uq_inventario_empresa | `CREATE UNIQUE INDEX uq_inventario_empresa ON petalops.inventario USING btree (id_inventario, empresa_id)` |
| uq_inventario_sucursal_insumo | `CREATE UNIQUE INDEX uq_inventario_sucursal_insumo ON petalops.inventario USING btree (sucursal_id, insumo_id)` |

## `metodo_pago_catalogo`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_metodo_pago | bigint | No | nextval('metodo_pago_catalogo_id_metodo_pago_seq'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | codigo | character varying(80) | No |  | Pendiente documentar |
| 4 | nombre | character varying(120) | No |  | Pendiente documentar |
| 5 | orden | integer | No | 0 | Pendiente documentar |
| 6 | activo | boolean | No | true | Pendiente documentar |
| 7 | created_at | timestamp without time zone | No | now() | Pendiente documentar |
| 8 | updated_at | timestamp without time zone | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| metodo_pago_catalogo_activo_not_null | CHECK |  | petalops.metodo_pago_catalogo(activo) |
| metodo_pago_catalogo_codigo_not_null | CHECK |  | petalops.metodo_pago_catalogo(codigo) |
| metodo_pago_catalogo_created_at_not_null | CHECK |  | petalops.metodo_pago_catalogo(created_at) |
| metodo_pago_catalogo_empresa_id_not_null | CHECK |  | petalops.metodo_pago_catalogo(empresa_id) |
| metodo_pago_catalogo_id_metodo_pago_not_null | CHECK |  | petalops.metodo_pago_catalogo(id_metodo_pago) |
| metodo_pago_catalogo_nombre_not_null | CHECK |  | petalops.metodo_pago_catalogo(nombre) |
| metodo_pago_catalogo_orden_not_null | CHECK |  | petalops.metodo_pago_catalogo(orden) |
| metodo_pago_catalogo_pkey | PRIMARY KEY | id_metodo_pago | petalops.metodo_pago_catalogo(id_metodo_pago) |

### Indices

| Nombre | Definicion |
| --- | --- |
| metodo_pago_catalogo_pkey | `CREATE UNIQUE INDEX metodo_pago_catalogo_pkey ON petalops.metodo_pago_catalogo USING btree (id_metodo_pago)` |
| ux_metodo_pago_catalogo_empresa_codigo | `CREATE UNIQUE INDEX ux_metodo_pago_catalogo_empresa_codigo ON petalops.metodo_pago_catalogo USING btree (empresa_id, codigo)` |
| ux_metodo_pago_catalogo_empresa_nombre | `CREATE UNIQUE INDEX ux_metodo_pago_catalogo_empresa_nombre ON petalops.metodo_pago_catalogo USING btree (empresa_id, nombre)` |

## `modulo`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_modulo | integer | No | nextval('modulo_id_modulo_seq'::regclass) | Pendiente documentar |
| 2 | codigo | character varying(50) | No |  | Pendiente documentar |
| 3 | nombre | character varying(100) | Si |  | Pendiente documentar |
| 4 | descripcion | text | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| modulo_codigo_not_null | CHECK |  | petalops.modulo(codigo) |
| modulo_id_modulo_not_null | CHECK |  | petalops.modulo(id_modulo) |
| modulo_pkey | PRIMARY KEY | id_modulo | petalops.modulo(id_modulo) |
| uk_modulo_codigo | UNIQUE | codigo | petalops.modulo(codigo) |

### Indices

| Nombre | Definicion |
| --- | --- |
| modulo_pkey | `CREATE UNIQUE INDEX modulo_pkey ON petalops.modulo USING btree (id_modulo)` |
| uk_modulo_codigo | `CREATE UNIQUE INDEX uk_modulo_codigo ON petalops.modulo USING btree (codigo)` |

## `movimiento_inventario`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_movimiento | integer | No | nextval('"MovimientoInventario_idMovimiento_seq"'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | inventario_id | bigint | No |  | Pendiente documentar |
| 5 | cantidad | numeric(12,2) | No |  | Pendiente documentar |
| 6 | fecha | timestamp without time zone | No |  | Pendiente documentar |
| 7 | motivo | character varying(250) | Si |  | Pendiente documentar |
| 8 | usuario_id | bigint | Si |  | Pendiente documentar |
| 9 | created_at | timestamp without time zone | Si |  | Pendiente documentar |
| 10 | tipo_movimiento_id | integer | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| MovimientoInventario_cantidad_not_null | CHECK |  | petalops.movimiento_inventario(cantidad) |
| MovimientoInventario_empresaID_not_null | CHECK |  | petalops.movimiento_inventario(empresa_id) |
| MovimientoInventario_fecha_not_null | CHECK |  | petalops.movimiento_inventario(fecha) |
| MovimientoInventario_idMovimiento_not_null | CHECK |  | petalops.movimiento_inventario(id_movimiento) |
| MovimientoInventario_inventarioID_not_null | CHECK |  | petalops.movimiento_inventario(inventario_id) |
| chk_cantidad_positiva | CHECK |  | petalops.movimiento_inventario(cantidad) |
| fk_movimiento_tipo | FOREIGN KEY | tipo_movimiento_id | petalops.tipo_movimiento(id_tipo_movimiento) |
| fk_movinv_empresa | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| fk_movinv_inventario | FOREIGN KEY | inventario_id | petalops.inventario(id_inventario) |
| fk_movinv_usuario | FOREIGN KEY | usuario_id | petalops.usuario(id_usuario) |
| MovimientoInventario_pkey | PRIMARY KEY | id_movimiento | petalops.movimiento_inventario(id_movimiento) |

### Indices

| Nombre | Definicion |
| --- | --- |
| MovimientoInventario_pkey | `CREATE UNIQUE INDEX "MovimientoInventario_pkey" ON petalops.movimiento_inventario USING btree (id_movimiento)` |
| fk_movinv_usuario | `CREATE INDEX fk_movinv_usuario ON petalops.movimiento_inventario USING btree (usuario_id)` |
| idx_movimiento_empresa_fecha | `CREATE INDEX idx_movimiento_empresa_fecha ON petalops.movimiento_inventario USING btree (empresa_id, fecha)` |
| idx_movimiento_inventario | `CREATE INDEX idx_movimiento_inventario ON petalops.movimiento_inventario USING btree (inventario_id)` |
| idx_movinv_empresa_fecha | `CREATE INDEX idx_movinv_empresa_fecha ON petalops.movimiento_inventario USING btree (empresa_id, fecha)` |
| idx_movinv_inventario_fecha | `CREATE INDEX idx_movinv_inventario_fecha ON petalops.movimiento_inventario USING btree (inventario_id, fecha)` |

## `pago`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_pago | integer | No | nextval('"Pago_idPago_seq"'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | pedido_id | bigint | No |  | Pendiente documentar |
| 4 | proveedor | character varying(50) | No |  | Pendiente documentar |
| 5 | referencia | character varying(120) | Si |  | Pendiente documentar |
| 6 | transaccion_id | character varying(120) | Si |  | Pendiente documentar |
| 8 | moneda | character varying(10) | No |  | Pendiente documentar |
| 9 | monto | numeric(12,2) | No |  | Pendiente documentar |
| 10 | checkouturl | text | Si |  | Pendiente documentar |
| 11 | raw_respuesta | text | Si |  | Pendiente documentar |
| 12 | metodo_pago | character varying(100) | No |  | Pendiente documentar |
| 13 | fecha_pago | timestamp without time zone | No |  | Pendiente documentar |
| 14 | created_at | timestamp without time zone | No |  | Pendiente documentar |
| 15 | updated_at | timestamp without time zone | Si |  | Pendiente documentar |
| 16 | estado_pago_id | integer | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| Pago_createdAt_not_null | CHECK |  | petalops.pago(created_at) |
| Pago_empresaID_not_null | CHECK |  | petalops.pago(empresa_id) |
| Pago_fechaPago_not_null | CHECK |  | petalops.pago(fecha_pago) |
| Pago_idPago_not_null | CHECK |  | petalops.pago(id_pago) |
| Pago_metodoPago_not_null | CHECK |  | petalops.pago(metodo_pago) |
| Pago_moneda_not_null | CHECK |  | petalops.pago(moneda) |
| Pago_monto_not_null | CHECK |  | petalops.pago(monto) |
| Pago_pedidoID_not_null | CHECK |  | petalops.pago(pedido_id) |
| Pago_proveedor_not_null | CHECK |  | petalops.pago(proveedor) |
| fk_pago_empresa | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| fk_pago_estado | FOREIGN KEY | estado_pago_id | petalops.estado_pago(id_estado_pago) |
| fk_pago_pedido | FOREIGN KEY | pedido_id | petalops.pedido(id_pedido) |
| Pago_pkey | PRIMARY KEY | id_pago | petalops.pago(id_pago) |
| uq_pago_pedido | UNIQUE | pedido_id | petalops.pago(pedido_id) |
| uq_pago_transaccion | UNIQUE | transaccion_id | petalops.pago(transaccion_id) |

### Indices

| Nombre | Definicion |
| --- | --- |
| Pago_pkey | `CREATE UNIQUE INDEX "Pago_pkey" ON petalops.pago USING btree (id_pago)` |
| fk_pago_empresa | `CREATE INDEX fk_pago_empresa ON petalops.pago USING btree (empresa_id)` |
| fk_pago_pedido | `CREATE INDEX fk_pago_pedido ON petalops.pago USING btree (pedido_id)` |
| uq_pago_pedido | `CREATE UNIQUE INDEX uq_pago_pedido ON petalops.pago USING btree (pedido_id)` |
| uq_pago_referencia | `CREATE UNIQUE INDEX uq_pago_referencia ON petalops.pago USING btree (referencia)` |
| uq_pago_transaccion | `CREATE UNIQUE INDEX uq_pago_transaccion ON petalops.pago USING btree (transaccion_id)` |

## `pago_metodo`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_pago_metodo | bigint | No | nextval('pago_metodo_id_pago_metodo_seq'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | pago_id | bigint | No |  | Pendiente documentar |
| 4 | pedido_id | bigint | No |  | Pendiente documentar |
| 5 | metodo_pago_id | bigint | No |  | Pendiente documentar |
| 6 | orden | integer | No | 0 | Pendiente documentar |
| 7 | created_at | timestamp without time zone | No | now() | Pendiente documentar |
| 8 | updated_at | timestamp without time zone | Si |  | Pendiente documentar |
| 9 | monto | numeric(12,2) | Si |  | Monto asignado a este metodo dentro del pago del pedido. En pagos mixtos permite saber cuanto fue efectivo, transferencia, etc. |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| pago_metodo_created_at_not_null | CHECK |  | petalops.pago_metodo(created_at) |
| pago_metodo_empresa_id_not_null | CHECK |  | petalops.pago_metodo(empresa_id) |
| pago_metodo_id_pago_metodo_not_null | CHECK |  | petalops.pago_metodo(id_pago_metodo) |
| pago_metodo_metodo_pago_id_not_null | CHECK |  | petalops.pago_metodo(metodo_pago_id) |
| pago_metodo_monto_nonnegative_chk | CHECK |  | petalops.pago_metodo(monto) |
| pago_metodo_orden_not_null | CHECK |  | petalops.pago_metodo(orden) |
| pago_metodo_pago_id_not_null | CHECK |  | petalops.pago_metodo(pago_id) |
| pago_metodo_pedido_id_not_null | CHECK |  | petalops.pago_metodo(pedido_id) |
| pago_metodo_metodo_pago_id_fkey | FOREIGN KEY | metodo_pago_id | petalops.metodo_pago_catalogo(id_metodo_pago) |
| pago_metodo_pago_id_fkey | FOREIGN KEY | pago_id | petalops.pago(id_pago) |
| pago_metodo_pedido_id_fkey | FOREIGN KEY | pedido_id | petalops.pedido(id_pedido) |
| pago_metodo_pkey | PRIMARY KEY | id_pago_metodo | petalops.pago_metodo(id_pago_metodo) |

### Indices

| Nombre | Definicion |
| --- | --- |
| ix_pago_metodo_empresa_pedido | `CREATE INDEX ix_pago_metodo_empresa_pedido ON petalops.pago_metodo USING btree (empresa_id, pedido_id)` |
| pago_metodo_pkey | `CREATE UNIQUE INDEX pago_metodo_pkey ON petalops.pago_metodo USING btree (id_pago_metodo)` |
| ux_pago_metodo_empresa_pedido_metodo | `CREATE UNIQUE INDEX ux_pago_metodo_empresa_pedido_metodo ON petalops.pago_metodo USING btree (empresa_id, pedido_id, metodo_pago_id)` |

## `pedido`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_pedido | integer | No | nextval('"Pedido_idPedido_seq"'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | sucursal_id | bigint | No |  | Pendiente documentar |
| 4 | cliente_id | bigint | No |  | Pendiente documentar |
| 5 | fecha_pedido | timestamp without time zone | No |  | Pendiente documentar |
| 8 | estado_pedido_id | bigint | No |  | Pendiente documentar |
| 9 | version | integer | No |  | Pendiente documentar |
| 10 | motivo_rechazo | character varying(300) | Si |  | Pendiente documentar |
| 11 | total_bruto | numeric(12,2) | No |  | Pendiente documentar |
| 12 | total_iva | numeric(12,2) | No |  | Pendiente documentar |
| 13 | total_neto | numeric(12,2) | No |  | Pendiente documentar |
| 14 | created_at | timestamp without time zone | No |  | Pendiente documentar |
| 15 | updated_at | timestamp without time zone | Si |  | Pendiente documentar |
| 16 | numero_pedido | bigint | Si |  | Pendiente documentar |
| 17 | codigo_pedido | character varying(40) | Si |  | Pendiente documentar |
| 18 | costo_domicilio | numeric(12,2) | No | 0 | Snapshot del costo de domicilio aplicado al pedido en el momento de la venta. |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| Pedido_clienteID_not_null | CHECK |  | petalops.pedido(cliente_id) |
| Pedido_createdAt_not_null | CHECK |  | petalops.pedido(created_at) |
| Pedido_empresaID_not_null | CHECK |  | petalops.pedido(empresa_id) |
| Pedido_estadoPedidoID_not_null | CHECK |  | petalops.pedido(estado_pedido_id) |
| Pedido_fechaPedido_not_null | CHECK |  | petalops.pedido(fecha_pedido) |
| Pedido_idPedido_not_null | CHECK |  | petalops.pedido(id_pedido) |
| Pedido_sucursalID_not_null | CHECK |  | petalops.pedido(sucursal_id) |
| Pedido_totalBruto_not_null | CHECK |  | petalops.pedido(total_bruto) |
| Pedido_totalIva_not_null | CHECK |  | petalops.pedido(total_iva) |
| Pedido_totalNeto_not_null | CHECK |  | petalops.pedido(total_neto) |
| Pedido_version_not_null | CHECK |  | petalops.pedido(version) |
| pedido_costo_domicilio_not_null | CHECK |  | petalops.pedido(costo_domicilio) |
| fk_pedido_cliente | FOREIGN KEY | cliente_id | petalops.cliente(cliente_id) |
| fk_pedido_empresa | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| fk_pedido_estado | FOREIGN KEY | estado_pedido_id | petalops.estado_pedido(id_estado_pedido) |
| fk_pedido_sucursal | FOREIGN KEY | sucursal_id | petalops.sucursal(id_sucursal) |
| Pedido_pkey | PRIMARY KEY | id_pedido | petalops.pedido(id_pedido) |

### Indices

| Nombre | Definicion |
| --- | --- |
| Pedido_pkey | `CREATE UNIQUE INDEX "Pedido_pkey" ON petalops.pedido USING btree (id_pedido)` |
| fk_pedido_cliente | `CREATE INDEX fk_pedido_cliente ON petalops.pedido USING btree (cliente_id)` |
| fk_pedido_estado | `CREATE INDEX fk_pedido_estado ON petalops.pedido USING btree (estado_pedido_id)` |
| fk_pedido_sucursal | `CREATE INDEX fk_pedido_sucursal ON petalops.pedido USING btree (sucursal_id)` |
| idx_pedido_empresa_estado | `CREATE INDEX idx_pedido_empresa_estado ON petalops.pedido USING btree (empresa_id, estado_pedido_id)` |
| uq_pedido_empresa_sucursal_numero | `CREATE UNIQUE INDEX uq_pedido_empresa_sucursal_numero ON petalops.pedido USING btree (empresa_id, sucursal_id, numero_pedido)` |

## `pedido_auditoria`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_audit | bigint | No | nextval('pedido_auditoria_id_audit_seq'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | sucursal_id | bigint | No |  | Pendiente documentar |
| 4 | pedido_id | bigint | No |  | Pendiente documentar |
| 5 | actor_user_id | bigint | Si |  | Pendiente documentar |
| 6 | actor_login | character varying(120) | No |  | Pendiente documentar |
| 7 | accion | character varying(60) | No |  | Pendiente documentar |
| 8 | estado_origen_id | bigint | Si |  | Pendiente documentar |
| 9 | estado_destino_id | bigint | Si |  | Pendiente documentar |
| 10 | detalle_json | text | Si |  | Pendiente documentar |
| 11 | created_at | timestamp without time zone | No | CURRENT_TIMESTAMP | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| pedido_auditoria_accion_not_null | CHECK |  | petalops.pedido_auditoria(accion) |
| pedido_auditoria_actor_login_not_null | CHECK |  | petalops.pedido_auditoria(actor_login) |
| pedido_auditoria_created_at_not_null | CHECK |  | petalops.pedido_auditoria(created_at) |
| pedido_auditoria_empresa_id_not_null | CHECK |  | petalops.pedido_auditoria(empresa_id) |
| pedido_auditoria_id_audit_not_null | CHECK |  | petalops.pedido_auditoria(id_audit) |
| pedido_auditoria_pedido_id_not_null | CHECK |  | petalops.pedido_auditoria(pedido_id) |
| pedido_auditoria_sucursal_id_not_null | CHECK |  | petalops.pedido_auditoria(sucursal_id) |
| pedido_auditoria_pkey | PRIMARY KEY | id_audit | petalops.pedido_auditoria(id_audit) |

### Indices

| Nombre | Definicion |
| --- | --- |
| idx_pedido_auditoria_empresa_fecha | `CREATE INDEX idx_pedido_auditoria_empresa_fecha ON petalops.pedido_auditoria USING btree (empresa_id, created_at DESC)` |
| idx_pedido_auditoria_pedido | `CREATE INDEX idx_pedido_auditoria_pedido ON petalops.pedido_auditoria USING btree (empresa_id, pedido_id)` |
| pedido_auditoria_pkey | `CREATE UNIQUE INDEX pedido_auditoria_pkey ON petalops.pedido_auditoria USING btree (id_audit)` |

## `pedido_canal_venta`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_pedido_canal_venta | bigint | No | nextval('pedido_canal_venta_id_pedido_canal_venta_seq'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | pedido_id | bigint | No |  | Pendiente documentar |
| 4 | canal_venta_id | bigint | No |  | Pendiente documentar |
| 5 | created_at | timestamp without time zone | No | now() | Pendiente documentar |
| 6 | updated_at | timestamp without time zone | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| pedido_canal_venta_canal_venta_id_not_null | CHECK |  | petalops.pedido_canal_venta(canal_venta_id) |
| pedido_canal_venta_created_at_not_null | CHECK |  | petalops.pedido_canal_venta(created_at) |
| pedido_canal_venta_empresa_id_not_null | CHECK |  | petalops.pedido_canal_venta(empresa_id) |
| pedido_canal_venta_id_pedido_canal_venta_not_null | CHECK |  | petalops.pedido_canal_venta(id_pedido_canal_venta) |
| pedido_canal_venta_pedido_id_not_null | CHECK |  | petalops.pedido_canal_venta(pedido_id) |
| pedido_canal_venta_canal_venta_id_fkey | FOREIGN KEY | canal_venta_id | petalops.canal_venta(id_canal_venta) |
| pedido_canal_venta_pedido_id_fkey | FOREIGN KEY | pedido_id | petalops.pedido(id_pedido) |
| pedido_canal_venta_pkey | PRIMARY KEY | id_pedido_canal_venta | petalops.pedido_canal_venta(id_pedido_canal_venta) |

### Indices

| Nombre | Definicion |
| --- | --- |
| pedido_canal_venta_pkey | `CREATE UNIQUE INDEX pedido_canal_venta_pkey ON petalops.pedido_canal_venta USING btree (id_pedido_canal_venta)` |
| ux_pedido_canal_venta_empresa_pedido | `CREATE UNIQUE INDEX ux_pedido_canal_venta_empresa_pedido ON petalops.pedido_canal_venta USING btree (empresa_id, pedido_id)` |

## `pedido_detalle`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_pedido_detalle | integer | No | nextval('"PedidoDetalle_idPedidoDetalle_seq"'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | sucursal_id | bigint | No |  | Pendiente documentar |
| 4 | pedido_id | bigint | No |  | Pendiente documentar |
| 5 | producto_id | bigint | No |  | Pendiente documentar |
| 6 | cantidad | numeric(12,2) | No |  | Pendiente documentar |
| 7 | precio_unitario | numeric(12,2) | No |  | Pendiente documentar |
| 8 | iva_unitario | numeric(12,2) | Si |  | Pendiente documentar |
| 9 | subtotal | numeric(12,2) | No |  | Pendiente documentar |
| 10 | observaciones_personalizados | text | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| PedidoDetalle_cantidad_not_null | CHECK |  | petalops.pedido_detalle(cantidad) |
| PedidoDetalle_empresaID_not_null | CHECK |  | petalops.pedido_detalle(empresa_id) |
| PedidoDetalle_idPedidoDetalle_not_null | CHECK |  | petalops.pedido_detalle(id_pedido_detalle) |
| PedidoDetalle_pedidoID_not_null | CHECK |  | petalops.pedido_detalle(pedido_id) |
| PedidoDetalle_precioUnitario_not_null | CHECK |  | petalops.pedido_detalle(precio_unitario) |
| PedidoDetalle_productoID_not_null | CHECK |  | petalops.pedido_detalle(producto_id) |
| PedidoDetalle_subtotal_not_null | CHECK |  | petalops.pedido_detalle(subtotal) |
| PedidoDetalle_sucursalID_not_null | CHECK |  | petalops.pedido_detalle(sucursal_id) |
| fk_detalle_empresa | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| fk_detalle_pedido | FOREIGN KEY | pedido_id | petalops.pedido(id_pedido) |
| fk_detalle_producto | FOREIGN KEY | producto_id | petalops.producto(id_producto) |
| fk_detalle_sucursal | FOREIGN KEY | sucursal_id | petalops.sucursal(id_sucursal) |
| PedidoDetalle_pkey | PRIMARY KEY | id_pedido_detalle | petalops.pedido_detalle(id_pedido_detalle) |
| uq_pedido_producto | UNIQUE | pedido_id | petalops.pedido_detalle(producto_id) |
| uq_pedido_producto | UNIQUE | pedido_id | petalops.pedido_detalle(pedido_id) |
| uq_pedido_producto | UNIQUE | producto_id | petalops.pedido_detalle(pedido_id) |
| uq_pedido_producto | UNIQUE | producto_id | petalops.pedido_detalle(producto_id) |

### Indices

| Nombre | Definicion |
| --- | --- |
| PedidoDetalle_pkey | `CREATE UNIQUE INDEX "PedidoDetalle_pkey" ON petalops.pedido_detalle USING btree (id_pedido_detalle)` |
| fk_detalle_empresa | `CREATE INDEX fk_detalle_empresa ON petalops.pedido_detalle USING btree (empresa_id)` |
| fk_detalle_pedido | `CREATE INDEX fk_detalle_pedido ON petalops.pedido_detalle USING btree (pedido_id)` |
| fk_detalle_producto | `CREATE INDEX fk_detalle_producto ON petalops.pedido_detalle USING btree (producto_id)` |
| fk_detalle_sucursal | `CREATE INDEX fk_detalle_sucursal ON petalops.pedido_detalle USING btree (sucursal_id)` |
| uq_pedido_producto | `CREATE UNIQUE INDEX uq_pedido_producto ON petalops.pedido_detalle USING btree (pedido_id, producto_id)` |

## `pedido_whatsapp_outbox`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id | bigint | No | nextval('pedido_whatsapp_outbox_id_seq'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | pedido_id | bigint | No |  | Pendiente documentar |
| 4 | estado_origen_id | bigint | Si |  | Pendiente documentar |
| 5 | estado_destino_id | bigint | No |  | Pendiente documentar |
| 6 | telefono | character varying(30) | Si |  | Pendiente documentar |
| 7 | nombre_cliente | character varying(200) | Si |  | Pendiente documentar |
| 8 | codigo_pedido | character varying(40) | Si |  | Pendiente documentar |
| 9 | status | character varying(20) | No | 'pending'::character varying | Pendiente documentar |
| 10 | attempts | integer | No | 0 | Pendiente documentar |
| 11 | last_error | text | Si |  | Pendiente documentar |
| 12 | available_at | timestamp without time zone | No | now() | Pendiente documentar |
| 13 | sent_at | timestamp without time zone | Si |  | Pendiente documentar |
| 14 | created_at | timestamp without time zone | No | now() | Pendiente documentar |
| 15 | updated_at | timestamp without time zone | No | now() | Pendiente documentar |
| 16 | empresa_nombre_comercial | character varying(180) | Si |  | Pendiente documentar |
| 17 | order_number | bigint | Si |  | Pendiente documentar |
| 18 | product_summary | text | Si |  | Pendiente documentar |
| 19 | delivery_date | timestamp without time zone | Si |  | Pendiente documentar |
| 20 | delivery_address | text | Si |  | Pendiente documentar |
| 21 | total_neto | numeric(12,2) | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| pedido_whatsapp_outbox_attempts_not_null | CHECK |  | petalops.pedido_whatsapp_outbox(attempts) |
| pedido_whatsapp_outbox_available_at_not_null | CHECK |  | petalops.pedido_whatsapp_outbox(available_at) |
| pedido_whatsapp_outbox_created_at_not_null | CHECK |  | petalops.pedido_whatsapp_outbox(created_at) |
| pedido_whatsapp_outbox_empresa_id_not_null | CHECK |  | petalops.pedido_whatsapp_outbox(empresa_id) |
| pedido_whatsapp_outbox_estado_destino_id_not_null | CHECK |  | petalops.pedido_whatsapp_outbox(estado_destino_id) |
| pedido_whatsapp_outbox_id_not_null | CHECK |  | petalops.pedido_whatsapp_outbox(id) |
| pedido_whatsapp_outbox_pedido_id_not_null | CHECK |  | petalops.pedido_whatsapp_outbox(pedido_id) |
| pedido_whatsapp_outbox_status_not_null | CHECK |  | petalops.pedido_whatsapp_outbox(status) |
| pedido_whatsapp_outbox_updated_at_not_null | CHECK |  | petalops.pedido_whatsapp_outbox(updated_at) |
| pedido_whatsapp_outbox_pkey | PRIMARY KEY | id | petalops.pedido_whatsapp_outbox(id) |
| uq_pedido_whatsapp_outbox_pedido_estado | UNIQUE | pedido_id | petalops.pedido_whatsapp_outbox(pedido_id) |
| uq_pedido_whatsapp_outbox_pedido_estado | UNIQUE | pedido_id | petalops.pedido_whatsapp_outbox(estado_destino_id) |
| uq_pedido_whatsapp_outbox_pedido_estado | UNIQUE | estado_destino_id | petalops.pedido_whatsapp_outbox(pedido_id) |
| uq_pedido_whatsapp_outbox_pedido_estado | UNIQUE | estado_destino_id | petalops.pedido_whatsapp_outbox(estado_destino_id) |

### Indices

| Nombre | Definicion |
| --- | --- |
| ix_pedido_whatsapp_outbox_status_available | `CREATE INDEX ix_pedido_whatsapp_outbox_status_available ON petalops.pedido_whatsapp_outbox USING btree (status, available_at, created_at)` |
| pedido_whatsapp_outbox_pkey | `CREATE UNIQUE INDEX pedido_whatsapp_outbox_pkey ON petalops.pedido_whatsapp_outbox USING btree (id)` |
| uq_pedido_whatsapp_outbox_pedido_estado | `CREATE UNIQUE INDEX uq_pedido_whatsapp_outbox_pedido_estado ON petalops.pedido_whatsapp_outbox USING btree (pedido_id, estado_destino_id)` |

## `perfil_florista`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | empleado_id | bigint | No |  | Pendiente documentar |
| 2 | capacidad_diaria | bigint | No |  | Pendiente documentar |
| 3 | trab_simul_permi | integer | No |  | Pendiente documentar |
| 4 | especialidades | text | Si |  | Pendiente documentar |
| 5 | fecha_ini_incap | timestamp without time zone | Si |  | Pendiente documentar |
| 6 | fecha_fin_incap | timestamp without time zone | Si |  | Pendiente documentar |
| 7 | numero_interno | bigint | Si |  | Pendiente documentar |
| 8 | es_externo | boolean | No | false | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| perfil_florista_capacidad_diaria_not_null | CHECK |  | petalops.perfil_florista(capacidad_diaria) |
| perfil_florista_empleado_id_not_null | CHECK |  | petalops.perfil_florista(empleado_id) |
| perfil_florista_es_externo_not_null | CHECK |  | petalops.perfil_florista(es_externo) |
| perfil_florista_trab_simul_permi_not_null | CHECK |  | petalops.perfil_florista(trab_simul_permi) |
| perfil_florista_empleado_id_fkey | FOREIGN KEY | empleado_id | petalops.empleado(id_empleado) |
| perfil_florista_pkey | PRIMARY KEY | empleado_id | petalops.perfil_florista(empleado_id) |

### Indices

| Nombre | Definicion |
| --- | --- |
| perfil_florista_pkey | `CREATE UNIQUE INDEX perfil_florista_pkey ON petalops.perfil_florista USING btree (empleado_id)` |

## `permiso_modulo`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | rol_id | bigint | No |  | Pendiente documentar |
| 2 | modulo | character varying(80) | No |  | Pendiente documentar |
| 3 | puede_ver | boolean | No |  | Pendiente documentar |
| 4 | puede_crear | boolean | No |  | Pendiente documentar |
| 5 | puede_editar | boolean | No |  | Pendiente documentar |
| 6 | puede_eliminar | boolean | No |  | Pendiente documentar |
| 7 | empresa_id | integer | No |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| PermisoModulo_empresaID_not_null | CHECK |  | petalops.permiso_modulo(empresa_id) |
| PermisoModulo_modulo_not_null | CHECK |  | petalops.permiso_modulo(modulo) |
| PermisoModulo_puedeCrear_not_null | CHECK |  | petalops.permiso_modulo(puede_crear) |
| PermisoModulo_puedeEditar_not_null | CHECK |  | petalops.permiso_modulo(puede_editar) |
| PermisoModulo_puedeEliminar_not_null | CHECK |  | petalops.permiso_modulo(puede_eliminar) |
| PermisoModulo_puedeVer_not_null | CHECK |  | petalops.permiso_modulo(puede_ver) |
| PermisoModulo_rolID_not_null | CHECK |  | petalops.permiso_modulo(rol_id) |
| fk_permiso_modulo_rol | FOREIGN KEY | rol_id | petalops.rol(id_rol) |
| PermisoModulo_pkey | PRIMARY KEY | rol_id | petalops.permiso_modulo(modulo) |
| PermisoModulo_pkey | PRIMARY KEY | rol_id | petalops.permiso_modulo(rol_id) |
| PermisoModulo_pkey | PRIMARY KEY | modulo | petalops.permiso_modulo(modulo) |
| PermisoModulo_pkey | PRIMARY KEY | modulo | petalops.permiso_modulo(rol_id) |
| uq_permiso | UNIQUE | rol_id | petalops.permiso_modulo(modulo) |
| uq_permiso | UNIQUE | rol_id | petalops.permiso_modulo(rol_id) |
| uq_permiso | UNIQUE | modulo | petalops.permiso_modulo(rol_id) |
| uq_permiso | UNIQUE | modulo | petalops.permiso_modulo(modulo) |

### Indices

| Nombre | Definicion |
| --- | --- |
| PermisoModulo_pkey | `CREATE UNIQUE INDEX "PermisoModulo_pkey" ON petalops.permiso_modulo USING btree (rol_id, modulo)` |
| idx_permiso_modulo | `CREATE INDEX idx_permiso_modulo ON petalops.permiso_modulo USING btree (modulo)` |
| uq_permiso | `CREATE UNIQUE INDEX uq_permiso ON petalops.permiso_modulo USING btree (rol_id, modulo)` |

## `plan`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_plan | bigint | No |  | Pendiente documentar |
| 2 | nombre | character varying(100) | No |  | Pendiente documentar |
| 3 | descripcion | character varying(255) | Si |  | Pendiente documentar |
| 4 | empresa_id | bigint | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| Plan_idPlan_not_null | CHECK |  | petalops.plan(id_plan) |
| Plan_nombre_not_null | CHECK |  | petalops.plan(nombre) |
| fk_plan_empresa | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| Plan_pkey | PRIMARY KEY | id_plan | petalops.plan(id_plan) |

### Indices

| Nombre | Definicion |
| --- | --- |
| Plan_pkey | `CREATE UNIQUE INDEX "Plan_pkey" ON petalops.plan USING btree (id_plan)` |
| idx_plan_empresaid | `CREATE INDEX idx_plan_empresaid ON petalops.plan USING btree (empresa_id)` |

## `plan_modulo`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | plan_id | bigint | No |  | Pendiente documentar |
| 2 | modulo | character varying(80) | No |  | Pendiente documentar |
| 3 | activo | boolean | No |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| PlanModulo_activo_not_null | CHECK |  | petalops.plan_modulo(activo) |
| PlanModulo_modulo_not_null | CHECK |  | petalops.plan_modulo(modulo) |
| PlanModulo_planID_not_null | CHECK |  | petalops.plan_modulo(plan_id) |
| fk_plan_modulo_plan | FOREIGN KEY | plan_id | petalops.plan(id_plan) |
| PlanModulo_pkey | PRIMARY KEY | plan_id | petalops.plan_modulo(modulo) |
| PlanModulo_pkey | PRIMARY KEY | plan_id | petalops.plan_modulo(plan_id) |
| PlanModulo_pkey | PRIMARY KEY | modulo | petalops.plan_modulo(modulo) |
| PlanModulo_pkey | PRIMARY KEY | modulo | petalops.plan_modulo(plan_id) |
| uq_plan_modulo | UNIQUE | plan_id | petalops.plan_modulo(modulo) |
| uq_plan_modulo | UNIQUE | plan_id | petalops.plan_modulo(plan_id) |
| uq_plan_modulo | UNIQUE | modulo | petalops.plan_modulo(plan_id) |
| uq_plan_modulo | UNIQUE | modulo | petalops.plan_modulo(modulo) |

### Indices

| Nombre | Definicion |
| --- | --- |
| PlanModulo_pkey | `CREATE UNIQUE INDEX "PlanModulo_pkey" ON petalops.plan_modulo USING btree (plan_id, modulo)` |
| uq_plan_modulo | `CREATE UNIQUE INDEX uq_plan_modulo ON petalops.plan_modulo USING btree (plan_id, modulo)` |

## `produccion`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_produccion | integer | No | nextval('produccion_id_seq'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | sucursal_id | bigint | No |  | Pendiente documentar |
| 4 | pedido_id | bigint | Si |  | Pendiente documentar |
| 6 | fecha_programada_produccion | date | Si |  | Pendiente documentar |
| 7 | fecha_asignacion | timestamp without time zone | Si |  | Pendiente documentar |
| 8 | pedido_detalle_id | bigint | Si |  | Pendiente documentar |
| 9 | empleado_id | bigint | Si |  | Pendiente documentar |
| 10 | estado_produccion_id | bigint | Si |  | Pendiente documentar |
| 11 | fecha_inicio | timestamp without time zone | Si |  | Pendiente documentar |
| 12 | fecha_finalizacion | timestamp without time zone | Si |  | Pendiente documentar |
| 13 | tiempoestimadomin | integer | Si |  | Pendiente documentar |
| 14 | tiempo_real_min | integer | Si |  | Pendiente documentar |
| 16 | prioridad | character varying(20) | Si |  | Pendiente documentar |
| 17 | observacionesinternas | text | Si |  | Pendiente documentar |
| 18 | orden_produccion | bigint | Si |  | Pendiente documentar |
| 19 | fecha_fin | timestamp without time zone | Si |  | Pendiente documentar |
| 20 | created_at | timestamp without time zone | No |  | Pendiente documentar |
| 21 | updated_at | timestamp without time zone | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| Produccion_createdAt_not_null | CHECK |  | petalops.produccion(created_at) |
| Produccion_empresaID_not_null | CHECK |  | petalops.produccion(empresa_id) |
| Produccion_idProduccion_not_null | CHECK |  | petalops.produccion(id_produccion) |
| Produccion_sucursalID_not_null | CHECK |  | petalops.produccion(sucursal_id) |
| fk_produccion_detalle | FOREIGN KEY | pedido_detalle_id | petalops.pedido_detalle(id_pedido_detalle) |
| fk_produccion_empleado | FOREIGN KEY | empleado_id | petalops.empleado(id_empleado) |
| fk_produccion_empresa | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| fk_produccion_estado | FOREIGN KEY | estado_produccion_id | petalops.estado_produccion(id_estado_produccion) |
| fk_produccion_pedido | FOREIGN KEY | pedido_id | petalops.pedido(id_pedido) |
| fk_produccion_sucursal | FOREIGN KEY | sucursal_id | petalops.sucursal(id_sucursal) |
| Produccion_pkey | PRIMARY KEY | id_produccion | petalops.produccion(id_produccion) |

### Indices

| Nombre | Definicion |
| --- | --- |
| Produccion_pkey | `CREATE UNIQUE INDEX "Produccion_pkey" ON petalops.produccion USING btree (id_produccion)` |
| fk_produccion_detalle | `CREATE INDEX fk_produccion_detalle ON petalops.produccion USING btree (pedido_detalle_id)` |
| fk_produccion_empleado | `CREATE INDEX fk_produccion_empleado ON petalops.produccion USING btree (empleado_id)` |
| fk_produccion_sucursal | `CREATE INDEX fk_produccion_sucursal ON petalops.produccion USING btree (sucursal_id)` |

## `produccion_historial`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_produccion_historial | integer | No | nextval('produccion_historial_id_seq'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | sucursal_id | bigint | No |  | Pendiente documentar |
| 4 | produccion_id | bigint | No |  | Pendiente documentar |
| 5 | florista_anterior_id | bigint | Si |  | Pendiente documentar |
| 6 | florista_nuevo_id | bigint | Si |  | Pendiente documentar |
| 7 | fecha_cambio | timestamp without time zone | No |  | Pendiente documentar |
| 8 | motivo | text | No |  | Pendiente documentar |
| 9 | usuariocambio | character varying(120) | No |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| ProduccionHistorial_empresaID_not_null | CHECK |  | petalops.produccion_historial(empresa_id) |
| ProduccionHistorial_fechaCambio_not_null | CHECK |  | petalops.produccion_historial(fecha_cambio) |
| ProduccionHistorial_idProduccionHistorial_not_null | CHECK |  | petalops.produccion_historial(id_produccion_historial) |
| ProduccionHistorial_motivo_not_null | CHECK |  | petalops.produccion_historial(motivo) |
| ProduccionHistorial_produccionID_not_null | CHECK |  | petalops.produccion_historial(produccion_id) |
| ProduccionHistorial_sucursalID_not_null | CHECK |  | petalops.produccion_historial(sucursal_id) |
| ProduccionHistorial_usuarioCambio_not_null | CHECK |  | petalops.produccion_historial(usuariocambio) |
| fk_produccion_historial_empresa | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| fk_produccion_historial_florista_anterior | FOREIGN KEY | florista_anterior_id | petalops.empleado(id_empleado) |
| fk_produccion_historial_florista_nuevo | FOREIGN KEY | florista_nuevo_id | petalops.empleado(id_empleado) |
| fk_produccion_historial_sucursal | FOREIGN KEY | sucursal_id | petalops.sucursal(id_sucursal) |
| ProduccionHistorial_pkey | PRIMARY KEY | id_produccion_historial | petalops.produccion_historial(id_produccion_historial) |

### Indices

| Nombre | Definicion |
| --- | --- |
| ProduccionHistorial_pkey | `CREATE UNIQUE INDEX "ProduccionHistorial_pkey" ON petalops.produccion_historial USING btree (id_produccion_historial)` |
| idx_historial_empresa_sucursal_fecha | `CREATE INDEX idx_historial_empresa_sucursal_fecha ON petalops.produccion_historial USING btree (empresa_id, sucursal_id, fecha_cambio)` |
| idx_historial_produccion_fecha | `CREATE INDEX idx_historial_produccion_fecha ON petalops.produccion_historial USING btree (produccion_id, fecha_cambio)` |

## `producto`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_producto | integer | No |  | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | categoria_id | bigint | No |  | Pendiente documentar |
| 4 | codigo_producto | character varying(50) | No |  | Pendiente documentar |
| 5 | nombre_producto | character varying(150) | No |  | Pendiente documentar |
| 6 | descripcion | text | Si |  | Pendiente documentar |
| 7 | porcentaje_iva | numeric(5,2) | Si |  | Pendiente documentar |
| 8 | iva_incluido | boolean | Si | false | Pendiente documentar |
| 9 | tiempo_base_min | integer | Si |  | Pendiente documentar |
| 10 | nivel_complejidad | character varying(50) | Si |  | Pendiente documentar |
| 11 | activo | boolean | No | true | Pendiente documentar |
| 12 | created_at | timestamp without time zone | No | CURRENT_TIMESTAMP | Pendiente documentar |
| 13 | updated_at | timestamp without time zone | Si |  | Pendiente documentar |
| 14 | codigo_catalogo | character varying(100) | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| producto_activo_not_null | CHECK |  | petalops.producto(activo) |
| producto_categoria_id_not_null | CHECK |  | petalops.producto(categoria_id) |
| producto_codigo_producto_not_null | CHECK |  | petalops.producto(codigo_producto) |
| producto_created_at_not_null | CHECK |  | petalops.producto(created_at) |
| producto_empresa_id_not_null | CHECK |  | petalops.producto(empresa_id) |
| producto_id_producto_not_null | CHECK |  | petalops.producto(id_producto) |
| producto_nombre_producto_not_null | CHECK |  | petalops.producto(nombre_producto) |
| fk_producto_categoria | FOREIGN KEY | categoria_id | petalops.categoria(id_categoria) |
| fk_producto_empresa | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| producto_pkey | PRIMARY KEY | id_producto | petalops.producto(id_producto) |
| uq_producto_codigo_empresa | UNIQUE | empresa_id | petalops.producto(empresa_id) |
| uq_producto_codigo_empresa | UNIQUE | empresa_id | petalops.producto(codigo_producto) |
| uq_producto_codigo_empresa | UNIQUE | codigo_producto | petalops.producto(empresa_id) |
| uq_producto_codigo_empresa | UNIQUE | codigo_producto | petalops.producto(codigo_producto) |

### Indices

| Nombre | Definicion |
| --- | --- |
| idx_producto_codigo_catalogo | `CREATE INDEX idx_producto_codigo_catalogo ON petalops.producto USING btree (codigo_catalogo)` |
| producto_pkey | `CREATE UNIQUE INDEX producto_pkey ON petalops.producto USING btree (id_producto)` |
| uq_producto_codigo_empresa | `CREATE UNIQUE INDEX uq_producto_codigo_empresa ON petalops.producto USING btree (empresa_id, codigo_producto)` |

## `producto_sucursal`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_producto_sucursal | integer | No |  | Pendiente documentar |
| 2 | producto_id | integer | No |  | Pendiente documentar |
| 3 | sucursal_id | bigint | No |  | Pendiente documentar |
| 4 | precio | numeric(10,2) | No |  | Pendiente documentar |
| 5 | activo | boolean | No | true | Pendiente documentar |
| 6 | es_destacado | boolean | Si | false | Pendiente documentar |
| 7 | orden_catalogo | integer | Si |  | Pendiente documentar |
| 8 | imagen_url | character varying(500) | Si |  | Pendiente documentar |
| 9 | imagen_s3_key | character varying(255) | Si |  | Pendiente documentar |
| 10 | created_at | timestamp without time zone | No | CURRENT_TIMESTAMP | Pendiente documentar |
| 11 | updated_at | timestamp without time zone | Si |  | Pendiente documentar |
| 12 | imagen_sm_key | character varying(255) | Si |  | Pendiente documentar |
| 13 | imagen_md_key | character varying(255) | Si |  | Pendiente documentar |
| 14 | imagen_lg_key | character varying(255) | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| producto_sucursal_activo_not_null | CHECK |  | petalops.producto_sucursal(activo) |
| producto_sucursal_created_at_not_null | CHECK |  | petalops.producto_sucursal(created_at) |
| producto_sucursal_id_producto_sucursal_not_null | CHECK |  | petalops.producto_sucursal(id_producto_sucursal) |
| producto_sucursal_precio_not_null | CHECK |  | petalops.producto_sucursal(precio) |
| producto_sucursal_producto_id_not_null | CHECK |  | petalops.producto_sucursal(producto_id) |
| producto_sucursal_sucursal_id_not_null | CHECK |  | petalops.producto_sucursal(sucursal_id) |
| fk_ps_producto | FOREIGN KEY | producto_id | petalops.producto(id_producto) |
| fk_ps_sucursal | FOREIGN KEY | sucursal_id | petalops.sucursal(id_sucursal) |
| producto_sucursal_pkey | PRIMARY KEY | id_producto_sucursal | petalops.producto_sucursal(id_producto_sucursal) |
| uq_producto_sucursal | UNIQUE | producto_id | petalops.producto_sucursal(producto_id) |
| uq_producto_sucursal | UNIQUE | producto_id | petalops.producto_sucursal(sucursal_id) |
| uq_producto_sucursal | UNIQUE | sucursal_id | petalops.producto_sucursal(producto_id) |
| uq_producto_sucursal | UNIQUE | sucursal_id | petalops.producto_sucursal(sucursal_id) |

### Indices

| Nombre | Definicion |
| --- | --- |
| producto_sucursal_pkey | `CREATE UNIQUE INDEX producto_sucursal_pkey ON petalops.producto_sucursal USING btree (id_producto_sucursal)` |
| uq_producto_sucursal | `CREATE UNIQUE INDEX uq_producto_sucursal ON petalops.producto_sucursal USING btree (producto_id, sucursal_id)` |

## `proveedor`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_proveedor | integer | No | nextval('"Proveedor_idProveedor_seq"'::regclass) | Pendiente documentar |
| 3 | nombre_proveedor | character varying(150) | No |  | Pendiente documentar |
| 4 | codigo_proveedor | character varying(80) | Si |  | Pendiente documentar |
| 5 | activo | integer | No |  | Pendiente documentar |
| 6 | created_at | timestamp without time zone | Si |  | Pendiente documentar |
| 7 | updated_at | timestamp without time zone | Si |  | Pendiente documentar |
| 8 | empresa_id | bigint | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| Proveedor_activo_not_null | CHECK |  | petalops.proveedor(activo) |
| Proveedor_idProveedor_not_null | CHECK |  | petalops.proveedor(id_proveedor) |
| Proveedor_nombreProveedor_not_null | CHECK |  | petalops.proveedor(nombre_proveedor) |
| proveedor_empresa_id_fkey | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| Proveedor_pkey | PRIMARY KEY | id_proveedor | petalops.proveedor(id_proveedor) |

### Indices

| Nombre | Definicion |
| --- | --- |
| Proveedor_pkey | `CREATE UNIQUE INDEX "Proveedor_pkey" ON petalops.proveedor USING btree (id_proveedor)` |

## `receta`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_receta | bigint | No |  | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | nombre | character varying(200) | No |  | Pendiente documentar |
| 4 | descripcion | text | Si |  | Pendiente documentar |
| 5 | activo | boolean | No | true | Pendiente documentar |
| 6 | created_at | timestamp without time zone | No | now() | Pendiente documentar |
| 7 | updated_at | timestamp without time zone | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| receta_activo_not_null | CHECK |  | petalops.receta(activo) |
| receta_created_at_not_null | CHECK |  | petalops.receta(created_at) |
| receta_empresa_id_not_null | CHECK |  | petalops.receta(empresa_id) |
| receta_id_receta_not_null | CHECK |  | petalops.receta(id_receta) |
| receta_nombre_not_null | CHECK |  | petalops.receta(nombre) |
| fk_receta_empresa | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| receta_pkey | PRIMARY KEY | id_receta | petalops.receta(id_receta) |
| uq_receta_empresa_nombre | UNIQUE | empresa_id | petalops.receta(empresa_id) |
| uq_receta_empresa_nombre | UNIQUE | empresa_id | petalops.receta(nombre) |
| uq_receta_empresa_nombre | UNIQUE | nombre | petalops.receta(nombre) |
| uq_receta_empresa_nombre | UNIQUE | nombre | petalops.receta(empresa_id) |

### Indices

| Nombre | Definicion |
| --- | --- |
| idx_receta_empresa | `CREATE INDEX idx_receta_empresa ON petalops.receta USING btree (empresa_id, activo)` |
| receta_pkey | `CREATE UNIQUE INDEX receta_pkey ON petalops.receta USING btree (id_receta)` |
| uq_receta_empresa_nombre | `CREATE UNIQUE INDEX uq_receta_empresa_nombre ON petalops.receta USING btree (empresa_id, nombre)` |

## `receta_detalle`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_receta_detalle | bigint | No |  | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | receta_id | bigint | No |  | Pendiente documentar |
| 4 | inventario_id | bigint | No |  | Pendiente documentar |
| 5 | cantidad | numeric(12,4) | No | 1 | Pendiente documentar |
| 6 | created_at | timestamp without time zone | No | now() | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| receta_detalle_cantidad_not_null | CHECK |  | petalops.receta_detalle(cantidad) |
| receta_detalle_created_at_not_null | CHECK |  | petalops.receta_detalle(created_at) |
| receta_detalle_empresa_id_not_null | CHECK |  | petalops.receta_detalle(empresa_id) |
| receta_detalle_id_receta_detalle_not_null | CHECK |  | petalops.receta_detalle(id_receta_detalle) |
| receta_detalle_inventario_id_not_null | CHECK |  | petalops.receta_detalle(inventario_id) |
| receta_detalle_receta_id_not_null | CHECK |  | petalops.receta_detalle(receta_id) |
| fk_receta_detalle_empresa | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| fk_receta_detalle_inventario | FOREIGN KEY | inventario_id | petalops.inventario(id_inventario) |
| fk_receta_detalle_receta | FOREIGN KEY | receta_id | petalops.receta(id_receta) |
| receta_detalle_pkey | PRIMARY KEY | id_receta_detalle | petalops.receta_detalle(id_receta_detalle) |
| uq_receta_detalle_receta_inv | UNIQUE | receta_id | petalops.receta_detalle(receta_id) |
| uq_receta_detalle_receta_inv | UNIQUE | receta_id | petalops.receta_detalle(inventario_id) |
| uq_receta_detalle_receta_inv | UNIQUE | inventario_id | petalops.receta_detalle(receta_id) |
| uq_receta_detalle_receta_inv | UNIQUE | inventario_id | petalops.receta_detalle(inventario_id) |

### Indices

| Nombre | Definicion |
| --- | --- |
| idx_receta_detalle_empresa | `CREATE INDEX idx_receta_detalle_empresa ON petalops.receta_detalle USING btree (empresa_id)` |
| idx_receta_detalle_receta | `CREATE INDEX idx_receta_detalle_receta ON petalops.receta_detalle USING btree (receta_id)` |
| receta_detalle_pkey | `CREATE UNIQUE INDEX receta_detalle_pkey ON petalops.receta_detalle USING btree (id_receta_detalle)` |
| uq_receta_detalle_receta_inv | `CREATE UNIQUE INDEX uq_receta_detalle_receta_inv ON petalops.receta_detalle USING btree (receta_id, inventario_id)` |

## `rol`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_rol | integer | No | nextval('"Rol_idRol_seq"'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | nombre_rol | character varying(80) | No |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| Rol_empresaID_not_null | CHECK |  | petalops.rol(empresa_id) |
| Rol_idRol_not_null | CHECK |  | petalops.rol(id_rol) |
| Rol_nombreRol_not_null | CHECK |  | petalops.rol(nombre_rol) |
| fk_rol_empresa | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| Rol_pkey | PRIMARY KEY | id_rol | petalops.rol(id_rol) |

### Indices

| Nombre | Definicion |
| --- | --- |
| Rol_pkey | `CREATE UNIQUE INDEX "Rol_pkey" ON petalops.rol USING btree (id_rol)` |
| idx_rol_empresa | `CREATE INDEX idx_rol_empresa ON petalops.rol USING btree (empresa_id)` |
| uq_rol_empresa_nombre | `CREATE UNIQUE INDEX uq_rol_empresa_nombre ON petalops.rol USING btree (empresa_id, nombre_rol)` |

## `sucursal`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_sucursal | integer | No | nextval('"Sucursal_idSucursal_seq"'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | nombre_sucursal | character varying(120) | No |  | Pendiente documentar |
| 4 | direccion | character varying(200) | Si |  | Pendiente documentar |
| 5 | telefono | character varying(30) | Si |  | Pendiente documentar |
| 6 | estado | character varying(30) | No |  | Pendiente documentar |
| 7 | created_at | timestamp without time zone | No |  | Pendiente documentar |
| 8 | updated_at | timestamp without time zone | Si |  | Pendiente documentar |
| 9 | prefijo_pedido | character varying(12) | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| Sucursal_createdAt_not_null | CHECK |  | petalops.sucursal(created_at) |
| Sucursal_empresaID_not_null | CHECK |  | petalops.sucursal(empresa_id) |
| Sucursal_estado_not_null | CHECK |  | petalops.sucursal(estado) |
| Sucursal_idSucursal_not_null | CHECK |  | petalops.sucursal(id_sucursal) |
| Sucursal_nombreSucursal_not_null | CHECK |  | petalops.sucursal(nombre_sucursal) |
| fk_sucursal_empresa | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| Sucursal_pkey | PRIMARY KEY | id_sucursal | petalops.sucursal(id_sucursal) |

### Indices

| Nombre | Definicion |
| --- | --- |
| Sucursal_pkey | `CREATE UNIQUE INDEX "Sucursal_pkey" ON petalops.sucursal USING btree (id_sucursal)` |
| uk_sucursal_empresa_nombre | `CREATE UNIQUE INDEX uk_sucursal_empresa_nombre ON petalops.sucursal USING btree (empresa_id, nombre_sucursal)` |

## `sucursal_contador_pedido`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | empresa_id | bigint | No |  | Pendiente documentar |
| 2 | sucursal_id | bigint | No |  | Pendiente documentar |
| 3 | ultimo_pedido | bigint | No |  | Pendiente documentar |
| 4 | updated_at | timestamp without time zone | Si |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| SucursalContadorPedido_empresaID_not_null | CHECK |  | petalops.sucursal_contador_pedido(empresa_id) |
| SucursalContadorPedido_sucursalID_not_null | CHECK |  | petalops.sucursal_contador_pedido(sucursal_id) |
| SucursalContadorPedido_ultimoPedido_not_null | CHECK |  | petalops.sucursal_contador_pedido(ultimo_pedido) |
| fk_scp_empresa | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| fk_scp_sucursal | FOREIGN KEY | sucursal_id | petalops.sucursal(id_sucursal) |
| SucursalContadorPedido_pkey | PRIMARY KEY | empresa_id | petalops.sucursal_contador_pedido(sucursal_id) |
| SucursalContadorPedido_pkey | PRIMARY KEY | empresa_id | petalops.sucursal_contador_pedido(empresa_id) |
| SucursalContadorPedido_pkey | PRIMARY KEY | sucursal_id | petalops.sucursal_contador_pedido(sucursal_id) |
| SucursalContadorPedido_pkey | PRIMARY KEY | sucursal_id | petalops.sucursal_contador_pedido(empresa_id) |

### Indices

| Nombre | Definicion |
| --- | --- |
| SucursalContadorPedido_pkey | `CREATE UNIQUE INDEX "SucursalContadorPedido_pkey" ON petalops.sucursal_contador_pedido USING btree (empresa_id, sucursal_id)` |
| fk_scp_sucursal | `CREATE INDEX fk_scp_sucursal ON petalops.sucursal_contador_pedido USING btree (sucursal_id)` |

## `tipo_movimiento`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_tipo_movimiento | integer | No | nextval('tipo_movimiento_id_tipo_movimiento_seq'::regclass) | Pendiente documentar |
| 2 | codigo | character varying(20) | Si |  | Pendiente documentar |
| 3 | nombre | character varying(50) | Si |  | Pendiente documentar |
| 4 | afecta_stock | boolean | No |  | Pendiente documentar |
| 5 | signo | smallint | No |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| tipo_movimiento_afecta_stock_not_null | CHECK |  | petalops.tipo_movimiento(afecta_stock) |
| tipo_movimiento_id_tipo_movimiento_not_null | CHECK |  | petalops.tipo_movimiento(id_tipo_movimiento) |
| tipo_movimiento_signo_not_null | CHECK |  | petalops.tipo_movimiento(signo) |
| tipo_movimiento_pkey | PRIMARY KEY | id_tipo_movimiento | petalops.tipo_movimiento(id_tipo_movimiento) |
| tipo_movimiento_codigo_key | UNIQUE | codigo | petalops.tipo_movimiento(codigo) |

### Indices

| Nombre | Definicion |
| --- | --- |
| tipo_movimiento_codigo_key | `CREATE UNIQUE INDEX tipo_movimiento_codigo_key ON petalops.tipo_movimiento USING btree (codigo)` |
| tipo_movimiento_pkey | `CREATE UNIQUE INDEX tipo_movimiento_pkey ON petalops.tipo_movimiento USING btree (id_tipo_movimiento)` |

## `transicion_estado_entrega`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_tran_estado_ent | integer | No | nextval('"TransicionEstadoEntrega_idTransicionEstadoEntrega_seq"'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | estado_origen_id | bigint | No |  | Pendiente documentar |
| 4 | estado_destino_id | bigint | No |  | Pendiente documentar |
| 5 | created_at | timestamp without time zone | No |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| TransicionEstadoEntrega_createdAt_not_null | CHECK |  | petalops.transicion_estado_entrega(created_at) |
| TransicionEstadoEntrega_empresaID_not_null | CHECK |  | petalops.transicion_estado_entrega(empresa_id) |
| TransicionEstadoEntrega_estadoDestinoID_not_null | CHECK |  | petalops.transicion_estado_entrega(estado_destino_id) |
| TransicionEstadoEntrega_estadoOrigenID_not_null | CHECK |  | petalops.transicion_estado_entrega(estado_origen_id) |
| TransicionEstadoEntrega_idTransicionEstadoEntrega_not_null | CHECK |  | petalops.transicion_estado_entrega(id_tran_estado_ent) |
| fk_trans_entrega_empresa | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| TransicionEstadoEntrega_pkey | PRIMARY KEY | id_tran_estado_ent | petalops.transicion_estado_entrega(id_tran_estado_ent) |

### Indices

| Nombre | Definicion |
| --- | --- |
| TransicionEstadoEntrega_pkey | `CREATE UNIQUE INDEX "TransicionEstadoEntrega_pkey" ON petalops.transicion_estado_entrega USING btree (id_tran_estado_ent)` |
| uk_trans_entrega | `CREATE UNIQUE INDEX uk_trans_entrega ON petalops.transicion_estado_entrega USING btree (empresa_id, estado_origen_id, estado_destino_id)` |

## `transicion_estado_pedido`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_trans_estado_ped | integer | No | nextval('"TransicionEstadoPedido_idTransicionEstadoPedido_seq"'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | estado_origen_id | bigint | No |  | Pendiente documentar |
| 4 | estado_destino_id | bigint | No |  | Pendiente documentar |
| 5 | created_at | timestamp without time zone | No |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| TransicionEstadoPedido_createdAt_not_null | CHECK |  | petalops.transicion_estado_pedido(created_at) |
| TransicionEstadoPedido_empresaID_not_null | CHECK |  | petalops.transicion_estado_pedido(empresa_id) |
| TransicionEstadoPedido_estadoDestinoID_not_null | CHECK |  | petalops.transicion_estado_pedido(estado_destino_id) |
| TransicionEstadoPedido_estadoOrigenID_not_null | CHECK |  | petalops.transicion_estado_pedido(estado_origen_id) |
| TransicionEstadoPedido_idTransicionEstadoPedido_not_null | CHECK |  | petalops.transicion_estado_pedido(id_trans_estado_ped) |
| fk_trans_pedido_empresa | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| TransicionEstadoPedido_pkey | PRIMARY KEY | id_trans_estado_ped | petalops.transicion_estado_pedido(id_trans_estado_ped) |

### Indices

| Nombre | Definicion |
| --- | --- |
| TransicionEstadoPedido_pkey | `CREATE UNIQUE INDEX "TransicionEstadoPedido_pkey" ON petalops.transicion_estado_pedido USING btree (id_trans_estado_ped)` |
| uk_trans_pedido | `CREATE UNIQUE INDEX uk_trans_pedido ON petalops.transicion_estado_pedido USING btree (empresa_id, estado_origen_id, estado_destino_id)` |

## `transicion_estado_produccion`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_trans_estado_prod | integer | No | nextval('"TransicionEstadoProduccion_idTransicionEstadoProduccion_seq"'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | estado_origen_id | bigint | No |  | Pendiente documentar |
| 4 | estado_destino_id | bigint | No |  | Pendiente documentar |
| 5 | created_at | timestamp without time zone | No |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| TransicionEstadoProduccion_createdAt_not_null | CHECK |  | petalops.transicion_estado_produccion(created_at) |
| TransicionEstadoProduccion_empresaID_not_null | CHECK |  | petalops.transicion_estado_produccion(empresa_id) |
| TransicionEstadoProduccion_estadoDestinoID_not_null | CHECK |  | petalops.transicion_estado_produccion(estado_destino_id) |
| TransicionEstadoProduccion_estadoOrigenID_not_null | CHECK |  | petalops.transicion_estado_produccion(estado_origen_id) |
| TransicionEstadoProduccion_idTransicionEstadoProduccio_not_null | CHECK |  | petalops.transicion_estado_produccion(id_trans_estado_prod) |
| fk_trans_produccion_empresa | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| TransicionEstadoProduccion_pkey | PRIMARY KEY | id_trans_estado_prod | petalops.transicion_estado_produccion(id_trans_estado_prod) |

### Indices

| Nombre | Definicion |
| --- | --- |
| TransicionEstadoProduccion_pkey | `CREATE UNIQUE INDEX "TransicionEstadoProduccion_pkey" ON petalops.transicion_estado_produccion USING btree (id_trans_estado_prod)` |
| uk_trans_produccion | `CREATE UNIQUE INDEX uk_trans_produccion ON petalops.transicion_estado_produccion USING btree (empresa_id, estado_origen_id, estado_destino_id)` |

## `usuario`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_usuario | integer | No | nextval('"Usuario_idUsuario_seq"'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | Si |  | Pendiente documentar |
| 3 | nombre | character varying(150) | No |  | Pendiente documentar |
| 4 | email | character varying(180) | No |  | Pendiente documentar |
| 5 | passwordhash | character varying(255) | No |  | Pendiente documentar |
| 6 | rolid | bigint | Si |  | Pendiente documentar |
| 7 | estado | character varying(20) | No |  | Pendiente documentar |
| 8 | ultimo_login | timestamp without time zone | Si |  | Pendiente documentar |
| 9 | created_at | timestamp without time zone | Si |  | Pendiente documentar |
| 10 | updated_at | timestamp without time zone | Si |  | Pendiente documentar |
| 11 | login | character varying(80) | No |  | Pendiente documentar |
| 12 | sucursal_id | bigint | Si |  | Pendiente documentar |
| 13 | es_superadmin | boolean | No | false | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| Usuario_email_not_null | CHECK |  | petalops.usuario(email) |
| Usuario_estado_not_null | CHECK |  | petalops.usuario(estado) |
| Usuario_idUsuario_not_null | CHECK |  | petalops.usuario(id_usuario) |
| Usuario_login_not_null | CHECK |  | petalops.usuario(login) |
| Usuario_nombre_not_null | CHECK |  | petalops.usuario(nombre) |
| Usuario_passwordHash_not_null | CHECK |  | petalops.usuario(passwordhash) |
| chk_usuario_empresa_o_superadmin | CHECK |  | petalops.usuario(empresa_id) |
| chk_usuario_empresa_o_superadmin | CHECK |  | petalops.usuario(rolid) |
| chk_usuario_empresa_o_superadmin | CHECK |  | petalops.usuario(sucursal_id) |
| chk_usuario_empresa_o_superadmin | CHECK |  | petalops.usuario(es_superadmin) |
| chk_usuario_rol_superadmin | CHECK |  | petalops.usuario(es_superadmin) |
| chk_usuario_rol_superadmin | CHECK |  | petalops.usuario(rolid) |
| usuario_es_superadmin_not_null | CHECK |  | petalops.usuario(es_superadmin) |
| fk_usuario_empresa | FOREIGN KEY | empresa_id | petalops.empresa(id_empresa) |
| fk_usuario_rol | FOREIGN KEY | rolid | petalops.rol(id_rol) |
| Usuario_pkey | PRIMARY KEY | id_usuario | petalops.usuario(id_usuario) |

### Indices

| Nombre | Definicion |
| --- | --- |
| Usuario_pkey | `CREATE UNIQUE INDEX "Usuario_pkey" ON petalops.usuario USING btree (id_usuario)` |
| idx_usuario_empresa_estado | `CREATE INDEX idx_usuario_empresa_estado ON petalops.usuario USING btree (empresa_id, estado)` |
| idx_usuario_empresa_sucursal_estado | `CREATE INDEX idx_usuario_empresa_sucursal_estado ON petalops.usuario USING btree (empresa_id, sucursal_id, estado)` |
| idx_usuario_rol | `CREATE INDEX idx_usuario_rol ON petalops.usuario USING btree (rolid)` |
| idx_usuario_superadmin | `CREATE INDEX idx_usuario_superadmin ON petalops.usuario USING btree (es_superadmin) WHERE (es_superadmin = true)` |
| uq_usuario_login | `CREATE UNIQUE INDEX uq_usuario_login ON petalops.usuario USING btree (login)` |

## `usuario_auditoria`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | id_audit | integer | No | nextval('"UsuarioAuditoria_idAudit_seq"'::regclass) | Pendiente documentar |
| 2 | empresa_id | bigint | No |  | Pendiente documentar |
| 3 | actor_user_id | bigint | No |  | Pendiente documentar |
| 4 | actor_login | character varying(80) | No |  | Pendiente documentar |
| 5 | accion | character varying(60) | No |  | Pendiente documentar |
| 6 | target_user_id | bigint | No |  | Pendiente documentar |
| 7 | target_login | character varying(80) | No |  | Pendiente documentar |
| 8 | detalle_json | text | Si |  | Pendiente documentar |
| 9 | created_at | timestamp without time zone | No |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| UsuarioAuditoria_accion_not_null | CHECK |  | petalops.usuario_auditoria(accion) |
| UsuarioAuditoria_actorLogin_not_null | CHECK |  | petalops.usuario_auditoria(actor_login) |
| UsuarioAuditoria_actorUserID_not_null | CHECK |  | petalops.usuario_auditoria(actor_user_id) |
| UsuarioAuditoria_createdAt_not_null | CHECK |  | petalops.usuario_auditoria(created_at) |
| UsuarioAuditoria_empresaID_not_null | CHECK |  | petalops.usuario_auditoria(empresa_id) |
| UsuarioAuditoria_idAudit_not_null | CHECK |  | petalops.usuario_auditoria(id_audit) |
| UsuarioAuditoria_targetLogin_not_null | CHECK |  | petalops.usuario_auditoria(target_login) |
| UsuarioAuditoria_targetUserID_not_null | CHECK |  | petalops.usuario_auditoria(target_user_id) |
| UsuarioAuditoria_pkey | PRIMARY KEY | id_audit | petalops.usuario_auditoria(id_audit) |

### Indices

| Nombre | Definicion |
| --- | --- |
| UsuarioAuditoria_pkey | `CREATE UNIQUE INDEX "UsuarioAuditoria_pkey" ON petalops.usuario_auditoria USING btree (id_audit)` |
| idx_audit_empresa_fecha | `CREATE INDEX idx_audit_empresa_fecha ON petalops.usuario_auditoria USING btree (empresa_id, created_at)` |
| idx_audit_target_fecha | `CREATE INDEX idx_audit_target_fecha ON petalops.usuario_auditoria USING btree (target_user_id, created_at)` |

## `usuario_modulo`

**Tipo:** BASE TABLE

**Descripcion:** Pendiente documentar

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | usuario_id | bigint | No |  | Pendiente documentar |
| 2 | modulo | character varying(80) | No |  | Pendiente documentar |
| 3 | activo | boolean | No |  | Pendiente documentar |
| 4 | updated_at | timestamp without time zone | No |  | Pendiente documentar |

### Restricciones

| Nombre | Tipo | Columna | Referencia |
| --- | --- | --- | --- |
| UsuarioModulo_activo_not_null | CHECK |  | petalops.usuario_modulo(activo) |
| UsuarioModulo_modulo_not_null | CHECK |  | petalops.usuario_modulo(modulo) |
| UsuarioModulo_updatedAt_not_null | CHECK |  | petalops.usuario_modulo(updated_at) |
| UsuarioModulo_userID_not_null | CHECK |  | petalops.usuario_modulo(usuario_id) |
| fk_usuario_modulo_usuario | FOREIGN KEY | usuario_id | petalops.usuario(id_usuario) |
| pk_usuario_modulo | PRIMARY KEY | usuario_id | petalops.usuario_modulo(modulo) |
| pk_usuario_modulo | PRIMARY KEY | usuario_id | petalops.usuario_modulo(usuario_id) |
| pk_usuario_modulo | PRIMARY KEY | modulo | petalops.usuario_modulo(usuario_id) |
| pk_usuario_modulo | PRIMARY KEY | modulo | petalops.usuario_modulo(modulo) |

### Indices

| Nombre | Definicion |
| --- | --- |
| idx_usuariomodulo_activo | `CREATE INDEX idx_usuariomodulo_activo ON petalops.usuario_modulo USING btree (usuario_id, activo)` |
| pk_usuario_modulo | `CREATE UNIQUE INDEX pk_usuario_modulo ON petalops.usuario_modulo USING btree (usuario_id, modulo)` |

## `vw_contabilidad_resumen_ventas_diario`

**Tipo:** VIEW

**Descripcion:** Resumen diario de ventas por empresa y sucursal. Siempre filtrar por empresa_id y, de ser necesario, por fecha y sucursal.

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | empresa_id | bigint | Si |  | Pendiente documentar |
| 2 | sucursal_id | bigint | Si |  | Pendiente documentar |
| 3 | fecha_operacion | date | Si |  | Pendiente documentar |
| 4 | cantidad_pedidos | bigint | Si |  | Pendiente documentar |
| 5 | total_arreglos_florales | numeric | Si |  | Pendiente documentar |
| 6 | total_domicilios | numeric | Si |  | Pendiente documentar |
| 7 | total_venta | numeric | Si |  | Pendiente documentar |
| 8 | total_efectivo_ventas | numeric | Si |  | Pendiente documentar |

## `vw_contabilidad_venta_pedido`

**Tipo:** VIEW

**Descripcion:** Vista base contable por pedido. Se usa para resumir ventas y efectivo sin duplicar informacion que ya vive en pedido/pago/pago_metodo.

### Columnas

| # | Columna | Tipo | Nulo | Default | Descripcion |
| --- | --- | --- | --- | --- | --- |
| 1 | empresa_id | bigint | Si |  | Pendiente documentar |
| 2 | sucursal_id | bigint | Si |  | Pendiente documentar |
| 3 | id_pedido | integer | Si |  | Pendiente documentar |
| 4 | numero_pedido | bigint | Si |  | Pendiente documentar |
| 5 | fecha_operacion | date | Si |  | Pendiente documentar |
| 6 | fecha_pedido | timestamp without time zone | Si |  | Pendiente documentar |
| 7 | total_bruto | numeric(12,2) | Si |  | Pendiente documentar |
| 8 | total_iva | numeric(12,2) | Si |  | Pendiente documentar |
| 9 | total_domicilios | numeric | Si |  | Pendiente documentar |
| 10 | total_arreglos | numeric | Si |  | Pendiente documentar |
| 11 | total_venta | numeric(12,2) | Si |  | Pendiente documentar |
| 12 | id_pago | integer | Si |  | Pendiente documentar |
| 13 | fecha_pago | timestamp without time zone | Si |  | Pendiente documentar |
| 14 | metodo_pago_snapshot | character varying(100) | Si |  | Pendiente documentar |
| 15 | estado_pago_codigo | character varying(30) | Si |  | Pendiente documentar |
| 16 | estado_pago_nombre | character varying(50) | Si |  | Pendiente documentar |
| 17 | total_efectivo | numeric | Si |  | Pendiente documentar |
