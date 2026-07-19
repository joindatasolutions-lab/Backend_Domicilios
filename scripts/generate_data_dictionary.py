from __future__ import annotations

import argparse
import os
from collections import defaultdict
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT_DIR / "docs" / "diccionario_datos_petalops.md"


def load_env(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ[key.strip()] = value.strip().strip('"').strip("'")


def fetch_schema_metadata(schema: str) -> dict:
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )

    with conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """
            select
                t.table_name,
                t.table_type,
                obj_description(c.oid) as table_comment
            from information_schema.tables t
            join pg_catalog.pg_namespace n
                on n.nspname = t.table_schema
            join pg_catalog.pg_class c
                on c.relnamespace = n.oid
                and c.relname = t.table_name
            where t.table_schema = %s
            order by t.table_name;
            """,
            (schema,),
        )
        tables = list(cur.fetchall())

        cur.execute(
            """
            select
                c.table_name,
                c.ordinal_position,
                c.column_name,
                c.data_type,
                c.udt_name,
                c.character_maximum_length,
                c.numeric_precision,
                c.numeric_scale,
                c.is_nullable,
                c.column_default,
                col_description(pc.oid, c.ordinal_position) as column_comment
            from information_schema.columns c
            join pg_catalog.pg_namespace n
                on n.nspname = c.table_schema
            join pg_catalog.pg_class pc
                on pc.relnamespace = n.oid
                and pc.relname = c.table_name
            where c.table_schema = %s
            order by c.table_name, c.ordinal_position;
            """,
            (schema,),
        )
        columns = list(cur.fetchall())

        cur.execute(
            """
            select
                tc.table_name,
                tc.constraint_name,
                tc.constraint_type,
                kcu.column_name,
                kcu.ordinal_position,
                ccu.table_schema as foreign_table_schema,
                ccu.table_name as foreign_table_name,
                ccu.column_name as foreign_column_name
            from information_schema.table_constraints tc
            left join information_schema.key_column_usage kcu
                on tc.constraint_schema = kcu.constraint_schema
                and tc.constraint_name = kcu.constraint_name
            left join information_schema.constraint_column_usage ccu
                on tc.constraint_schema = ccu.constraint_schema
                and tc.constraint_name = ccu.constraint_name
            where tc.table_schema = %s
            order by tc.table_name, tc.constraint_type, tc.constraint_name, kcu.ordinal_position;
            """,
            (schema,),
        )
        constraints = list(cur.fetchall())

        cur.execute(
            """
            select
                schemaname as table_schema,
                tablename as table_name,
                indexname as index_name,
                indexdef as index_definition
            from pg_catalog.pg_indexes
            where schemaname = %s
            order by tablename, indexname;
            """,
            (schema,),
        )
        indexes = list(cur.fetchall())

    conn.close()

    return {
        "schema": schema,
        "tables": tables,
        "columns": columns,
        "constraints": constraints,
        "indexes": indexes,
    }


def format_type(column: dict) -> str:
    data_type = column["data_type"]
    if column["character_maximum_length"]:
        return f"{data_type}({column['character_maximum_length']})"
    if data_type in {"numeric", "decimal"} and column["numeric_precision"] and column["numeric_scale"] is not None:
        return f"{data_type}({column['numeric_precision']},{column['numeric_scale']})"
    if data_type == "USER-DEFINED":
        return column["udt_name"]
    return data_type


def cell(value: object) -> str:
    if value is None:
        return ""
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[list[str]], headers: list[str]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(value) for value in row) + " |")
    return "\n".join(lines)


def build_markdown(metadata: dict) -> str:
    schema = metadata["schema"]
    tables = metadata["tables"]

    columns_by_table = defaultdict(list)
    for column in metadata["columns"]:
        columns_by_table[column["table_name"]].append(column)

    constraints_by_table = defaultdict(list)
    for constraint in metadata["constraints"]:
        constraints_by_table[constraint["table_name"]].append(constraint)

    indexes_by_table = defaultdict(list)
    for index in metadata["indexes"]:
        indexes_by_table[index["table_name"]].append(index)

    lines = [
        f"# Diccionario de Datos - Esquema `{schema}`",
        "",
        "Documento generado a partir de los metadatos del esquema PostgreSQL.",
        "",
        "## Resumen",
        "",
        markdown_table(
            [[str(len(tables)), str(len(metadata["columns"])), str(len(metadata["constraints"]))]],
            ["Tablas/Vistas", "Columnas", "Restricciones"],
        ),
        "",
        "## Objetos",
        "",
    ]

    if tables:
        lines.append(
            markdown_table(
                [
                    [
                        table["table_name"],
                        table["table_type"],
                        table["table_comment"] or "Pendiente documentar",
                    ]
                    for table in tables
                ],
                ["Objeto", "Tipo", "Descripcion"],
            )
        )
    else:
        lines.append("No se encontraron tablas o vistas en el esquema.")

    for table in tables:
        table_name = table["table_name"]
        lines.extend(
            [
                "",
                f"## `{table_name}`",
                "",
                f"**Tipo:** {table['table_type']}",
                "",
                f"**Descripcion:** {table['table_comment'] or 'Pendiente documentar'}",
                "",
                "### Columnas",
                "",
            ]
        )

        column_rows = []
        for column in columns_by_table[table_name]:
            column_rows.append(
                [
                    str(column["ordinal_position"]),
                    column["column_name"],
                    format_type(column),
                    "Si" if column["is_nullable"] == "YES" else "No",
                    column["column_default"] or "",
                    column["column_comment"] or "Pendiente documentar",
                ]
            )
        lines.append(
            markdown_table(
                column_rows,
                ["#", "Columna", "Tipo", "Nulo", "Default", "Descripcion"],
            )
        )

        table_constraints = constraints_by_table[table_name]
        if table_constraints:
            lines.extend(["", "### Restricciones", ""])
            rows = []
            for constraint in table_constraints:
                reference = ""
                if constraint["foreign_table_name"]:
                    reference = (
                        f"{constraint['foreign_table_schema']}."
                        f"{constraint['foreign_table_name']}"
                        f"({constraint['foreign_column_name']})"
                    )
                rows.append(
                    [
                        constraint["constraint_name"],
                        constraint["constraint_type"],
                        constraint["column_name"] or "",
                        reference,
                    ]
                )
            lines.append(markdown_table(rows, ["Nombre", "Tipo", "Columna", "Referencia"]))

        table_indexes = indexes_by_table[table_name]
        if table_indexes:
            lines.extend(["", "### Indices", ""])
            lines.append(
                markdown_table(
                    [
                        [index["index_name"], f"`{index['index_definition']}`"]
                        for index in table_indexes
                    ],
                    ["Nombre", "Definicion"],
                )
            )

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera el diccionario de datos del esquema PostgreSQL.")
    parser.add_argument("--env", default=ROOT_DIR / ".env", type=Path)
    parser.add_argument("--output", default=DEFAULT_OUTPUT, type=Path)
    parser.add_argument("--schema", default=None)
    args = parser.parse_args()

    load_env(args.env)
    schema = args.schema or os.environ.get("DB_SCHEMA", "petalops")
    metadata = fetch_schema_metadata(schema)
    markdown = build_markdown(metadata)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(markdown, encoding="utf-8")
    print(f"Diccionario generado: {args.output}")
    print(f"Objetos: {len(metadata['tables'])}")
    print(f"Columnas: {len(metadata['columns'])}")


if __name__ == "__main__":
    main()
