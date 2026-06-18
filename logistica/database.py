import sqlite3

DB = "logistica.db"


def conectar():
    """Retorna uma conexão com o banco de dados."""
    return sqlite3.connect(DB)


def criar_tabelas():
    """Cria todas as tabelas se ainda não existirem."""
    with conectar() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            nome            TEXT NOT NULL,
            login           TEXT UNIQUE NOT NULL,
            senha           TEXT NOT NULL,
            perfil          TEXT NOT NULL CHECK (perfil IN ('cliente', 'admin'))
        );
        CREATE TABLE IF NOT EXISTS pedidos (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id      INTEGER REFERENCES usuarios(id),
            descricao       TEXT NOT NULL,
            origem          TEXT NOT NULL,
            destino         TEXT NOT NULL,
            status          TEXT DEFAULT 'pendente',
            criado_em       TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS rastreamento (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id       INTEGER REFERENCES pedidos(id),
            localizacao     TEXT NOT NULL,
            status          TEXT NOT NULL,
            atualizado_em   TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS veiculos (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            placa           TEXT UNIQUE NOT NULL,
            motorista       TEXT NOT NULL,
            status          TEXT DEFAULT 'disponivel'
        );
        CREATE TABLE IF NOT EXISTS custos (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id       INTEGER REFERENCES pedidos(id),
            frete           REAL NOT NULL,
            outros          REAL DEFAULT 0.0,
            total           REAL NOT NULL
        );
        """)
if __name__ == "__main__":
    criar_tabelas()
    print("Tabelas criadas com sucesso.")