from datetime import datetime
from db import conectar

def menu_disciplina():
    while True:
        print("\n==== MENU - DISCIPLINA ====")
        print("1. Adicionar disciplina")
        print("2. Editar disciplina")
        print("3. Excluir disciplina")
        print("4. Visualizar disciplina por ID")
        print("5. Listar disciplinas por ID do professor")
        print("6. Listar todas as disciplinas")
        print("7. Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            adicionar_disciplina()
        elif opcao == '2':
            editar_disciplina()
        elif opcao == '3':
            excluir_disciplina()
        elif opcao == '4':
            visualizar_disciplina()
        elif opcao == '5':
            listar_disciplinas_por_professor()
        elif opcao == '6':
            listar_disciplinas()
        elif opcao == '7':
            break
        else:
            print("Opção inválida. Tente novamente.")


def adicionar_disciplina():
    try:
        nome = input("Nome da disciplina: ")
        descricao = input("Descrição: ")
        id_professor = input("ID do professor responsável: ")

        conn = conectar()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO Disciplina (nome, descricao, fk_Professor_id)
            VALUES (%s, %s, %s)
        """, (nome, descricao, id_professor))

        conn.commit()
        print("Disciplina cadastrada com sucesso!")

    except Exception as e:
        print(f"Erro ao cadastrar disciplina: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()

def editar_disciplina():
    try:
        id_disc = input("ID da disciplina a editar: ")

        conn = conectar()
        cur = conn.cursor()

        cur.execute("SELECT * FROM Disciplina WHERE id = %s", (id_disc,))
        if cur.fetchone() is None:
            print("Disciplina não encontrada.")
            return

        nome = input("Novo nome: ")
        descricao = input("Nova descrição: ")
        id_professor = input("Novo ID do professor responsável: ")

        cur.execute("""
            UPDATE Disciplina
            SET nome = %s, descricao = %s, fk_Professor_id = %s
            WHERE id = %s
        """, (nome, descricao, id_professor, id_disc))

        conn.commit()
        print("Disciplina atualizada com sucesso!")

    except Exception as e:
        print(f"Erro ao editar disciplina: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()

def excluir_disciplina():
    try:
        id_disc = input("ID da disciplina a excluir: ")

        conn = conectar()
        cur = conn.cursor()

        cur.execute("SELECT * FROM Disciplina WHERE id = %s", (id_disc,))
        if cur.fetchone() is None:
            print("Disciplina não encontrada.")
            return

        cur.execute("DELETE FROM Disciplina WHERE id = %s", (id_disc,))
        conn.commit()
        print("Disciplina excluída com sucesso!")

    except Exception as e:
        print(f"Erro ao excluir disciplina: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()

def visualizar_disciplina():
    try:
        id_disc = input("ID da disciplina: ")

        conn = conectar()
        cur = conn.cursor()

        cur.execute("""
            SELECT d.id, d.nome, d.descricao, p.nome
            FROM Disciplina d
            JOIN Professor p ON d.fk_Professor_id = p.id
            WHERE d.id = %s
        """, (id_disc,))
        
        disc = cur.fetchone()

        if disc:
            print(f"ID: {disc[0]}, Nome: {disc[1]}, Descrição: {disc[2]}, Professor: {disc[3]}")
        else:
            print("Disciplina não encontrada.")

    except Exception as e:
        print(f"Erro ao consultar disciplina: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()

def listar_disciplinas():
    try:
        conn = conectar()
        cur = conn.cursor()

        cur.execute("""
            SELECT d.id, d.nome, d.descricao, p.nome
            FROM Disciplina d
            JOIN Professor p ON d.fk_Professor_id = p.id
            ORDER BY d.id
        """)
        
        disciplinas = cur.fetchall()

        print("\nDisciplinas cadastradas:")
        for d in disciplinas:
            print(f"ID: {d[0]}, Nome: {d[1]}, Descrição: {d[2]}, Professor: {d[3]}")

    except Exception as e:
        print(f"Erro ao listar disciplinas: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()

def listar_disciplinas_por_professor():
    try:
        id_professor = input("ID do professor: ")

        conn = conectar()
        cur = conn.cursor()

        cur.execute("""
            SELECT p.nome, d.id, d.nome, d.descricao
            FROM Disciplina d
            JOIN Professor p on p.id = d.fk_Professor_id
            WHERE d.fk_Professor_id = %s
            ORDER BY d.id
        """, (id_professor,))

        disciplinas = cur.fetchall()

        if disciplinas:
            for d in disciplinas:
                print(f"\nDisciplinas do(a) Professor(a) {d[0]}:")
                print(f"ID: {d[1]}, Nome: {d[2]}, Descrição: {d[3]}")
        else:
            print("Nenhuma disciplina encontrada para este professor.")

    except Exception as e:
        print(f"Erro ao listar disciplinas: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()