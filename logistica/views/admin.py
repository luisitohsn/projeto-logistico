from models import pedidos, veiculos, custos
from utils.display import tabela_pedidos, tabela_veiculos

def menu(usuario: dict):
    """Exibe o menu completo para o perfil administrador."""
    while True:
        print(f"\nAdmin: {usuario['nome']}")
        print("1. Todos os pedidos")
        print("2. Frota de veículos")
        print("3. Custos e fretes")
        print("0. Sair")
        op = input("Escolha: ").strip()

        if op == "1":
            tabela_pedidos(pedidos.listar_todos())
        elif op == "2":
            tabela_veiculos(veiculos.listar_todos())
        elif op == "3":
            for c in custos.listar_todos():
                print(f"  Pedido #{c['pedido_id']} | Frete: R${c['frete']:.2f} | Total: R${c['total']:.2f}")
        elif op == "0":
            break