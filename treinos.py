import psycopg2

from conexao import abrir_conexao


def cadastrar_treino(codigo_usuario):
    print("\n--- CADASTRAR TREINO ---")
    descricao = input("Descrição: ").strip()
    objetivo = input("Objetivo: ").strip()

    try:
        duracao = int(input("Duração (em minutos): ").strip())
        codigo_aluno = int(input("Código do aluno: ").strip())
        codigo_instrutor = int(input("Código do instrutor: ").strip())
    except ValueError:
        print("Duração e códigos devem ser números inteiros.")
        return

    if not descricao or not objetivo or len(objetivo) > 50:
        print("Informe a descrição e um objetivo de até 50 caracteres.")
        return

    if duracao <= 0:
        print("A duração deve ser maior que zero.")
        return

    conn = abrir_conexao()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT codigo_aluno FROM aluno WHERE codigo_aluno = %s AND codigo_usuario = %s",
            (codigo_aluno, codigo_usuario),
        )
        if not cur.fetchone():
            print("Aluno não encontrado nesta conta.")
            return

        cur.execute(
            "SELECT codigo_instrutor FROM instrutor WHERE codigo_instrutor = %s AND codigo_usuario = %s",
            (codigo_instrutor, codigo_usuario),
        )
        if not cur.fetchone():
            print("Instrutor não encontrado nessa conta.")
            return

        sql = """
            INSERT INTO treino (descricao, objetivo, duracao_minutos, codigo_aluno, codigo_instrutor, codigo_usuario)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cur.execute(
            sql,
            (descricao, objetivo, duracao, codigo_aluno, codigo_instrutor, codigo_usuario),
            )
        conn.commit()
        print("Treino cadastrado com sucesso!")
    except psycopg2.Error:
        conn.rollback()
        print("Erro ao cadastrar treino. Confira os dados e tente novamente.")
    finally:
        cur.close()
        conn.close()

def listar_treinos(codigo_usuario):
    print("\n--- LISTA DE TREINOS ---")
    conn = abrir_conexao()
    cur = conn.cursor()
    try:
        sql = """
            SELECT t.codigo_treino, t.descricao, t.objetivo, t.duracao_minutos,
            a.nome AS nome_aluno, i.nome AS nome_instrutor
            FROM treino t
            INNER JOIN aluno a ON t.codigo_aluno = a.codigo_aluno AND a.codigo_usuario = t.codigo_usuario
            INNER JOIN instrutor i ON t.codigo_instrutor = i.codigo_instrutor AND i.codigo_usuario = t.codigo_usuario
            WHERE t.codigo_usuario = %s
            ORDER BY t.codigo_treino ASC
        """
        cur.execute(sql, (codigo_usuario,))
        treinos = cur.fetchall()

        if not treinos:
            print("Nenhum treino cadastrado nesta conta.")
            return

        for tr in treinos:
            print(
                f"Código: {tr[0]} | Descrição: {tr[1]} | Objetivo: {tr[2]} | "
                f"Duração: {tr[3]} min | Aluno: {tr[4]} | Instrutor: {tr[5]}"
            )
    except psycopg2.Error:
        print("Erro ao listar treinos. Confira os dados e tente novamente.")
    finally:
        cur.close()
        conn.close()

def menu_treinos(codigo_usuario):
    while True:
        print("\n=== MENU DE TREINOS ===")
        print("1 - Cadastrar")
        print("2 - Listar")
        print("3 - Editar")
        print("4 - Excluir")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_treino(codigo_usuario)
        elif opcao == "2":
            listar_treinos(codigo_usuario)
        elif opcao == "3":
            editar_treino(codigo_usuario)
        elif opcao == "4":
            excluir_treino(codigo_usuario)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

def editar_treino(codigo_usuario):
    print("\n--- EDITAR TREINO ---")
    try:
        codigo_treino = int(input("Digite o código do treino: ").strip())
    except ValueError:
        print("Código inválido. Digite apenas números.")
        return

    conn = abrir_conexao()
    cur = conn.cursor()
    try:
        sql_busca = """
            SELECT codigo_treino, descricao, objetivo, duracao_minutos, codigo_aluno, codigo_instrutor
            FROM treino
            WHERE codigo_treino = %s AND codigo_usuario = %s
        """
        cur.execute(sql_busca, (codigo_treino, codigo_usuario))
        treino = cur.fetchone()

        if not treino:
            print("Treino não encontrado nesta conta.")
            return

        print("Deixe em branco para manter o valor atual.")
        nova_desc = input(f"Nova descrição [{treino[1]}]: ").strip() or treino[1]
        novo_obj = input(f"Novo objetivo [{treino[2]}]: ").strip() or treino[2]

        if len(novo_obj) > 50:
            print("Informe um objetivo de até 50 caracteres.")
            return

        duracao_str = input(f"Nova duração em minutos [{treino[3]}]: ").strip()
        if duracao_str:
            try:
                nova_duracao = int(duracao_str)
            except ValueError:
                print("Duração deve ser um número inteiro.")
                return
        else:
            nova_duracao = treino[3]

        if nova_duracao <= 0:
            print("A duração deve ser maior que zero.")
            return

        aluno_str = input(f"Novo código do aluno [{treino[4]}]: ").strip()
        if aluno_str:
            try:
                novo_aluno = int(aluno_str)
            except ValueError:
                print("Código do aluno deve ser um número inteiro.")
                return
        else:
            novo_aluno = treino[4]

        instrutor_str = input(f"Novo código do instrutor [{treino[5]}]: ").strip()
        if instrutor_str:
            try:
                novo_instrutor = int(instrutor_str)
            except ValueError:
                print("Código do instrutor deve ser um número inteiro.")
                return
        else:
            novo_instrutor = treino[5]

        cur.execute(
            "SELECT codigo_aluno FROM aluno WHERE codigo_aluno = %s AND codigo_usuario = %s",
            (novo_aluno, codigo_usuario),
        )
        if not cur.fetchone():
            print("Aluno não encontrado nesta conta.")
            return

        cur.execute(
            "SELECT codigo_instrutor FROM instrutor WHERE codigo_instrutor = %s AND codigo_usuario = %s",
            (novo_instrutor, codigo_usuario),
        )
        if not cur.fetchone():
            print("Instrutor não encontrado nesta conta.")
            return

        sql_update = """
            UPDATE treino
            SET descricao = %s, objetivo = %s, duracao_minutos = %s,
                codigo_aluno = %s, codigo_instrutor = %s
            WHERE codigo_treino = %s AND codigo_usuario = %s
        """
        cur.execute(
            sql_update,
            (nova_desc, novo_obj, nova_duracao, novo_aluno, novo_instrutor, codigo_treino, codigo_usuario),
        )
        conn.commit()
        print("Treino atualizado com sucesso!" if cur.rowcount else "Registro não encontrado nesta conta.")
    except psycopg2.Error:
        conn.rollback()
        print("Erro ao editar treino. Confira os dados e tente novamente.")
    finally:
        cur.close()
        conn.close()

def excluir_treino(codigo_usuario):
    print("\n--- EXCLUIR TREINO ---")
    try:
        codigo_treino = int(input("Digite o código do treino: ").strip())
    except ValueError:
        print("Código inválido. Digite apenas números.")
        return

    conn = abrir_conexao()
    cur = conn.cursor()
    try:
        sql_busca = """
            SELECT codigo_treino
            FROM treino
            WHERE codigo_treino = %s AND codigo_usuario = %s
        """
        cur.execute(sql_busca, (codigo_treino, codigo_usuario))
        if not cur.fetchone():
            print("Treino não encontrado nesta conta.")
            return

        sql_delete = """
            DELETE FROM treino
            WHERE codigo_treino = %s AND codigo_usuario = %s
        """
        cur.execute(sql_delete, (codigo_treino, codigo_usuario))
        conn.commit()
        print("Treino excluído com sucesso!" if cur.rowcount else "Registro não encontrado nesta conta.")
    except psycopg2.Error:
        conn.rollback()
        print("Erro ao excluir treino. Confira os dados e tente novamente.")
    finally:
        cur.close()
        conn.close()
