from database import conectar, criar_tabelas

def popular():
    """Insere dados iniciais fictícios para testes."""
    criar_tabelas()
    with conectar() as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO usuarios (nome, login, senha, perfil) VALUES (?,?,?,?)",
            [
                ("Ana Lima",    "ana",   "1234", "cliente"),
                ("Carlos Melo", "carlos","1234", "cliente"),
                ("Admin Sys",   "admin", "admin","admin"),
            ]
        )
        conn.executemany(
            "INSERT OR IGNORE INTO veiculos (placa, motorista, status) VALUES (?,?,?)",
            [
                ("ABC-1234", "João Silva",   "em_rota"),
                ("DEF-5678", "Maria Santos", "disponivel"),
            ]
        )
        # Insere pedido apenas se não existir (evita duplicatas em múltiplas execuções do seed)
        pedido_row = conn.execute(
            "SELECT id FROM pedidos WHERE cliente_id = ? AND descricao = ? AND origem = ? AND destino = ?",
            (1, 'Eletrônicos', 'São Paulo', 'Rio de Janeiro')
        ).fetchone()

        if pedido_row:
            pedido_id = pedido_row[0]
        else:
            conn.execute(
                "INSERT INTO pedidos (cliente_id, descricao, origem, destino, status) VALUES (?,?,?,?,?)",
                (1, 'Eletrônicos', 'São Paulo', 'Rio de Janeiro', 'em_transito')
            )
            pedido_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

        # Insere rastreamento apenas se não existir para o pedido
        rast_row = conn.execute(
            "SELECT id FROM rastreamento WHERE pedido_id = ? AND localizacao = ? AND status = ?",
            (pedido_id, 'Rodovia Dutra km 180', 'Em trânsito')
        ).fetchone()
        if not rast_row:
            conn.execute(
                "INSERT INTO rastreamento (pedido_id, localizacao, status) VALUES (?,?,?)",
                (pedido_id, 'Rodovia Dutra km 180', 'Em trânsito')
            )

        # Insere custos apenas se não existir para o pedido
        custo_row = conn.execute(
            "SELECT id FROM custos WHERE pedido_id = ?",
            (pedido_id,)
        ).fetchone()
        if not custo_row:
            conn.execute(
                "INSERT INTO custos (pedido_id, frete, outros, total) VALUES (?,?,?,?)",
                (pedido_id, 150.0, 20.0, 170.0)
            )
    print("Dados de teste inseridos.")


def corrigir_duplicatas():
    """Encontra pedidos duplicados (mesmo cliente, descrição, origem e destino),
    mantém o mais antigo e consolida `rastreamento` e `custos` para o registro mantido.
    Remove os pedidos duplicados que sobraram.
    """
    from database import conectar

    with conectar() as conn:
        conn.row_factory = None
        # Encontrar grupos duplicados
        dup_groups = conn.execute(
            """
            SELECT cliente_id, descricao, origem, destino, COUNT(*) as cnt
            FROM pedidos
            GROUP BY cliente_id, descricao, origem, destino
            HAVING cnt > 1
            """
        ).fetchall()

        for grupo in dup_groups:
            cliente_id, descricao, origem, destino, _ = grupo
            rows = conn.execute(
                "SELECT id FROM pedidos WHERE cliente_id = ? AND descricao = ? AND origem = ? AND destino = ? ORDER BY criado_em ASC",
                (cliente_id, descricao, origem, destino)
            ).fetchall()
            ids = [r[0] for r in rows]
            keep_id = ids[0]
            dup_ids = ids[1:]
            for did in dup_ids:
                conn.execute("UPDATE rastreamento SET pedido_id = ? WHERE pedido_id = ?", (keep_id, did))
                conn.execute("UPDATE custos SET pedido_id = ? WHERE pedido_id = ?", (keep_id, did))
                conn.execute("DELETE FROM pedidos WHERE id = ?", (did,))
            print(f"Consolidado pedidos {ids} -> mantendo {keep_id}")

        # Remover custos duplicados por pedido (manter o primeiro)
        dup_custos = conn.execute(
            "SELECT pedido_id, COUNT(*) as cnt FROM custos GROUP BY pedido_id HAVING cnt > 1"
        ).fetchall()
        for pc in dup_custos:
            pedido_id = pc[0]
            rows = conn.execute("SELECT id FROM custos WHERE pedido_id = ? ORDER BY id", (pedido_id,)).fetchall()
            ids = [r[0] for r in rows]
            keep = ids[0]
            for rid in ids[1:]:
                conn.execute("DELETE FROM custos WHERE id = ?", (rid,))
            print(f"Consolidado custos para pedido {pedido_id}: mantendo {keep}, removidos {ids[1:]}")


if __name__ == "__main__":
    popular()
    corrigir_duplicatas()