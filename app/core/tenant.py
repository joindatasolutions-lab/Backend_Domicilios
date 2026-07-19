from typing import Annotated

from fastapi import Query
from pydantic import BaseModel


class TenantContext(BaseModel):
    empresa_id: int
    sucursal_id: int | None = None


def get_tenant_context(
    empresa_id: Annotated[int, Query(gt=0)],
    sucursal_id: Annotated[int | None, Query(gt=0)] = None,
) -> TenantContext:
    return TenantContext(empresa_id=empresa_id, sucursal_id=sucursal_id)
