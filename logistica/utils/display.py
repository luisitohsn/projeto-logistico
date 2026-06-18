from rich.console import Console
from rich.table import Table

console = Console()

def tabela_pedidos(lista: list[dict]):
    """Exibe lista de pedidos em tabela formatada no terminal."""
    t = Table(title="Pedidos", show_lines=True)
    for col in ["ID", "Descrição", "Origem", "Destino", "Status"]:
        t.add_column(col)
    for p in lista:
        t.add_row(
            str(p["id"]), p["descricao"],
            p["origem"], p["destino"], p["status"]
        )
    console.print(t)

def tabela_veiculos(lista: list[dict]):
    """Exibe frota de veículos em tabela formatada."""
    t = Table(title="Veículos", show_lines=True)
    for col in ["ID", "Placa", "Motorista", "Status"]:
        t.add_column(col)
    for v in lista:
        t.add_row(str(v["id"]), v["placa"], v["motorista"], v["status"])
    console.print(t)