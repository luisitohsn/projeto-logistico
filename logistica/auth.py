import sqlite3

from database import conectar

def fazer_login() -> dict | None:
    """Solicita credenciais e retorna o usuário autenticado ou None."""
    print("\n=== Login ===")

    login = input("Usuário: ").strip()
    senha = input("Senha: ").strip()

    with conectar() as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM usuarios WHERE login = ? AND senha = ?",
            (login, senha)
        ).fetchone()

    if row:
        return dict(row)
    print("Credenciais inválidas.")
    return None