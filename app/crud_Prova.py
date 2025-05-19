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

        input("Aperte Enter para continuar")

def adicionar_prova():
    try:
        # Pega os dados da nova prova
        nota_max = int(input("Nota máxima: "))
        qtd_questoes = int(input("Quantidade de questões: "))
        data_str = input("Data de criação (AAAA-MM-DD): ")
        tipo = input("Tipo (Objetiva, Dissertativa, Mista): ")
        professor_id = input("ID do(a) professor(a): ")
        disciplina_id = input("ID da disciplina: ")

        data_criacao = datetime.strptime(data_str, "%Y-%m-%d").date()

        # Conecta ao BD e cria cursor
        conn = conectar()
        cur = conn.cursor()

        # Faz a inserção do novo registro
        cur.execute("""
            INSERT INTO Prova (nota_max, qtd_questoes, data_criacao, tipo, fk_Professor_id, fk_Disciplina_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nota_max, qtd_questoes, data_criacao, tipo, professor_id, disciplina_id))

        # Commita, encerrando a operação
        conn.commit()
        print("Prova cadastrada com sucesso!")

    except Exception as e:
        print(f"Erro ao cadastrar prova: {e}")

    finally:
        if conn:
            # Encerra conexão com o BD e cursor
            cur.close()
            conn.close()


def editar_prova():
    try:
        # Pega o id da prova a ser editada
        id_prova = input("ID da prova a editar: ")

        # Pega os novos dados da prova
        nota_max = int(input("Nova nota máxima: "))
        qtd_questoes = int(input("Nova quantidade de questões: "))
        data_str = input("Nova data de criação (AAAA-MM-DD): ")
        tipo = input("Novo tipo: ")
        professor_id = input("Novo ID do(a) professor(a): ")
        disciplina_id = input("Novo ID da disciplina: ")

        data_criacao = datetime.strptime(data_str, "%Y-%m-%d").date()

        # Cria conexão com o BD e cursor
        conn = conectar()
        cur = conn.cursor()

        # Realiza as mudanças no registro da prova
        cur.execute("""
            UPDATE Prova
            SET nota_max = %s, qtd_questoes = %s, data_criacao = %s, tipo = %s,
                fk_Professor_id = %s, fk_Disciplina_id = %s
            WHERE id = %s
        """, (nota_max, qtd_questoes, data_criacao, tipo, professor_id, disciplina_id, id_prova))

        # Commita as mudanças e encerra a operação
        conn.commit()
        print("Prova atualizada com sucesso!")

    except Exception as e:
        print(f"Erro ao editar prova: {e}")

    finally:
        if conn:
            # Encerra conexão com o BD e cursor
            cur.close()
            conn.close()


def excluir_prova():
    try:
        # Pega o id da prova a ser excluída
        id_prova = input("ID da prova a excluir: ")

        # Cria conexão com o BD e cria o cursor
        conn = conectar()
        cur = conn.cursor()

        # Verifica se a prova existe no banco
        cur.execute("SELECT * FROM Prova WHERE id = %s", (id_prova,))
        if cur.fetchone() is None:
            print("Prova não encontrada.")
            return

        # Deleta a prova
        cur.execute("DELETE FROM Prova WHERE id = %s", (id_prova,))
        conn.commit()
        print("Prova excluída com sucesso!")

    except Exception as e:
        print(f"Erro ao excluir prova: {e}")

    finally:
        if conn:
            # Finaliza a conexão com o BD e o cursor
            cur.close()
            conn.close()


def listar_todas_as_provas():
    try:
        # Conecta ao Bd e cria cursor
        conn = conectar()
        cur = conn.cursor()

        # Pega dos os registros de prova
        cur.execute("""
            SELECT p.id, p.tipo, p.data_criacao, p.nota_max, d.nome AS disciplina, pr.nome AS professor
            FROM Prova p
            JOIN Disciplina d ON p.fk_Disciplina_id = d.id
            JOIN Professor pr ON p.fk_Professor_id = pr.id
            ORDER BY p.id
        """)

        # Salva todos os registros
        provas = cur.fetchall()

        print("\nProvas cadastradas:")
        for p in provas:
            print(f"ID: {p[0]}, Tipo: {p[1]}, Data: {p[2]}, Nota Máx: {p[3]}, Disciplina: {p[4]}, Professor: {p[5]}")

    except Exception as e:
        print(f"Erro ao listar provas: {e}")

    finally:
        if conn:
            # Finaliza conexão com o BD e cursor
            cur.close()
            conn.close()


def listar_provas_por_professor():
    try:
        # Pega o id do professor
        id_professor = input("ID do professor: ")

        # Conecta ao BD e cria cursor
        conn = conectar()
        cur = conn.cursor()

        # Pega o nome do professor
        cur.execute("""
            SELECT nome
            FROM Professor
            WHERE id = %s
        """, (id_professor,))
        
        professor_nome = cur.fetchone()
        
        # Verifica se o professor existe
        if professor_nome is None:
            print("Professor(a) não encontrado.")
            return

        # Seleciona as provas que foram criadas pelo determinado professor
        cur.execute("""
            SELECT p.id, p.tipo, p.data_criacao, p.nota_max, d.nome
            FROM Prova p
            JOIN Disciplina d ON p.fk_Disciplina_id = d.id
            WHERE p.fk_Professor_id = %s
            ORDER BY p.id
        """, (id_professor,))

        provas = cur.fetchall()

        print(f"\nProvas do(a) professor(a) {professor_nome[0]}:")
        for p in provas:
            print(f"ID: {p[0]}, Tipo: {p[1]}, Data: {p[2]}, Nota Máx: {p[3]}, Disciplina: {p[4]}")

    except Exception as e:
        print(f"Erro ao listar provas: {e}")

    finally:
        if conn:
            # Encerra conexão com BD e cursor
            cur.close()
            conn.close()



def listar_prova_por_id():
    try:
        # Pega o ID da prova
        id_prova = input("ID da prova: ")

        # Conecta ao BD e cria cursor
        conn = conectar()
        cur = conn.cursor()

        # Busca a prova desejada
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
            # Encerra a conexão e o cursor
            cur.close()
            conn.close()


def listar_provas_por_disciplina():
    try:
        #Pega o Id da dsiciplina
        id_disc = input("ID da disciplina: ")

        # Faz a conexão com o BD e cria o cursor
        conn = conectar()
        cur = conn.cursor()

        # Busca o nome da disciplina
        cur.execute("""
            SELECT nome
            FROM Disciplina
            WHERE id = %s
        """, (id_disc,))
        
        disciplina_nome = cur.fetchone()

        # Verifica se a disciplina está registrada no BD
        if disciplina_nome is None:
            print("Disciplina não encontrada.")
            return

        # Seleciona as provas da determinada disciplina
        cur.execute("""
            SELECT p.id, p.tipo, p.data_criacao, p.nota_max, pr.nome
            FROM Prova p
            JOIN Professor pr ON p.fk_Professor_id = pr.id
            WHERE p.fk_Disciplina_id = %s
            ORDER BY p.id
        """, (id_disc,))

        provas = cur.fetchall()

        print(f"\nProvas da disciplina {disciplina_nome[0]}:")
        for p in provas:
            print(f"ID: {p[0]}, Tipo: {p[1]}, Data: {p[2]}, Nota Máx: {p[3]}, Professor: {p[4]}")

    except Exception as e:
        print(f"Erro ao listar provas: {e}")

    finally:
        if conn:
            # Finaliza conexão e cursor
            cur.close()
            conn.close()