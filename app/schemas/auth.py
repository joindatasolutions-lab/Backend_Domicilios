from pydantic import BaseModel, Field


class TenantData(BaseModel):
    empresa_id: int
    nombre: str
    nombre_comercial: str | None = None
    slug: str | None = None
    logo_url: str | None = None


class DomiciliarioLoginRequest(BaseModel):
    empresa_id: int | None = Field(default=None, gt=0)
    usuario: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=255)
    sucursal_id: int | None = Field(default=None, gt=0)


class DomiciliarioAuthData(BaseModel):
    id_empleado: int
    empresa_id: int
    sucursal_id: int | None
    tenant: TenantData | None = None
    nombre: str | None = None
    nombre_empleado: str
    usuario: str | None
    email: str | None
    cargo: str
    foto_url: str | None = None


class DomiciliarioLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    domiciliario: DomiciliarioAuthData


class DomiciliarioFotoRequest(BaseModel):
    foto_url: str = Field(min_length=1, max_length=1000)


class DomiciliarioPerfilResponse(DomiciliarioAuthData):
    pass
