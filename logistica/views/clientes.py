from models import pedidos, rastreamento
from utils.display import tabela_pedidos

def menu(usuario: dict):
    """Exibe o menu e ações disponíveis para o perfil cliente."""
    while True:
        print(f"\nOlá, {usuario['nome']}!")
        print("1. Meus pedidos")
        print("2. Rastrear pedido")
        print("0. Sair")
        op = input("Escolha: ").strip()

        if op == "1":
            lista = pedidos.listar_por_cliente(usuario["id"])
            tabela_pedidos(lista)
        elif op == "2":
            pid = input("ID do pedido: ").strip()
            if pid.isdigit():
                pid_i = int(pid)
                pedido = pedidos.buscar_por_id(pid_i)
                if not pedido or pedido.get('cliente_id') != usuario['id']:
                    print("Pedido não encontrado ou não pertence a você.")
                    continue
                # Pergunta ao usuário se quer o histórico completo ou apenas o último registro
                escolha = input("Mostrar histórico completo? (s/N): ").strip().lower()
                if escolha == 's':
                    hist = rastreamento.historico(pid_i)
                    if not hist:
                        print("Nenhum registro de rastreio encontrado para esse pedido.")
                    else:
                        for h in hist:
                            print(f"  [{h['atualizado_em']}] {h['localizacao']} — {h['status']}")
                else:
                    ultimo = rastreamento.ultimo(pid_i)
                    if not ultimo:
                        print("Nenhum registro de rastreio encontrado para esse pedido.")
                    else:
                        h = ultimo
                        print(f"  [{h['atualizado_em']}] {h['localizacao']} — {h['status']}")
        elif op == "0":
            break