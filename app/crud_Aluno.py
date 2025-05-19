from datetime import datetime
from db import conectar


def menu_aluno():
    while True:
        print("\n==== MENU - ALUNO ====")
        print("1. Adicionar aluno")
        print("2. Editar aluno")
        print("3. Excluir aluno")
        print("4. Visualizar aluno por matrícula")
        print("5. Listar todos os alunos")
        print("6. Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            adicionar_aluno()
        elif opcao == '2':
            editar_aluno()
        elif opcao == '3':
            excluir_aluno()
        elif opcao == '4':
            visualizar_aluno()
        elif opcao == '5':
            listar_alunos()
        elif opcao == '6':
            break
        else:
            print("Opção inválida.")


def adicionar_aluno():
    try:
        matricula = input("Matrícula do aluno: ")
        nome = input("Nome completo: ")
        telefone = input("Telefone: ")
        data_str = input("Data de nascimento (AAAA-MM-DD): ")
        data_nascimento = datetime.strptime(data_str, "%Y-%m-%d").date()

        conn = conectar()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO Aluno (matricula, nome, telefone, data_nascimento)
            VALUES (%s, %s, %s, %s)
        """, (matricula, nome, telefone, data_nascimento))

        conn.commit()
        print("Aluno cadastrado com sucesso!")

    except Exception as e:
        print(f"Erro ao cadastrar aluno: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()

def editar_aluno():
    try:
        matricula = input("Matrícula do aluno a editar: ")

        conn = conectar()
        cur = conn.cursor()

        cur.execute("SELECT * FROM Aluno WHERE matricula = %s", (matricula,))
        if cur.fetchone() is None:
            print("Aluno não encontrado.")
            return

        nome = input("Novo nome: ")
        telefone = input("Novo telefone: ")
        data_str = input("Nova data de nascimento (AAAA-MM-DD): ")
        data_nascimento = datetime.strptime(data_str, "%Y-%m-%d").date()

        cur.execute("""
            UPDATE Aluno
            SET nome = %s, telefone = %s, data_nascimento = %s
            WHERE matricula = %s
        """, (nome, telefone, data_nascimento, matricula))

        conn.commit()
        print("Aluno atualizado com sucesso!")

    except Exception as e:
        print(f"Erro ao editar aluno: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()

def excluir_aluno():
    try:
        matricula = input("Matrícula do aluno a excluir: ")

        conn = conectar()
        cur = conn.cursor()

        cur.execute("SELECT * FROM Aluno WHERE matricula = %s", (matricula,))
        if cur.fetchone() is None:
            print("Aluno não encontrado.")
            return

        cur.execute("DELETE FROM Aluno WHERE matricula = %s", (matricula,))
        conn.commit()
        print("Aluno excluído com sucesso!")

    except Exception as e:
        print(f"Erro ao excluir aluno: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()

def visualizar_aluno():
    try:
        matricula = input("Matrícula do aluno: ")

        conn = conectar()
        cur = conn.cursor()

        cur.execute("SELECT * FROM Aluno WHERE matricula = %s", (matricula,))
        aluno = cur.fetchone()

        if aluno:
            print(f"Matrícula: {aluno[0]}, Nome: {aluno[1]}, Telefone: {aluno[2]}, Nascimento: {aluno[3]}")
        else:
            print("Aluno não encontrado.")

    except Exception as e:
        print(f"Erro ao consultar aluno: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()

def listar_alunos():
    try:
        conn = conectar()
        cur = conn.cursor()

        cur.execute("SELECT * FROM Aluno ORDER BY matricula")
        alunos = cur.fetchall()

        print("\nAlunos cadastrados:")
        for a in alunos:
            print(f"Matrícula: {a[0]}, Nome: {a[1]}, Telefone: {a[2]}, Nascimento: {a[3]}")

    except Exception as e:
        print(f"Erro ao listar alunos: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()