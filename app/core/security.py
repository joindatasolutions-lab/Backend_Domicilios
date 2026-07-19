from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.core.config import settings


ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/domiciliarios/login")


class CurrentDomiciliario(BaseModel):
    id_empleado: int
    empresa_id: int
    sucursal_id: int | None = None
    usuario: str
    cargo: str


def verify_password(plain_password: str, hashed_password: str | None) -> bool:
    if not hashed_password:
        return False
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, claims: dict[str, Any] | None = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload: dict[str, Any] = {"sub": subject, "exp": expire}
    if claims:
        payload.update(claims)
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


def get_current_domiciliario(token: str = Depends(oauth2_scheme)) -> CurrentDomiciliario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        employee_id = payload.get("sub")
        if not employee_id or payload.get("tipo") != "domiciliario":
            raise credentials_exception
        return CurrentDomiciliario(
            id_empleado=int(employee_id),
            empresa_id=int(payload["empresa_id"]),
            sucursal_id=payload.get("sucursal_id"),
            usuario=payload.get("usuario") or str(employee_id),
            cargo=payload.get("cargo") or "Domiciliario",
        )
    except (JWTError, KeyError, TypeError, ValueError) as exc:
        raise credentials_exception from exc
