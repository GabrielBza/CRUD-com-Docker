from datetime import datetime
from db import conectar

def menu_professor():
    while True:
        print("\n==== MENU - PROFESSOR ====")
        print("1. Adicionar professor(a)")
        print("2. Editar professor(a)")
        print("3. Excluir professor(a)")
        print("4. Visualizar professor(a) por id")
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

        input("Aperte Enter para continuar")

def adicionar_professor():
    try:
        # Recebe os dados do novo professor
        nome = input("Nome do(a) professor(a): ")
        formacao = input("Formação: ")

        # Cria a conexão com o BD e o cursor
        conn = conectar()
        cur = conn.cursor()

        # Executa o INSERT
        cur.execute("""
            INSERT INTO Professor (nome, formacao)
            VALUES (%s, %s)
        """, (nome, formacao))

        # Realiza o commit, finalizando a operação
        conn.commit()
        print("Professor(a) cadastrado(a) com sucesso!")

    except Exception as e:
        print(f"Erro ao cadastrar professor(a): {e}")

    finally:
        if conn:
            # Fecha conexão com o BD e o cursor
            cur.close()
            conn.close()

def editar_professor():
    try:
        # Pega o id do professor 
        id_prof = input("ID do(a) professor(a) a editar: ")
        
        # Cria conexão com o BD e cursor
        conn = conectar()
        cur = conn.cursor()

        # Verifica se existe o registro daquele professor no BD
        cur.execute("SELECT * FROM Professor WHERE id = %s", (id_prof,))
        if cur.fetchone() is None:
            print("Professor(a) não encontrado.")
            return

        # Pega os novos dados do professor
        nome = input("Novo nome: ")
        formacao = input("Nova formação: ")

        # Atualiza os dados do professor
        cur.execute("""
            UPDATE Professor
            SET nome = %s, formacao = %s
            WHERE id = %s
        """, (nome, formacao, id_prof))

        # Commita as alterações e encerra a operação
        conn.commit()
        print("Professor(a) atualizado(a) com sucesso!")

    except Exception as e:
        print(f"Erro ao editar professor(a): {e}")

    finally:
        if conn:
            # Fecha conexão com o BD e cursor
            cur.close()
            conn.close()

def excluir_professor():
    try:
        # Pega o id do professor 
        id_prof = input("ID do(a) professor(a) a excluir: ")

        # Cria conexão com o BD e cursor
        conn = conectar()
        cur = conn.cursor()

        # Verifica se o Professor está registrado no sistema
        cur.execute("SELECT * FROM Professor WHERE id = %s", (id_prof,))
        if cur.fetchone() is None:
            print("Professor(a) não encontrado.")
            return

        # Deleta o professor e commita a alteração
        cur.execute("DELETE FROM Professor WHERE id = %s", (id_prof,))
        conn.commit()
        print("Professor(a) excluído(a) com sucesso!")

    except Exception as e:
        print(f"Erro ao excluir professor(a): {e}")

    finally:
        if conn:
            # Fecha a conexão com o BD e o cursor
            cur.close()
            conn.close()

def visualizar_professor():
    try:
        # Pega o ID do professor
        id_prof = input("ID do(a) professor(a): ")

        # Cria conexão com o BD ecursor
        conn = conectar()
        cur = conn.cursor()

        # Busca o professor no BD
        cur.execute("SELECT * FROM Professor WHERE id = %s", (id_prof,))
        prof = cur.fetchone()

        if prof:
            print(f"ID: {prof[0]}, Nome: {prof[1]}, Formação: {prof[2]}")
        else:
            print("Professor(a) não encontrado.")

    except Exception as e:
        print(f"Erro ao consultar professor(a): {e}")

    finally:
        if conn:
            # Fecha a conexão com o BD e o cursor
            cur.close()
            conn.close()

def listar_professores():
    try:
        # Cria conexão com o BD e cursor
        conn = conectar()
        cur = conn.cursor()

        # Busca os professores
        cur.execute("SELECT * FROM Professor ORDER BY id")
        profs = cur.fetchall()

        print("\nProfessores cadastrados:")
        for p in profs:
            print(f"ID: {p[0]}, Nome: {p[1]}, Formação: {p[2]}")

    except Exception as e:
        print(f"Erro ao listar professores: {e}")

    finally:
        if conn:
            # Fecha conexão com o BD e cursor
            cur.close()
            conn.close()