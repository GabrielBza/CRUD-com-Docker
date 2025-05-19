from datetime import datetime
from db import conectar

def menu_realizacao():
    while True:
        print("\n==== MENU - REALIZAÇÔES ====")
        print("1. Adicionar Realização")
        print("2. Editar Nota")
        print("3. Excluir Realização")
        print("4. Listar realizações por aluno")
        print("5. Listar todas as realizações")
        print("6. Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            adicionar_realizacao()
        elif opcao == '2':
            editar_nota_realizacao()
        elif opcao == '3':
            excluir_realizacao()
        elif opcao == '4':
            listar_realizacoes_por_aluno()
        elif opcao == '5':
            listar_todas_realizacoes()
        elif opcao == '6':
            break
        else:
            print("Opção inválida.")

        input("Aperte Enter para continuar")


def adicionar_realizacao():
    try:
        # Pega os dados da nova realização
        aluno = input("Matrícula do(a) aluno(a): ")
        prova = input("ID da prova: ")
        data_str = input("Data (AAAA-MM-DD): ")
        nota_str = input("Nota (opcional): ")

        data = datetime.strptime(data_str, "%Y-%m-%d").date()
        nota = float(nota_str) if nota_str.strip() != '' else None

        # Cria a conexão com o BD e o cursor
        conn = conectar()
        cur = conn.cursor()

        # Insere o registro da realização
        if nota is not None:
            cur.execute("""
                INSERT INTO Realizacao (fk_Prova_id, fk_Aluno_matricula, data, nota_obtida)
                VALUES (%s, %s, %s, %s)
            """, (prova, aluno, data, nota))
        else:
            cur.execute("""
                INSERT INTO Realizacao (fk_Prova_id, fk_Aluno_matricula, data)
                VALUES (%s, %s, %s)
            """, (prova, aluno, data))

        # Commita e finaliza a operação
        conn.commit()
        print("Realização registrada com sucesso!")

    except Exception as e:
        print(f"Erro ao adicionar realização: {e}")

    finally:
        if conn:
            # Fecha a conexão e cursor
            cur.close()
            conn.close()

def editar_nota_realizacao():
    try:
        # Pega os dados do aluno e do id da prova juntamente com a nova nota
        aluno = input("Matrícula do(a) aluno(a): ")
        prova = input("ID da prova: ")
        nova_nota = float(input("Nova nota: "))

        # Conecta ao BD e cria o cursor
        conn = conectar()
        cur = conn.cursor()

        # Realiza a atualização e commita as mudanças
        cur.execute("""
            UPDATE Realizacao
            SET nota_obtida = %s
            WHERE fk_Aluno_matricula = %s AND fk_Prova_id = %s
        """, (nova_nota, aluno, prova))

        conn.commit()
        print("Nota atualizada com sucesso!")

    except Exception as e:
        print(f"Erro ao editar nota: {e}")

    finally:
        if conn:
            # Fecha a conexão e o cursor
            cur.close()
            conn.close()

def excluir_realizacao():
    try:
        aluno = input("Matrícula do aluno: ")
        prova = input("ID da prova: ")

        conn = conectar()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM Realizacao
            WHERE fk_Aluno_matricula = %s AND fk_Prova_id = %s
        """, (aluno, prova))

        conn.commit()
        print("Realização excluída com sucesso!")

    except Exception as e:
        print(f"Erro ao excluir realização: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()

def listar_todas_realizacoes():
    try:
        conn = conectar()
        cur = conn.cursor()

        cur.execute("""
            SELECT r.id, a.nome, p.id, d.nome, r.data, r.nota_obtida
            FROM Realizacao r
            JOIN Aluno a ON r.fk_Aluno_matricula = a.matricula
            JOIN Prova p ON r.fk_Prova_id = p.id
            JOIN Disciplina d ON p.fk_Disciplina_id = d.id
            ORDER BY r.data;
        """)

        resultados = cur.fetchall()

        print("\nRealizações registradas:")
        for r in resultados:
            print(f"ID: {r[0]}, Aluno: {r[1]}, Prova: {r[2]}, Disciplina: {r[3]}, Data: {r[4]}, Nota: {r[5]}")
    except Exception as e:
        print("Erro ao listar realizações:", e)

    finally:
        if conn:
            cur.close()
            conn.close()

def listar_realizacoes_por_aluno():
    try:
        matricula = input("Digite a matrícula do aluno: ")

        conn = conectar()
        cur = conn.cursor()

        # Buscar o nome do aluno
        cur.execute("""
            SELECT nome
            FROM Aluno
            WHERE matricula = %s
        """, (matricula,))

        aluno_nome = cur.fetchone()

        if aluno_nome is None:
            print("Aluno não encontrado.")
            return

        # Agora, buscar as realizações associadas ao aluno
        cur.execute("""
            SELECT d.nome AS disciplina, p.tipo, r.data, r.nota_obtida
            FROM Realizacao r
            JOIN Prova p ON r.fk_Prova_id = p.id
            JOIN Disciplina d ON p.fk_Disciplina_id = d.id
            WHERE r.fk_Aluno_matricula = %s
            ORDER BY r.data;
        """, (matricula,))

        realizacoes = cur.fetchall()

        # Exibir as realizações do aluno
        print(f"\nRealizações do(a) aluno(a) {aluno_nome[0]}:")
        if realizacoes:
            for r in realizacoes:
                print(f"Disciplina: {r[0]}, Tipo: {r[1]}, Data: {r[2]}, Nota: {r[3]}")
        else:
            print("Nenhuma realização encontrada para este aluno.")

    except Exception as e:
        print(f"Erro ao listar realizações: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()
