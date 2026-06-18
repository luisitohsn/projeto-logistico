import sqlite3
from database import conectar

def listar_por_cliente(cliente_id: int) -> list[dict]:
    """Retorna todos os pedidos de um cliente específico."""
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM pedidos WHERE cliente_id = ?",
            (cliente_id,)
        ).fetchall()
    return [dict(r) for r in rows]

def buscar_por_id(pedido_id: int) -> dict | None:
    """Retorna um pedido pelo ID ou None se não encontrado."""
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM pedidos WHERE id = ?",
            (pedido_id,)
        ).fetchone()
    return dict(row) if row else None

def listar_todos() -> list[dict]:
    """Retorna todos os pedidos — uso exclusivo de administradores."""
    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM pedidos").fetchall()
    return [dict(r) for r in rows]