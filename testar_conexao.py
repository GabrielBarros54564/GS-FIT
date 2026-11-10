import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()
conexao = psycopg2.connect(os.environ["DATABASE_URL"], connect_timeout=5)

try:
    with conexao.cursor() as cursor:
        cursor.execute("SELECT current_database(), current_user")
        banco, usuario = cursor.fetchone()
        print(f"Conectado ao banco {banco} como {usuario}")
        cursor.execute("SELECT codigo_aluno, nome FROM public.aluno ORDER BY nome")
        print("Alunos:", cursor.fetchall())
finally:
    conexao.close()