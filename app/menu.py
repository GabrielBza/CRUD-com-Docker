from crud_Aluno import menu_aluno
from crud_Disciplina import menu_disciplina
from crud_Professor import menu_professor
from crud_Prova import menu_prova
from crud_Realizacao import menu_realizacao

def menu_principal():
    while True:
        print("\n==== MENU PRINCIPAL ====")
        print("1. Gerenciar Alunos")
        print("2. Gerenciar Professores")
        print("3. Gerenciar Disciplinas")
        print("4. Gerenciar Provas")
        print("5. Gerenciar Realizações")
        print("6. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            menu_aluno()
        elif opcao == '2':
            menu_professor()
        elif opcao == '3':
            menu_disciplina()
        elif opcao == '4':
            menu_prova()
        elif opcao == '5':
            menu_realizacao()
        elif opcao == '6':
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu_principal()