from contextlib import closing
from datetime import date

from psycopg2.errors import ForeignKeyViolation, UniqueViolation

from conexao import abrir_conexao


def validar_cpf(cpf):
    if len(cpf) != 11 or not cpf.isascii() or not cpf.isdigit():
        return False

    if cpf == cpf[0] * 11:
        return False

    for posicao in (9, 10):
        soma = 0
        for indice in range(posicao):
            peso = posicao + 1 - indice
            soma += int(cpf[indice]) * peso

        resto = soma % 11
        digito_esperado = 0 if resto < 2 else 11 - resto

        if int(cpf[posicao]) != digito_esperado:
            return False

    return True


def ler_dados_aluno():
    nome = input("Nome: ").strip()
    cpf = input("CPF (com 11 digitos): ").strip()
    telefone = input("Telefone (com DDD): ").strip()
    nacimento_str = input("Data de nascimento (AAAA-MM-DD): ").strip()
    endereco = input("Endereço: ").strip()

    if not nome or len(nome) > 100:
        print("Nome inválido. Deve ter entre 1 e 100 caracteres.")
        return None

    if not validar_cpf(cpf):
        print("CPF inválido. Confira os 11 dígitos e digite sem pontos ou traço.")
        return None

    if not telefone or len(telefone) > 20:
        print("Telefone inválido. Deve ter entre 1 e 20 caracteres.")
        return None

    if not endereco or len(endereco) > 200:
        print("Endereço inválido. Deve ter entre 1 e 200 caracteres.")
        return None

    try:
        data_nascimento = date.fromisoformat(nacimento_str)
    except ValueError:
        print("Data de nascimento inválida. Use o formato AAAA-MM-DD.")
        return None

    return nome, cpf, telefone, data_nascimento, endereco

def ler_codigo_aluno():
    try:
        codigo_aluno = int(input("Código do aluno: "))
        if codigo_aluno > 0:
            return codigo_aluno
    except ValueError:
        pass

    print("Código inválido. Deve ser um número inteiro positivo.")
    return None

def cadastrar_aluno(codigo_usuario):
    dados_aluno = ler_dados_aluno()
    if dados_aluno is None:
        return

    try:
        with closing(abrir_conexao()) as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(
                     """
                    INSERT INTO aluno
                        (nome, cpf, telefone, data_nascimento, endereco, codigo_usuario)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING codigo_aluno
                    """,
                    (*dados_aluno, codigo_usuario),
                )
                codigo_aluno = cursor.fetchone()[0]
    except UniqueViolation:
        print("Erro: O CPF já está cadastrado.")
        return

    print(f"Aluno cadastrado com sucesso! Código do aluno: {codigo_aluno}")

def listar_alunos(codigo_usuario, termo=""):
    with closing(abrir_conexao()) as conexao:
        with closing(conexao.cursor()) as cursor:
            cursor.execute(
                """
                SELECT codigo_aluno, nome, telefone
                FROM aluno
                WHERE codigo_usuario = %s
                  AND LOWER(nome) LIKE LOWER(%s)
                ORDER BY nome, codigo_aluno
                """,
                (codigo_usuario, f"%{termo}%"),
            )
            alunos = cursor.fetchall()
    if not alunos:
        print("Nenhum aluno encontrado.")
        return

    for codigo_aluno, nome, telefone in alunos:
        print(f"Código: {codigo_aluno}, Nome: {nome}, Telefone: {telefone}")

def editar_aluno(codigo_usuario):
    codigo_aluno = ler_codigo_aluno()
    if codigo_aluno is None:
        return

    print("Digite os dados completos do aluno para atualizar.")
    dados_aluno = ler_dados_aluno()
    if dados_aluno is None:
        return

    try:
        with closing(abrir_conexao()) as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(
                       """
                    UPDATE aluno
                    SET nome = %s, cpf = %s, telefone = %s,
                        data_nascimento = %s, endereco = %s
                    WHERE codigo_aluno = %s AND codigo_usuario = %s
                    """,
                    (*dados_aluno, codigo_aluno, codigo_usuario),
                )
                alterados = cursor.rowcount
    except UniqueViolation:
        print("Erro: O CPF já está cadastrado.")
        return  

    print("aluno atualizado com sucesso!" if alterados else "Aluno não encontrado ou sem permissão para editar.")

def excluir_aluno(codigo_usuario):
    codigo_aluno = ler_codigo_aluno()
    if codigo_aluno is None:
        return

    resposta = input(f"Tem certeza que deseja excluir o aluno {codigo_aluno}? (s/n): ").strip().lower()
    if resposta != "s":
        print("Exclusão cancelada.")
        return

    try:
        with closing(abrir_conexao()) as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(
                      """
                    DELETE FROM aluno
                    WHERE codigo_aluno = %s AND codigo_usuario = %s
                    """,
                    (codigo_aluno, codigo_usuario),
                )
                excluidos = cursor.rowcount
    except ForeignKeyViolation:
        print("Erro: Não é possível excluir o aluno, pois existem registros dependentes.")
        return

    print("Aluno excluído com sucesso!" if excluidos else "Aluno não encontrado ou sem permissão para excluir.")

def menu_alunos(codigo_usuario):
    menu = """
╭────────────────────────────────────────╮
│               GS FIT                   │
│          Gestão de alunos              │
├────────────────────────────────────────┤
│  1. Cadastrar        4. Editar         │
│  2. Listar           5. Excluir        │
│  3. Pesquisar                          │
├────────────────────────────────────────┤
│  0. Voltar ao menu principal           │
╰────────────────────────────────────────╯"""

    while True:
        print(menu)
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            return
        elif opcao == "1":
            cadastrar_aluno(codigo_usuario)
        elif opcao == "2":
            listar_alunos(codigo_usuario)
        elif opcao == "3":
            termo = input("Digite parte do nome do aluno: ").strip()
            listar_alunos(codigo_usuario, termo)
        elif opcao == "4":
            editar_aluno(codigo_usuario)
        elif opcao == "5":
            excluir_aluno(codigo_usuario)
        else:
            print("Opção inválida. Digite um número de 0 a 5.")

        input("\nPressione Enter para voltar ao menu de alunos...")