
import sqlite3
from database import conectar

def listar_todos() -> list[dict]:
	"""Retorna todos os custos cadastrados."""
	with conectar() as conn:
		conn.row_factory = sqlite3.Row
		rows = conn.execute("SELECT * FROM custos").fetchall()
	return [dict(r) for r in rows]
