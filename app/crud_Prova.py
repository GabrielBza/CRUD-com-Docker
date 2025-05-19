from datetime import datetime
from db import conectar

def menu_prova():
    while True:
        print("\n==== MENU - PROVA ====")
        print("1. Adicionar prova")
        print("2. Editar prova")
        print("3. Excluir prova")
        print("4. Visualizar prova por id")
        print("5. Listar provas por professor")
        print("6. Listar provas por disciplina")
        print("7. Listar todas as provas")
        print("8. Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            adicionar_prova()
        elif opcao == '2':
            editar_prova()
        elif opcao == '3':
            excluir_prova()
        elif opcao == '4':
            listar_prova_por_id()
        elif opcao == '5':
            listar_provas_por_professor()
        elif opcao == '6':
            listar_provas_por_disciplina()
        elif opcao == '7':
            listar_todas_as_provas()
        elif opcao == '8':
            break
        else:
            print("Opção inválida.")

def adicionar_prova():
    try:
        nota_max = int(input("Nota máxima: "))
        qtd_questoes = int(input("Quantidade de questões: "))
        data_str = input("Data de criação (AAAA-MM-DD): ")
        tipo = input("Tipo (Objetiva, Dissertativa, Mista): ")
        professor_id = input("ID do professor: ")
        disciplina_id = input("ID da disciplina: ")

        data_criacao = datetime.strptime(data_str, "%Y-%m-%d").date()

        conn = conectar()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO Prova (nota_max, qtd_questoes, data_criacao, tipo, fk_Professor_id, fk_Disciplina_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nota_max, qtd_questoes, data_criacao, tipo, professor_id, disciplina_id))

        conn.commit()
        print("Prova cadastrada com sucesso!")

    except Exception as e:
        print(f"Erro ao cadastrar prova: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()


def editar_prova():
    try:
        id_prova = input("ID da prova a editar: ")

        nota_max = int(input("Nova nota máxima: "))
        qtd_questoes = int(input("Nova quantidade de questões: "))
        data_str = input("Nova data de criação (AAAA-MM-DD): ")
        tipo = input("Novo tipo: ")
        professor_id = input("Novo ID do professor: ")
        disciplina_id = input("Novo ID da disciplina: ")

        data_criacao = datetime.strptime(data_str, "%Y-%m-%d").date()

        conn = conectar()
        cur = conn.cursor()

        cur.execute("""
            UPDATE Prova
            SET nota_max = %s, qtd_questoes = %s, data_criacao = %s, tipo = %s,
                fk_Professor_id = %s, fk_Disciplina_id = %s
            WHERE id = %s
        """, (nota_max, qtd_questoes, data_criacao, tipo, professor_id, disciplina_id, id_prova))

        conn.commit()
        print("Prova atualizada com sucesso!")

    except Exception as e:
        print(f"Erro ao editar prova: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()


def excluir_prova():
    try:
        id_prova = input("ID da prova a excluir: ")

        conn = conectar()
        cur = conn.cursor()

        cur.execute("DELETE FROM Prova WHERE id = %s", (id_prova,))
        conn.commit()
        print("Prova excluída com sucesso!")

    except Exception as e:
        print(f"Erro ao excluir prova: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()


def listar_todas_as_provas():
    try:
        conn = conectar()
        cur = conn.cursor()

        cur.execute("""
            SELECT p.id, p.tipo, p.data_criacao, p.nota_max, d.nome AS disciplina, pr.nome AS professor
            FROM Prova p
            JOIN Disciplina d ON p.fk_Disciplina_id = d.id
            JOIN Professor pr ON p.fk_Professor_id = pr.id
            ORDER BY p.id
        """)

        provas = cur.fetchall()

        print("\nProvas cadastradas:")
        for p in provas:
            print(f"ID: {p[0]}, Tipo: {p[1]}, Data: {p[2]}, Nota Máx: {p[3]}, Disciplina: {p[4]}, Professor: {p[5]}")

    except Exception as e:
        print(f"Erro ao listar provas: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()


def listar_provas_por_professor():
    try:
        id_professor = input("ID do professor: ")

        conn = conectar()
        cur = conn.cursor()

        cur.execute("""
            SELECT p.id, p.tipo, p.data_criacao, p.nota_max, d.nome
            FROM Prova p
            JOIN Disciplina d ON p.fk_Disciplina_id = d.id
            WHERE p.fk_Professor_id = %s
            ORDER BY p.id
        """, (id_professor,))

        provas = cur.fetchall()

        print(f"\nProvas do professor {id_professor}:")
        for p in provas:
            print(f"ID: {p[0]}, Tipo: {p[1]}, Data: {p[2]}, Nota Máx: {p[3]}, Disciplina: {p[4]}")

    except Exception as e:
        print(f"Erro ao listar provas: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()


def listar_prova_por_id():
    try:
        id_prova = input("ID da prova: ")

        conn = conectar()
        cur = conn.cursor()

        cur.execute("""
            SELECT p.id, p.tipo, p.data_criacao, p.nota_max, d.nome, pr.nome
            FROM Prova p
            JOIN Disciplina d ON p.fk_Disciplina_id = d.id
            JOIN Professor pr ON p.fk_Professor_id = pr.id
            WHERE p.id = %s
        """, (id_prova,))

        p = cur.fetchone()

        if p:
            print(f"\nID: {p[0]}, Tipo: {p[1]}, Data: {p[2]}, Nota Máx: {p[3]}, Disciplina: {p[4]}, Professor: {p[5]}")
        else:
            print("Prova não encontrada.")

    except Exception as e:
        print(f"Erro ao buscar prova: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()


def listar_provas_por_disciplina():
    try:
        id_disc = input("ID da disciplina: ")

        conn = conectar()
        cur = conn.cursor()

        cur.execute("""
            SELECT p.id, p.tipo, p.data_criacao, p.nota_max, pr.nome
            FROM Prova p
            JOIN Professor pr ON p.fk_Professor_id = pr.id
            WHERE p.fk_Disciplina_id = %s
            ORDER BY p.id
        """, (id_disc,))

        provas = cur.fetchall()

        print(f"\nProvas da disciplina {id_disc}:")
        for p in provas:
            print(f"ID: {p[0]}, Tipo: {p[1]}, Data: {p[2]}, Nota Máx: {p[3]}, Professor: {p[4]}")

    except Exception as e:
        print(f"Erro ao listar provas: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()
