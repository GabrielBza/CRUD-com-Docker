from db import conectar
from datetime import datetime

def menu():
    print("\n==== GERENCIAMENTO DE NOTAS ====")
    print("1. Cadastrar realização")
    print("2. Atualizar nota")
    print("3. Listar notas por disciplina")
    print("4. Remover nota")
    print("5. Sair")

def main():
    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_nota()
        elif opcao == '2':
            atualizar_nota()
        elif opcao == '3':
            listar_notas()
        elif opcao == '4':
            remover_nota()
        elif opcao == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


def cadastrar_nota():
    try:
        matricula = input("Matrícula do Aluno: ")
        prova_id = input("ID da Prova: ")
        data_str = input("Data da realização (AAAA-MM-DD): ")

        try:
            data = datetime.strptime(data_str, "%Y-%m-%d").date()
        except ValueError:
            print("Data inválida. Use o formato AAAA-MM-DD.")
            return

        nota_str = input("Nota obtida (opcional, pressione Enter para deixar em branco): ")
        nota = float(nota_str) if nota_str.strip() != '' else None

        conn = conectar()
        cur = conn.cursor()

        if nota is not None:
            cur.execute("""
                INSERT INTO Realizacao (fk_Aluno_matricula, fk_Prova_id, data, nota_obtida)
                VALUES (%s, %s, %s, %s)
            """, (matricula, prova_id, data, nota))
        else:
            cur.execute("""
                INSERT INTO Realizacao (fk_Aluno_matricula, fk_Prova_id, data)
                VALUES (%s, %s, %s)
            """, (matricula, prova_id, data))

        conn.commit()
        print("Realização cadastrada com sucesso!")

    except Exception as e:
        print(f"Erro ao cadastrar realização: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()


def atualizar_nota():
    try:
        matricula = input("Matrícula do aluno: ")
        prova_id = input("ID da prova: ")
        nova_nota = float(input("Nova nota: "))

        conn = conectar()
        cur = conn.cursor()

        cur.execute("""
            SELECT * FROM Realizacao
            WHERE fk_Aluno_matricula = %s AND fk_Prova_id = %s
        """, (matricula, prova_id))

        if cur.fetchone() is None:
            print("Nota não encontrada para esse aluno e prova.")
            return

        cur.execute("""
            UPDATE Realizacao
            SET nota_obtida = %s
            WHERE fk_Aluno_matricula = %s AND fk_Prova_id = %s
        """, (nova_nota, matricula, prova_id))

        conn.commit()
        print("Nota atualizada com sucesso!")

    except Exception as e:
        print(f"Erro ao atualizar nota: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()


def listar_notas():
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                a.nome AS aluno,
                d.nome AS disciplina,
                r.data,
                COALESCE(TO_CHAR(r.nota_obtida, 'FM999.0'), 'Nota pendente') AS nota
            FROM Realizacao r
            JOIN Aluno a ON r.fk_Aluno_matricula = a.matricula
            JOIN Prova p ON r.fk_Prova_id = p.id
            JOIN Disciplina d ON p.fk_Disciplina_id = d.id
            ORDER BY a.nome, d.nome;
        """)

        resultados = cursor.fetchall()

        print("\nNotas dos alunos:")
        for aluno, disciplina, data, nota in resultados:
            print(f"Aluno: {aluno}, Disciplina: {disciplina}, Data: {data}, Nota: {nota}")

    except Exception as e:
        print("Erro ao consultar as notas:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def remover_nota():
    try:
        matricula = input("Matrícula do aluno: ")
        prova_id = input("ID da prova: ")

        conn = conectar()
        cur = conn.cursor()

        cur.execute("""
            SELECT * FROM Realizacao
            WHERE fk_Aluno_matricula = %s AND fk_Prova_id = %s
        """, (matricula, prova_id))

        if cur.fetchone() is None:
            print("Nota não encontrada para esse aluno e prova.")
            return

        cur.execute("""
            DELETE FROM Realizacao
            WHERE fk_Aluno_matricula = %s AND fk_Prova_id = %s
        """, (matricula, prova_id))

        conn.commit()
        print("Nota removida com sucesso!")

    except Exception as e:
        print(f"Erro ao remover nota: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()


if __name__ == "__main__":
    main()
