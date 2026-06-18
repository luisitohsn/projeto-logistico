from database import criar_tabelas
from auth import fazer_login
from views import clientes, admin

def main():
    criar_tabelas()
    print("=== Sistema de Monitoração Logística ===")

    usuario = fazer_login()
    if not usuario:
        return

    if usuario["perfil"] == "admin":
        admin.menu(usuario)
    else:
        clientes.menu(usuario)

if __name__ == "__main__":
    main()