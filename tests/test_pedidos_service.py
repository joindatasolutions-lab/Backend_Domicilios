from datetime import date

from app.core.security import CurrentDomiciliario
from app.services.pedidos import (
    _buscar_pedido_domiciliario_para_estado,
    listar_pedidos_asignados,
    listar_pedidos_disponibles,
)


class _FakeResult:
    def mappings(self):
        return self

    def all(self):
        return []


class _FakeDb:
    def __init__(self):
        self.statement = None
        self.params = None

    def execute(self, statement, params):
        self.statement = statement
        self.params = params
        return _FakeResult()


def test_listar_pedidos_asignados_includes_delivered_by_actual_delivery_date() -> None:
    db = _FakeDb()
    domiciliario = CurrentDomiciliario(
        id_empleado=7,
        empresa_id=3,
        sucursal_id=11,
        usuario="mateo",
        cargo="domiciliario",
    )

    result = listar_pedidos_asignados(
        db,
        domiciliario=domiciliario,
        fecha=date(2026, 7, 22),
    )

    sql = str(db.statement)
    assert result == []
    assert "ee.codigo in ('asignado', 'en_ruta', 'entregado')" in sql
    assert "join estado_pedido ep" in sql
    assert "lower(regexp_replace(trim(ep.nombre_estado), '\\s+', ' ', 'g')) = 'aprobado'" in sql
    assert "when ee.codigo = 'entregado'" in sql
    assert "e.fechaentrega::date + nullif(e.fechaentrega::time, time '00:00')" in sql
    assert "de.entregado_en" in sql
    assert db.params == {
        "empresa_id": 3,
        "domiciliario_id": 7,
        "sucursal_id": 11,
        "fecha": date(2026, 7, 22),
        "limit": 100,
        "offset": 0,
    }


def test_listar_pedidos_disponibles_requires_para_entrega_production_state() -> None:
    db = _FakeDb()

    result = listar_pedidos_disponibles(
        db,
        empresa_id=3,
        sucursal_id=11,
        fecha=date(2026, 7, 28),
    )

    sql = str(db.statement)
    assert result == []
    assert "join estado_pedido ep" not in sql
    assert "from entrega e" in sql
    assert "join produccion prod" in sql
    assert "on prod.id_produccion = e.produccionid" in sql
    assert "join pedido p" in sql
    assert "p.id_pedido = coalesce(prod.pedido_id, pd_link.pedido_id)" in sql
    assert "ee.codigo = 'pendiente'" in sql
    assert "join estado_produccion eprod" in sql
    assert (
        "lower(regexp_replace(trim(coalesce(eprod.codigo, eprod.nombre, '')), '\\s+', '', 'g'))"
    ) in sql
    assert "in ('paraentrega', 'paraentregar')" in sql
    assert "'aprobado'" not in sql
    assert db.params == {
        "empresa_id": 3,
        "sucursal_id": 11,
        "fecha": date(2026, 7, 28),
        "limit": 100,
        "offset": 0,
    }


def test_buscar_pedido_domiciliario_para_estado_requires_approved_order() -> None:
    db = _FakeDb()
    domiciliario = CurrentDomiciliario(
        id_empleado=7,
        empresa_id=3,
        sucursal_id=11,
        usuario="mateo",
        cargo="domiciliario",
    )

    result = _buscar_pedido_domiciliario_para_estado(
        db,
        numero_pedido=96650,
        domiciliario=domiciliario,
        estado_origen="asignado",
    )

    sql = str(db.statement)
    assert result == []
    assert "join estado_pedido ep" in sql
    assert "lower(regexp_replace(trim(ep.nombre_estado), '\\s+', ' ', 'g')) = 'aprobado'" in sql
    assert db.params == {
        "empresa_id": 3,
        "numero_pedido": 96650,
        "domiciliario_id": 7,
        "estado_origen": "asignado",
        "sucursal_id": 11,
    }
