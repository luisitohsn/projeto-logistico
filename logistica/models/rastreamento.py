import sqlite3
from database import conectar

def listar_todos() -> list[dict]:
    """Retorna todos os registros de rastreamento."""
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM rastreamento ORDER BY atualizado_em DESC").fetchall()
    return [dict(r) for r in rows]

def historico(pedido_id: int) -> list[dict]:
    """Busca o histórico de rastreamento de um pedido pelo seu ID."""
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM rastreamento WHERE pedido_id = ? ORDER BY atualizado_em DESC",
            (pedido_id,)
        ).fetchall()
    return [dict(r) for r in rows]


def ultimo(pedido_id: int) -> dict | None:
    """Retorna o último registro de rastreamento (mais recente) para um pedido."""
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM rastreamento WHERE pedido_id = ? ORDER BY atualizado_em DESC LIMIT 1",
            (pedido_id,)
        ).fetchone()
    return dict(row) if row else None