#from instrutores import menu_instrutores
#from treinos import menu_treinos

from psycopg2 import OperationalError

from alunos import menu_alunos
from usuarios import cadastrar_usuario, fazer_login


def mostrar_menu(titulo, opcoes):
    largura = 40

    print()
    print("╭" + "─" * largura + "╮")
    print(f"│{'ACADEMIA GS FIT':^{largura}}│")
    print(f"│{titulo:^{largura}}│")
    print("├" + "─" * largura + "┤")

    for opcao in opcoes:
        print(f"│  {opcao:<{largura - 2}}│")

    print("╰" + "─" * largura + "╯")


def menu_principal(codigo_usuario):
    while True:
        mostrar_menu("Menu principal", [
            "1. Alunos",
            "2. Instrutores",
            "3. Treinos",
            "0. Sair da conta",
        ])
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_alunos(codigo_usuario)
        elif opcao in ("2", "3"):
            print("Este módulo está em desenvolvimento.")
        elif opcao == "0":
            print("Você saiu da conta.")
            return
        else:
            print("Opção inválida. Digite um número de 0 a 3.")


def main():
    while True:
        mostrar_menu("Acesso ao sistema", [
            "1. Cadastrar usuário",
            "2. Entrar na conta",
            "0. Encerrar programa",
        ])
        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                cadastrar_usuario()
            elif opcao == "2":
                codigo_usuario = fazer_login()
                if codigo_usuario is not None:
                    menu_principal(codigo_usuario)
            elif opcao == "0":
                print("Programa encerrado. Até logo!")
                return
            else:
                print("Opção inválida. Digite um número de 0 a 2.")
        except OperationalError:
            print("Falha ao acessar o banco. Confira a conexão e tente novamente.")


if __name__ == "__main__":
    main()