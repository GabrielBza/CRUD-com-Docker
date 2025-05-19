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

        input("Aperte Enter para continuar")


def adicionar_disciplina():
    try:
        # Recebe os dados do usuário
        nome = input("Nome da disciplina: ")
        descricao = input("Descrição: ")
        id_professor = input("ID do professor responsável: ")

        # Abre a conexão com o BD e cria o cursor
        conn = conectar()
        cur = conn.cursor()

        # Executa o comando passando os dados da nova disciplina
        cur.execute("""
            INSERT INTO Disciplina (nome, descricao, fk_Professor_id)
            VALUES (%s, %s, %s)
        """, (nome, descricao, id_professor))

        # Commita, finalizando a operação
        conn.commit()
        print("Disciplina cadastrada com sucesso!")

    except Exception as e:
        print(f"Erro ao cadastrar disciplina: {e}")

    finally:
        if conn:
            # Fecha conexão e cursor
            cur.close()
            conn.close()

def editar_disciplina():
    try:
        # Pega o id da disciplina inserido pelo usuário
        id_disc = input("ID da disciplina a editar: ")

        # Inicia conexão com o BD e o cursor
        conn = conectar()
        cur = conn.cursor()

        # Executa um select e verifica se a disciplina foi retornada nele
        cur.execute("SELECT * FROM Disciplina WHERE id = %s", (id_disc,))
        if cur.fetchone() is None:
            print("Disciplina não encontrada.")
            return

        # Pega os novos dados da disciplina
        nome = input("Novo nome: ")
        descricao = input("Nova descrição: ")
        id_professor = input("Novo ID do professor responsável: ")

        # Executa um UPDATE com os novos dados
        cur.execute("""
            UPDATE Disciplina
            SET nome = %s, descricao = %s, fk_Professor_id = %s
            WHERE id = %s
        """, (nome, descricao, id_professor, id_disc))

        # Commita as modificações e encerra a operação
        conn.commit()
        print("Disciplina atualizada com sucesso!")

    except Exception as e:
        print(f"Erro ao editar disciplina: {e}")

    finally:
        if conn:
            # Encerra a conexão com o BD e o cursor
            cur.close()
            conn.close()

def excluir_disciplina():
    try:
        # Pega do usuário o id da disciplina
        id_disc = input("ID da disciplina a excluir: ")

        # Conecta ao BD e cria o cursor
        conn = conectar()
        cur = conn.cursor()

        # Executa um select para ver se a disciplina foi encontrada
        cur.execute("SELECT * FROM Disciplina WHERE id = %s", (id_disc,))
        if cur.fetchone() is None:
            print("Disciplina não encontrada.")
            return

        # Realiza a operação de deleção e commita, finalizando a operação
        cur.execute("DELETE FROM Disciplina WHERE id = %s", (id_disc,))
        conn.commit()
        print("Disciplina excluída com sucesso!")

    except Exception as e:
        print(f"Erro ao excluir disciplina: {e}")

    finally:
        if conn:
            # Encerra a conexão com o BD e o cursor
            cur.close()
            conn.close()

def visualizar_disciplina():
    try:
        # Pega o id inserido pelo usuário
        id_disc = input("ID da disciplina: ")

        # Conecta ao BD e cria o cursor
        conn = conectar()
        cur = conn.cursor()

        # Executa o SELECT buscando a disciplina
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
            # Encerra a conexão com o BD e o cursor
            cur.close()
            conn.close()

def listar_disciplinas():
    try:
        # Conecta com o BD e cria cursor
        conn = conectar()
        cur = conn.cursor()

        # Executa o SELECT para pegar as disciplinas
        cur.execute("""
            SELECT d.id, d.nome, d.descricao, p.nome
            FROM Disciplina d
            JOIN Professor p ON d.fk_Professor_id = p.id
            ORDER BY d.id
        """)
        
        # Salva as disciplinas
        disciplinas = cur.fetchall()

        print("\nDisciplinas cadastradas:")
        for d in disciplinas:
            print(f"ID: {d[0]}, Nome: {d[1]}, Descrição: {d[2]}, Professor: {d[3]}")

    except Exception as e:
        print(f"Erro ao listar disciplinas: {e}")

    finally:
        if conn:
            # Fecha a conexão e o cursor
            cur.close()
            conn.close()

def listar_disciplinas_por_professor():
    try:
        # Pega o id do professor inserido pelo usuário
        id_professor = input("ID do professor: ")

        # Conecta ao BD e cria o cursor
        conn = conectar()
        cur = conn.cursor()

        # Pega o nome do professor
        cur.execute("""
            SELECT nome
            FROM Professor
            WHERE id = %s
        """, (id_professor,))
        
        professor_nome = cur.fetchone()
        
        if professor_nome is None:
            print("Professor não encontrado.")
            return

        # Executa um Select buscando todas as disciplinas que o professor com o id fornecido ministra
        cur.execute("""
            SELECT d.id, d.nome, d.descricao
            FROM Disciplina d
            WHERE d.fk_Professor_id = %s
            ORDER BY d.id
        """, (id_professor,))

        disciplinas = cur.fetchall()

        if disciplinas:
            for d in disciplinas:
                print(f"\nDisciplinas do(a) Professor(a) {professor_nome[0]}:")
                print(f"ID: {d[0]}, Nome: {d[1]}, Descrição: {d[2]}")
        else:
            print(f"Nenhuma disciplina encontrada para o(a) Professor(a) {professor_nome[0]}.")

    except Exception as e:
        print(f"Erro ao listar disciplinas: {e}")

    finally:
        if conn:
            # Fecha cursor e conexão
            cur.close()
            conn.close()
