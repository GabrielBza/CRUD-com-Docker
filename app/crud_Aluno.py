from datetime import datetime
from db import conectar


def menu_aluno(): #Função de Menu que chamará todas as outras funções de "Aluno" e será passada pra main
    while True:
        print("\n==== MENU - ALUNO ====")
        print("1. Adicionar aluno(a)")
        print("2. Editar aluno(a)")
        print("3. Excluir aluno(a)")
        print("4. Visualizar aluno(a) por matrícula")
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


        input("Aperte Enter para continuar")


def adicionar_aluno():
    try:
        # Recebe os dados do novo aluno
        matricula = input("Matrícula do(a) aluno(a): ")
        nome = input("Nome completo: ")
        telefone = input("Telefone: ")
        data_str = input("Data de nascimento (AAAA-MM-DD): ")
        data_nascimento = datetime.strptime(data_str, "%Y-%m-%d").date()

        # Faz a conexão com o BD e cria o cursor
        conn = conectar()
        cur = conn.cursor()

        # Passa a instrução em SQL para o cursor e substitui os valores pelas informações recebidas do usuário
        cur.execute("""
            INSERT INTO Aluno (matricula, nome, telefone, data_nascimento)
            VALUES (%s, %s, %s, %s)
        """, (matricula, nome, telefone, data_nascimento))

        # Commita finalizando a operação
        conn.commit()
        print("Aluno(a) cadastrado(a) com sucesso!")

    except Exception as e:
        print(f"Erro ao cadastrar aluno(a): {e}")

    finally:
        if conn:
            # Encerra a conexão e o cursor
            cur.close()
            conn.close()

def editar_aluno():
    try:
        # Recebe a matrícula do aluno
        matricula = input("Matrícula do(a) aluno(a) a editar: ")

        # Conecta ao bd e cria o cursor
        conn = conectar()
        cur = conn.cursor()

        # Envia a consulta SQL juntamente com a matrícula para o cursor
        cur.execute("SELECT * FROM Aluno WHERE matricula = %s", (matricula,))
        if cur.fetchone() is None:
            print("Aluno(a) não encontrado.")
            return

        # Pega os dados atualizados do aluno
        nome = input("Novo nome: ")
        telefone = input("Novo telefone: ")
        data_str = input("Nova data de nascimento (AAAA-MM-DD): ")
        data_nascimento = datetime.strptime(data_str, "%Y-%m-%d").date()

        # Envia os dados novos para a atualização do aluno
        cur.execute("""
            UPDATE Aluno
            SET nome = %s, telefone = %s, data_nascimento = %s
            WHERE matricula = %s
        """, (nome, telefone, data_nascimento, matricula))

        # Commita, finalizando a operação
        conn.commit()
        print("Aluno(a) atualizado(a) com sucesso!")

    except Exception as e:
        print(f"Erro ao editar aluno(a): {e}")

    finally:
        if conn:
            # Fecha o cursor e a conexão
            cur.close()
            conn.close()

def excluir_aluno():
    try:
        # Pega a referência de id do aluno 
        matricula = input("Matrícula do(a) aluno(a) a excluir: ")

        # Cria a conexão com o BD e o cursor
        conn = conectar()
        cur = conn.cursor()

        # Verifica se o aluno está registrado
        cur.execute("SELECT * FROM Aluno WHERE matricula = %s", (matricula,))
        if cur.fetchone() is None:
            print("Aluno(a) não encontrado.")
            return

        # Deleta o aluno passando sua patrícula
        cur.execute("DELETE FROM Aluno WHERE matricula = %s", (matricula,))
        conn.commit()
        print("Aluno(a) excluído com sucesso!")

    except Exception as e:
        print(f"Erro ao excluir aluno(a): {e}")

    # Fecha a conexão e o cursor
    finally:
        if conn:
            cur.close()
            conn.close()

def visualizar_aluno():
    try:
        # Pega a matrícula do aluno
        matricula = input("Matrícula do(a) aluno(a): ")

        # Cria a conexão com o BD e o cursor
        conn = conectar()
        cur = conn.cursor()

        # Verifica se o aluno existe
        cur.execute("SELECT * FROM Aluno WHERE matricula = %s", (matricula,))
        aluno = cur.fetchone()

        # Printa as informações do aluno ou informa que ele não foi encontrado
        if aluno:
            print(f"Matrícula: {aluno[0]}, Nome: {aluno[1]}, Telefone: {aluno[2]}, Nascimento: {aluno[3]}")
        else:
            print("Aluno(a) não encontrado.")

    except Exception as e:
        print(f"Erro ao consultar aluno(a): {e}")

    finally:
        if conn:
            # Fecha conexão com o BD e cursor
            cur.close()
            conn.close()

def listar_alunos():
    try:
        # Conecta ao BD e cria cursor
        conn = conectar()
        cur = conn.cursor()

        # Manda a consulta pro BD
        cur.execute("SELECT * FROM Aluno ORDER BY matricula")
        alunos = cur.fetchall()

        #Printa os alunos 
        print("\nAlunos(as) cadastrados(as):")
        for a in alunos:
            print(f"Matrícula: {a[0]}, Nome: {a[1]}, Telefone: {a[2]}, Nascimento: {a[3]}")

    except Exception as e:
        print(f"Erro ao listar alunos(as): {e}")

    finally:
        if conn:
            # Fecha a conexão
            cur.close()
            conn.close()