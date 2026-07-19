import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.core.security import CurrentDomiciliario
from app.schemas.auth import DomiciliarioLoginRequest
from app.services.storage import subir_foto_empleado


INVALID_CREDENTIALS = "Usuario o contrasena invalidos"
AMBIGUOUS_CREDENTIALS = "El usuario pertenece a varias empresas. Seleccione empresa."
logger = logging.getLogger(__name__)


def _tenant_identity(row) -> dict:
    return {
        "empresa_id": row["empresa_id"],
        "nombre": row["tenant_nombre"],
        "nombre_comercial": row["tenant_nombre_comercial"],
        "slug": row["tenant_slug"],
        "logo_url": row["tenant_logo_url"],
    }


def login_domiciliario(db: Session, credentials: DomiciliarioLoginRequest) -> dict:
    query = text(
        """
        select
            e.id_empleado,
            e.empresa_id,
            e.sucursal_id,
            u.nombre,
            u.nombre as nombre_empleado,
            u.login as usuario,
            u.email,
            e.cargo,
            e.foto_url,
            u.passwordhash,
            emp.nombre_empresa as tenant_nombre,
            emp.nombre_comercial as tenant_nombre_comercial,
            emp.slug as tenant_slug,
            emp.logo_url as tenant_logo_url
        from usuario u
        join empleado e on e.usuario_id = u.id_usuario
        join empresa emp on emp.id_empresa = e.empresa_id
        where (cast(:empresa_id as bigint) is null or u.empresa_id = cast(:empresa_id as bigint))
            and (cast(:empresa_id as bigint) is null or e.empresa_id = cast(:empresa_id as bigint))
            and (cast(:sucursal_id as bigint) is null or u.sucursal_id = cast(:sucursal_id as bigint))
            and (cast(:sucursal_id as bigint) is null or e.sucursal_id = cast(:sucursal_id as bigint))
            and lower(u.estado) = 'activo'
            and e.activo = 1
            and lower(e.cargo) = 'domiciliario'
            and (
                lower(u.login) = lower(:usuario)
                or lower(u.email) = lower(:usuario)
            )
        order by u.empresa_id, u.sucursal_id, u.id_usuario
        limit 2;
        """
    )
    try:
        rows = db.execute(
            query,
            {
                "empresa_id": credentials.empresa_id,
                "sucursal_id": credentials.sucursal_id,
                "usuario": credentials.usuario.strip(),
            },
        ).mappings().all()
    except SQLAlchemyError as exc:
        logger.exception(
            "Database query failed during domiciliario login for target %s",
            settings.database_connection_target,
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo conectar con la base de datos",
        ) from exc

    if len(rows) > 1 and credentials.empresa_id is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=AMBIGUOUS_CREDENTIALS,
        )

    row = rows[0] if rows else None
    if not row or not verify_password(credentials.password, row["passwordhash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_CREDENTIALS,
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        db.execute(
            text("update usuario set ultimo_login = now() where login = :usuario and empresa_id = :empresa_id"),
            {"usuario": row["usuario"], "empresa_id": row["empresa_id"]},
        )
        db.commit()
    except SQLAlchemyError:
        db.rollback()

    domiciliario = {
        "id_empleado": row["id_empleado"],
        "empresa_id": row["empresa_id"],
        "sucursal_id": row["sucursal_id"],
        "tenant": _tenant_identity(row),
        "nombre": row["nombre"],
        "nombre_empleado": row["nombre_empleado"],
        "usuario": row["usuario"],
        "email": row["email"],
        "cargo": row["cargo"],
        "foto_url": row["foto_url"],
    }
    access_token = create_access_token(
        subject=str(row["id_empleado"]),
        claims={
            "empresa_id": row["empresa_id"],
            "sucursal_id": row["sucursal_id"],
            "usuario": row["usuario"] or row["email"] or str(row["id_empleado"]),
            "cargo": row["cargo"],
            "tipo": "domiciliario",
        },
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "domiciliario": domiciliario,
    }


def obtener_perfil_domiciliario(db: Session, domiciliario: CurrentDomiciliario) -> dict:
    row = db.execute(
        text(
            """
            select
                e.id_empleado,
                e.empresa_id,
                e.sucursal_id,
                u.nombre,
                u.nombre as nombre_empleado,
                u.login as usuario,
                u.email,
                e.cargo,
                e.foto_url,
                emp.nombre_empresa as tenant_nombre,
                emp.nombre_comercial as tenant_nombre_comercial,
                emp.slug as tenant_slug,
                emp.logo_url as tenant_logo_url
            from empleado e
            join usuario u on u.id_usuario = e.usuario_id
            join empresa emp on emp.id_empresa = e.empresa_id
            where e.id_empleado = :id_empleado
                and e.empresa_id = :empresa_id
                and e.activo = 1
                and lower(u.estado) = 'activo'
                and lower(e.cargo) = 'domiciliario'
            limit 1
            """
        ),
        {
            "id_empleado": domiciliario.id_empleado,
            "empresa_id": domiciliario.empresa_id,
        },
    ).mappings().first()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domiciliario no encontrado",
        )
    perfil = dict(row)
    perfil["tenant"] = _tenant_identity(perfil)
    perfil.pop("tenant_nombre")
    perfil.pop("tenant_nombre_comercial")
    perfil.pop("tenant_slug")
    perfil.pop("tenant_logo_url")
    return perfil


def actualizar_foto_domiciliario(
    db: Session,
    *,
    domiciliario: CurrentDomiciliario,
    foto_url: str,
) -> dict:
    row = db.execute(
        text(
            """
            with empleado_actualizado as (
                update empleado
                set
                    foto_url = :foto_url,
                    updated_at = now()
                where id_empleado = :id_empleado
                    and empresa_id = :empresa_id
                    and activo = 1
                    and lower(cargo) = 'domiciliario'
                returning
                    id_empleado,
                    empresa_id,
                    sucursal_id,
                    usuario_id,
                    cargo,
                    foto_url
            )
            select
                e.id_empleado,
                e.empresa_id,
                e.sucursal_id,
                u.nombre,
                u.nombre as nombre_empleado,
                u.login as usuario,
                u.email,
                e.cargo,
                e.foto_url,
                emp.nombre_empresa as tenant_nombre,
                emp.nombre_comercial as tenant_nombre_comercial,
                emp.slug as tenant_slug,
                emp.logo_url as tenant_logo_url
            from empleado_actualizado e
            join usuario u on u.id_usuario = e.usuario_id
            join empresa emp on emp.id_empresa = e.empresa_id
            where lower(u.estado) = 'activo'
            """
        ),
        {
            "foto_url": foto_url,
            "id_empleado": domiciliario.id_empleado,
            "empresa_id": domiciliario.empresa_id,
        },
    ).mappings().first()

    if row is None:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domiciliario no encontrado",
        )

    db.commit()
    perfil = dict(row)
    perfil["tenant"] = _tenant_identity(perfil)
    perfil.pop("tenant_nombre")
    perfil.pop("tenant_nombre_comercial")
    perfil.pop("tenant_slug")
    perfil.pop("tenant_logo_url")
    return perfil


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


def subir_y_actualizar_foto_domiciliario(
    db: Session,
    *,
    domiciliario: CurrentDomiciliario,
    file,
) -> dict:
    tenant_slug = _obtener_tenant_slug(db, domiciliario.empresa_id)
    _, foto_url = subir_foto_empleado(
        tenant_slug=tenant_slug,
        id_empleado=domiciliario.id_empleado,
        file=file,
    )
    return actualizar_foto_domiciliario(
        db,
        domiciliario=domiciliario,
        foto_url=foto_url,
    )
