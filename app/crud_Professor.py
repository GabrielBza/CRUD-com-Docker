from datetime import datetime
from db import conectar

def menu_professor():
    while True:
        print("\n==== MENU - PROFESSOR ====")
        print("1. Adicionar professor")
        print("2. Editar professor")
        print("3. Excluir professor")
        print("4. Visualizar professor por id")
        print("5. Listar todos os professores")
        print("6. Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            adicionar_professor()
        elif opcao == '2':
            editar_professor()
        elif opcao == '3':
            excluir_professor()
        elif opcao == '4':
            visualizar_professor()
        elif opcao == '5':
            listar_professores()
        elif opcao == '6':
            break
        else:
            print("Opção inválida.")

def adicionar_professor():
    try:
        nome = input("Nome do professor: ")
        formacao = input("Formação: ")

        conn = conectar()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO Professor (nome, formacao)
            VALUES (%s, %s)
        """, (nome, formacao))

        conn.commit()
        print("Professor cadastrado com sucesso!")

    except Exception as e:
        print(f"Erro ao cadastrar professor: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()

def editar_professor():
    try:
        id_prof = input("ID do professor a editar: ")

        conn = conectar()
        cur = conn.cursor()

        cur.execute("SELECT * FROM Professor WHERE id = %s", (id_prof,))
        if cur.fetchone() is None:
            print("Professor não encontrado.")
            return

        nome = input("Novo nome: ")
        formacao = input("Nova formação: ")

        cur.execute("""
            UPDATE Professor
            SET nome = %s, formacao = %s
            WHERE id = %s
        """, (nome, formacao, id_prof))

        conn.commit()
        print("Professor atualizado com sucesso!")

    except Exception as e:
        print(f"Erro ao editar professor: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()

def excluir_professor():
    try:
        id_prof = input("ID do professor a excluir: ")

        conn = conectar()
        cur = conn.cursor()

        cur.execute("SELECT * FROM Professor WHERE id = %s", (id_prof,))
        if cur.fetchone() is None:
            print("Professor não encontrado.")
            return

        cur.execute("DELETE FROM Professor WHERE id = %s", (id_prof,))
        conn.commit()
        print("Professor excluído com sucesso!")

    except Exception as e:
        print(f"Erro ao excluir professor: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()

def visualizar_professor():
    try:
        id_prof = input("ID do professor: ")

        conn = conectar()
        cur = conn.cursor()

        cur.execute("SELECT * FROM Professor WHERE id = %s", (id_prof,))
        prof = cur.fetchone()

        if prof:
            print(f"ID: {prof[0]}, Nome: {prof[1]}, Formação: {prof[2]}")
        else:
            print("Professor não encontrado.")

    except Exception as e:
        print(f"Erro ao consultar professor: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()

def listar_professores():
    try:
        conn = conectar()
        cur = conn.cursor()

        cur.execute("SELECT * FROM Professor ORDER BY id")
        profs = cur.fetchall()

        print("\nProfessores cadastrados:")
        for p in profs:
            print(f"ID: {p[0]}, Nome: {p[1]}, Formação: {p[2]}")

    except Exception as e:
        print(f"Erro ao listar professores: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()