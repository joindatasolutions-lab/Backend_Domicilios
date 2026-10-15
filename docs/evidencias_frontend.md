# Evidencias al confirmar entrega

`POST /api/v1/pedidos/{numero_pedido}/entregar` acepta JSON con URLs existentes o
`multipart/form-data` con archivos. Requiere `Authorization: Bearer <token>`.
Se conserva el parametro opcional `?sucursal_id=...` y la respuesta de confirmacion
actual. El pedido debe estar asignado al domiciliario y en estado `en_ruta`.

Campos multipart (todos opcionales, como en el contrato JSON anterior):

| Campo | Tipo |
| --- | --- |
| `foto` | Un archivo JPG, PNG o WEBP |
| `firma` | Un archivo JPG, PNG o WEBP |
| `firma_nombre` | Texto |
| `firma_documento` | Texto |
| `observaciones` | Texto |
| `evidencia_foto_url` | URL existente, si no se envia `foto` |
| `firma_imagen_url` | URL existente, si no se envia `firma` |

Si se envia archivo y URL para la misma evidencia, prevalece el archivo.
El backend sube los archivos a S3 y guarda sus URLs con la entrega.
No enviar base64 ni URLs `blob:` como evidencia: convertir la firma del canvas
en un Blob PNG y adjuntarlo con nombre de archivo.

```javascript
const form = new FormData();
if (foto) form.append("foto", foto, foto.name || "foto.jpg");
if (firmaBlob) form.append("firma", firmaBlob, "firma.png");
form.append("firma_nombre", nombre || "");
form.append("firma_documento", documento || "");
form.append("observaciones", observaciones || "");

const response = await fetch(`${API_URL}/api/v1/pedidos/${numeroPedido}/entregar`, {
  method: "POST",
  headers: { Authorization: `Bearer ${token}` },
  body: form,
});
const resultado = await response.json();
if (!response.ok) {
  throw new Error(typeof resultado.detail === "string"
    ? resultado.detail : "No se pudo confirmar la entrega");
}
// Mostrar exito y actualizar el pedido solo despues de recibir HTTP 200.
```

No fijar `Content-Type` manualmente ni usar un interceptor que fuerce JSON.
Para obtener la firma: `canvas.toBlob(callback, "image/png")`; esperar el Blob
antes de enviar. Omitir archivos ausentes, no enviar las cadenas `null`/`undefined`.

Errores: 401 token invalido/ausente; 409 pedido o estado no valido; 415 formato
de archivo no admitido; 422 datos invalidos; 503 fallo de almacenamiento.
Conservar los archivos seleccionados cuando falle la peticion.

Las URLs se consultan en `GET /api/v1/pedidos/historial` como
`evidencia_entrega_url` y `evidencia_firma_url`; la respuesta de `/entregar`
mantiene su formato anterior, sin agregar URLs.

`/novedad` mantiene su contrato actual (`tipo_novedad`, `descripcion`, `foto`).
`/no-entregado` y la resolucion de novedades siguen recibiendo JSON con URLs.

Operacion: requiere la configuracion S3 existente. No necesita migracion.
S3 y la base de datos no comparten transaccion: si se sube un archivo y luego
falla otra subida o la confirmacion, puede quedar un objeto sin asociar en S3.
