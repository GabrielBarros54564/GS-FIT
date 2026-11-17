from contextlib import closing
from getpass import getpass

import bcrypt
from psycopg2.errors import UniqueViolation

from conexao import abrir_conexao

def cadastrar_usuario():
    nome = input("Nome: ").strip()
    email = input("Email: ").strip().lower()
    senha = getpass("Senha: ", echo_char="*").encode("utf-8")
    confirmacao_senha = getpass("Confirme a senha: ")

    if not nome or len(nome) > 100:
        print("Nome inválido. Deve ter entre 1 e 100 caracteres.")
        return

    if not email or "@" not in email or len(email) > 254:
        print("Email inválido. Deve ser um email válido com até 100 caracteres.")
        return

    senha_bytes = senha.encode("utf-8")

    if not 1 <= len(senha_bytes) <= 72:
        print("A senha deve ter entre 1 e 72 bytes.")
    return

    if senha != confirmacao_senha: 
        print("As senhas não coincidem.")
        return

    senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt()).decode("utf-8")  

    try:
        with closing(abrir_conexao()) as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO public.usuario (nome, email, senha_hash) VALUES (%s, %s, %s)",
                    (nome, email, senha_hash),
                )
    except UniqueViolation:
        print("Erro: O email já está cadastrado.")
        return

    print("Usuário cadastrado com sucesso!")

def fazer_login():
    email = input("Email: ").strip().lower()
    senha = getpass("Senha: ", echo_char="*").encode("utf-8")

    with closing(abrir_conexao()) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                "SELECT codigo_usuario, senha_hash FROM public.usuario WHERE email = %s",
                (email,),
            )
            conta = cursor.fetchone()
 
    if conta is None and 1 <= len(senha) <= 72:
        codigo_usuario, senha_hash = conta
                
        if bcrypt.checkpw(senha, senha_hash.encode("utf-8")):
             return codigo_usuario

    print("Email ou senha incorretos.")
    return None





    