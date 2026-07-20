from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PedidoDisponible(BaseModel):
    numero_pedido: int | None
    destinatario: str | None
    telefono_destinatario: str | None
    arreglo: str | None
    imagen_arreglo: str | None
    imagenes_arreglo: list[str]
    direccion: str | None
    barrio: str | None
    zona: str | None
    hora_entrega: str | None
    fecha_entrega: date | None
    estado_entrega: str | None = None
    asignado_en: datetime | None = None
    en_ruta_en: datetime | None = None
    entregado_en: datetime | None = None
    hora_asignado: str | None = None
    hora_en_ruta: str | None = None
    hora_entregado: str | None = None

    model_config = ConfigDict(from_attributes=True)


class PedidoHistorialNovedad(BaseModel):
    accion: str | None = None
    estado_anterior: str | None = None
    estado_nuevo: str | None = None
    detalle: str | None = None
    registrada_en: datetime | None = None


class PedidoHistorial(BaseModel):
    numero_pedido: int | None
    cliente: str | None
    destinatario: str | None
    telefono_destinatario: str | None
    arreglo: str | None
    imagen_arreglo: str | None
    imagenes_arreglo: list[str]
    direccion: str | None
    barrio: str | None
    zona: str | None
    fecha_asignacion: datetime | None = None
    fecha_entrega: datetime | None = None
    asignado_en: datetime | None = None
    entregado_en: datetime | None = None
    hora_asignado: str | None = None
    hora_entregado: str | None = None
    estado_final: str
    estado_entrega: str | None = None
    novedad: str | None = None
    novedades: list[PedidoHistorialNovedad]
    evidencia_entrega_url: str | None = None
    evidencia_firma_url: str | None = None
    firma_nombre: str | None = None
    firma_documento: str | None = None
    observaciones: str | None = None

    model_config = ConfigDict(from_attributes=True)


class PedidoNovedadItem(BaseModel):
    id_novedad: int
    numero_pedido: int | None
    cliente: str | None
    destinatario: str | None
    telefono_destinatario: str | None
    arreglo: str | None
    imagen_arreglo: str | None
    imagenes_arreglo: list[str]
    direccion: str | None
    barrio: str | None
    zona: str | None
    tipo_novedad: str | None = None
    descripcion: str | None = None
    motivo: str | None = None
    detalle_json: str | None = None
    evidencia_foto_url: str | None = None
    estado_novedad: Literal["abierta", "resuelta"]
    estado_pedido: str | None = None
    reportada_en: datetime | None = None
    resuelta_en: datetime | None = None
    puede_reintentar: bool
    puede_contactar_cliente: bool

    model_config = ConfigDict(from_attributes=True)


class PedidoNovedadResolverRequest(BaseModel):
    solucion: str = Field(min_length=1, max_length=1000)
    observaciones: str | None = Field(default=None, max_length=1000)
    nuevo_estado_pedido: Literal["entregado", "asignado", "en_ruta", "pendiente"] | None = None
    evidencia_foto_url: str | None = None
    firma_nombre: str | None = None
    firma_documento: str | None = None
    firma_imagen_url: str | None = None


class PedidoNovedadResolverResponse(BaseModel):
    status: str
    numero_pedido: int
    id_novedad: int
    estado_novedad: Literal["resuelta"]
    estado_pedido: str
    resuelta_en: datetime | None = None
    mensaje: str


class PedidoAsignadoResponse(BaseModel):
    numero_pedido: int
    id_pedido: int
    id_entrega: int
    estado: str
    domiciliario_id: int
    asignado_en: datetime | None = None
    hora_asignado: str | None = None
    mensaje: str


class PedidoDevueltoResponse(BaseModel):
    numero_pedido: int
    id_pedido: int
    id_entrega: int
    estado: str
    domiciliario_id: None = None
    mensaje: str


class PedidoEstadoResponse(BaseModel):
    numero_pedido: int
    id_pedido: int
    id_entrega: int
    estado: str
    domiciliario_id: int
    asignado_en: datetime | None = None
    en_ruta_en: datetime | None = None
    entregado_en: datetime | None = None
    hora_asignado: str | None = None
    hora_en_ruta: str | None = None
    hora_entregado: str | None = None
    fecha_inicio_entrega: datetime | None = None
    fecha_entrega: datetime | None = None
    mensaje: str


class PedidoEntregadoRequest(BaseModel):
    firma_nombre: str | None = None
    firma_documento: str | None = None
    firma_imagen_url: str | None = None
    evidencia_foto_url: str | None = None
    observaciones: str | None = None


class PedidoNoEntregadoRequest(BaseModel):
    motivo: str
    evidencia_foto_url: str | None = None
    observaciones: str | None = None


class PedidoNovedadRequest(BaseModel):
    tipo_novedad: Literal[
        "cliente_no_disponible",
        "direccion_incorrecta",
        "rechazado_por_cliente",
        "arreglo_danado",
        "otra_novedad",
    ]
    descripcion: str | None = Field(default=None, max_length=1000)
    evidencia_foto_url: str | None = None
