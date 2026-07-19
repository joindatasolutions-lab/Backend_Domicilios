# PetalOps Domicilios Backend

Backend para la app de domiciliarios de PetalOps, construido con FastAPI y PostgreSQL.

## Requisitos

- Python 3.12+
- PostgreSQL accesible desde la maquina local
- Credenciales AWS S3 si se van a subir fotos de perfil

## Instalacion

```bash
pip install -r requirements.txt
```

Crear el archivo `.env` a partir de `.env.example` y configurar las variables de base de datos, JWT, CORS y S3.

Para produccion, `BACKEND_CORS_ORIGINS` debe incluir el dominio del frontend:

```text
https://domiapp.joindata.com.co
```

Para pruebas desde Vite/local, `BACKEND_CORS_ORIGIN_REGEX` permite `localhost` y `127.0.0.1` en cualquier puerto. Si se desactiva ese regex en Cloud Run, agregar tambien el origen local exacto a `BACKEND_CORS_ORIGINS`, por ejemplo `http://127.0.0.1:5174`.

En Cloud Run, si la base de datos no es accesible, los endpoints que consultan PostgreSQL devuelven `503`. Configurar `DB_CONNECT_TIMEOUT=3` para evitar esperas largas mientras se valida conectividad.

Si PostgreSQL esta en Cloud SQL, configurar `DB_CLOUD_SQL_INSTANCE` con el formato `project:region:instance` y desplegar Cloud Run con la instancia adjunta. En ese modo la app conecta por socket Unix en `/cloudsql/...` y no usa la IP publica de `DB_HOST`.

## Ejecutar En Local

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Health checks:

```text
GET http://127.0.0.1:8000/health
GET http://127.0.0.1:8000/api/v1/health
GET http://127.0.0.1:8000/api/v1/health/db
```

## Login Multitenant

El login de domiciliarios usa la tabla `usuario` para autenticar y luego se une con `empleado` usando `empleado.usuario_id = usuario.id_usuario`.

El frontend no necesita enviar `empresa_id` ni `sucursal_id` en el login inicial. El backend infiere el tenant desde el usuario autenticado.

Endpoint:

```text
POST /api/v1/auth/domiciliarios/login
```

Payload:

```json
{
  "usuario": "domi.demo2",
  "password": "abc123"
}
```

Respuesta resumida:

```json
{
  "access_token": "...",
  "token_type": "bearer",
  "domiciliario": {
    "id_empleado": 50,
    "empresa_id": 2,
    "sucursal_id": 2,
    "tenant": {
      "empresa_id": 2,
      "nombre": "Petalops",
      "nombre_comercial": "Petalops",
      "slug": "petalops",
      "logo_url": "https://..."
    },
    "nombre": "Valentina Cruz",
    "nombre_empleado": "Valentina Cruz",
    "usuario": "domi.demo2",
    "email": "domi.demo2@petalops.local",
    "cargo": "Domiciliario",
    "foto_url": "https://..."
  }
}
```

Si el mismo login existe en varias empresas y el frontend no envia `empresa_id`, el backend responde `409 Conflict` para evitar una autenticacion ambigua.

## Credenciales Demo

```text
Empresa 2:
usuario: domi.demo2
password: abc123

Empresa 3:
usuario: domi.demo3
password: abc123
```

## Instruccion Para El Frontend

En login enviar solo:

```js
body: JSON.stringify({
  usuario,
  password,
})
```

Despues del login guardar el token, el tenant y los ids inferidos:

```js
const data = await response.json();

localStorage.setItem("token", data.access_token);
localStorage.setItem("empresa_id", data.domiciliario.empresa_id);
localStorage.setItem("sucursal_id", data.domiciliario.sucursal_id);
localStorage.setItem("tenant", JSON.stringify(data.domiciliario.tenant));
```

Para pintar la identidad de empresa:

```jsx
const tenant = JSON.parse(localStorage.getItem("tenant"));

<img
  src={tenant.logo_url}
  alt={tenant.nombre_comercial || tenant.nombre}
/>
```

Las siguientes peticiones protegidas deben enviar:

```text
Authorization: Bearer <access_token>
```

Y cuando un endpoint lo solicite por query, usar los valores devueltos por el login:

```text
empresa_id=<domiciliario.empresa_id>
sucursal_id=<domiciliario.sucursal_id>
```

## Fotos Y S3

Endpoint para subir foto del domiciliario:

```text
POST /api/v1/auth/domiciliarios/me/foto
Content-Type: multipart/form-data
campo archivo: foto
```

Tipos permitidos:

```text
image/jpeg
image/png
image/webp
```

Variables principales:

```text
AWS_REGION
AWS_S3_BUCKET
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_SESSION_TOKEN
CLOUDFRONT_DOMAIN
AWS_S3_PUBLIC_BASE_URL
AWS_S3_OBJECT_ACL
```

`AWS_S3_PUBLIC_BASE_URL` tiene prioridad para construir URLs publicas. Si no esta configurado, se usa `CLOUDFRONT_DOMAIN`. Si tampoco existe, se genera URL directa de S3.

## Endpoints Principales

Autenticacion:

```text
POST /api/v1/auth/domiciliarios/login
GET /api/v1/auth/domiciliarios/me
PATCH /api/v1/auth/domiciliarios/me/foto
POST /api/v1/auth/domiciliarios/me/foto
```

Pedidos:

```text
GET /api/v1/pedidos/disponibles
GET /api/v1/pedidos/asignados
POST /api/v1/pedidos/{numero_pedido}/asignarme
POST /api/v1/pedidos/{numero_pedido}/devolver
POST /api/v1/pedidos/{numero_pedido}/iniciar-entrega
POST /api/v1/pedidos/{numero_pedido}/entregar
POST /api/v1/pedidos/{numero_pedido}/no-entregado
POST /api/v1/pedidos/{numero_pedido}/novedad
```

## Estructura

```text
app/
  api/v1/          Rutas versionadas
  core/            Configuracion, seguridad y tenant
  db/              Conexion a base de datos
  schemas/         Schemas Pydantic
  services/        Logica de negocio
docs/              Documentacion del proyecto
scripts/           Scripts de soporte
tests/             Pruebas
```

## Pruebas

```bash
pytest
```
