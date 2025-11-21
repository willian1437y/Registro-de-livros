import csv
import os
from datetime import datetime, timedelta
#to do
"""
- entrega de livro

"""

def registroLivro():
    """
    DESC: Solciita e guarda as informações do livro fornecidas pelo usuário e guarda no arquivo registro.csv
    ARGS: Não possui Argumentos.
    RETURN: Não retorna nada.
    """

    print("\n---INFORMAÇÕES DO LIVRO---")
    livro = input("Nome do livro: ")
    autor = input("Nome do autor: ")
    codLivro = input("Código do livro: ")
    data = datetime.today().strftime("%d/%m/%Y %H:%M:%S")

    with open("livros.csv", mode="a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)

        if arquivo.tell() == 0:
            escritor.writerow(["livro", "autor", "Código do Livro", "Data de Registro"])
        escritor.writerow([livro, autor, codLivro, data])

    print("---REGISTRO CONCLUÍDO---")


def apagarLivro():
    """
    DESC: Imprime ao usuário TODOS os livros registrados no csv, e solicita ao usuário o DELETE de todas as informações
    de um livro específico, fornecidos por ele mesmo. Caso o código que queira excluir seja DIFERENTE do que está no 
    CSV, ele irá armazenar este valor em uma varíavel. Caso o código que queira excluir seja o mesmo de um já registrado
    no .CSV, então será feito o DELETE com sucesso.
    """

    arquivo = 'livros.csv'
    if os.path.exists(arquivo):
        with open(arquivo, mode='r', encoding="utf-8") as f:
            linhas = f.readlines()

            print("\n---LIVROS REGISTRADOS---")
            print(f"{'Livro':<30} {'Autor':<30} {'Código do Livro':<20} {'Data de Registro':<20}")
            print("-" * 100)
            for linha in linhas[1:]:
                dados = linha.strip().split(",")
                print(f"{dados[0]:<30} {dados[1]:<30} {dados[2]:<20} {dados[3]:<20}")

            codigoExcluir = input("\nDigite o código do livro que deseja apagar: ").strip()

            novas_linhas = [linhas[0]]
            for linha in linhas[1:]:
                dados = linha.strip().split(",")
                if dados[2] != codigoExcluir:
                    novas_linhas.append(linha)

            if len(novas_linhas) > 1:
                with open(arquivo, mode='w', encoding="utf-8") as f:
                    f.writelines(novas_linhas)
                print("---REGISTRO APAGADO COM SUCESSO---")
            else:
                print("Código não encontrado ou livro já foi apagado.")

def editarLivro():
    """
    DESC: Irá ser mostrado na tela todos as informações dos livros que estão registrados no .CSV, será pedido o código
    do livro a ser digitado para o usuário,
    """

    arquivo = 'livros.csv'
    if os.path.exists(arquivo):
        with open(arquivo, mode='r', encoding="utf-8") as f:
            linhas = f.readlines()
            
            print("\n---LIVROS REGISTRADOS---")
            print(f"{'Livro':<30} {'Autor':<30} {'Código do Livro':<20} {'Data de Registro':<20}")
            print("-" * 100)
            for linha in linhas[1:]:
                ##Nomes genericos para dados de multiplos bancos, faz com que fique confuso de qual banco de dados esta sendo retirado a informação

                dados = linha.strip().split(",")
                print(f"{dados[0]:<30} {dados[1]:<30} {dados[2]:<20} {dados[3]:<20}")

            codigoEditar = input("\nDigite o código do livro que deseja editar: ").strip()
            novas_linhas = []
            encontrado = False

            for linha in linhas:
                aux = linha.strip().split(",")
                if aux[2] == codigoEditar:
                    encontrado = True
                    print("\n---EDITANDO REGISTRO---")
                    novo_nome = input(f"Novo nome do livro ({aux[0]}): ") or aux[0]
                    novo_autor = input(f"Novo autor ({aux[1]}): ") or aux[1]
                    nova_data = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
                    novas_linhas.append(f"{novo_nome},{novo_autor},{codigoEditar},{nova_data}\n")
                else:
                    novas_linhas.append(linha)

            if not encontrado:
                print("Código não encontrado.")
            else:
                with open(arquivo, mode='w', encoding="utf-8") as f:
                    f.writelines(novas_linhas)
                print("---REGISTRO EDITADO COM SUCESSO---")


def emprestarLivro():

    """//*
    Desc: Empresta um livro para um usuario

    ///*"""

    print("\n---EMPRÉSTIMO DE LIVRO---")

    exibirLivros() ##Exibe os livres disponiveis


    nome = input("\nNome completo: ")
    cpf = input("CPF: ")
    celular = input("Celular para contato: ")
    codLivro = input("Código do livro: ")

    data_emprestimo = datetime.today().strftime("%d/%m/%Y %H:%M:%S")

    livro_existe = False #aqui cria o livro falso pra checar se existe na biblioteca

    with open("livros.csv", mode="r", encoding="utf-8") as f:
        linhas = f.readlines()
        for linha in linhas[1:]:
            dados = linha.strip().split(",")
            if dados[2] == codLivro:
                livro_existe = True
                break

    if not livro_existe:
        print("Código do livro não encontrado.")
        return

    if not os.path.exists("registros.csv"):
        with open("registros.csv", mode="w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(["Nome", "CPF", "Celular", "Código do Livro", "Data de Empréstimo"])

    with open("registros.csv", mode="a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow([nome, cpf, celular, codLivro, data_emprestimo])

    print("---EMPRÉSTIMO REGISTRADO COM SUCESSO---")


def excluiEmprestimo():
    '''
    DESC:
    exclui um emprestimo
    '''

    exibirEmprestimos() #Exibe livres emprestados

    codLivro = input("Código do livro: ")
    nome = input("Nome completo: ")

    livro_emprestado = False #Cria emprestimo falso para checar se emprestimo esta disponivel
    with open("registros.csv", mode="r", encoding="utf-8") as f:
        linhas = f.readlines()
        for linha in linhas[1:]:
            dados = linha.strip().split(",")
            if dados[3] == codLivro and dados[0] == nome:
                livro_emprestado = True
                break

    if not livro_emprestado:
        print("O livro não foi emprestado ou o nome não corresponde.")
        return

    novas_linhas = [] #cria novas linhas no arquivo registro.csv
    with open("registros.csv", mode="r", encoding="utf-8") as f:
        linhas = f.readlines()
        for linha in linhas:
            if not (linha.strip().split(",")[3] == codLivro and linha.strip().split(",")[0] == nome):
                novas_linhas.append(linha)

    with open("registros.csv", mode="w", encoding="utf-8") as f:
        f.writelines(novas_linhas)

    print("---LIVRO EXCLUÍDO COM SUCESSO---")


def exibirLivros():
    arquivo = 'livros.csv'
    if os.path.exists(arquivo):
        with open(arquivo, mode='r', encoding="utf-8") as f:
            linhas = f.readlines()

            print("\n---LIVROS DISPONÍVEIS---\n")
            print(f"{'Livro':<30} {'Autor':<30} {'Código do Livro':<20} {'Data de Registro':<20}")
            print("-" * 100)
            for linha in linhas[1:]:
                dados = linha.strip().split(",")
                print(f"{dados[0]:<30} {dados[1]:<30} {dados[2]:<20} {dados[3]:<20}")


def exibirEmprestimos():
    arquivo = 'registros.csv'
    if os.path.exists(arquivo):
        with open(arquivo, mode='r', encoding="utf-8") as f:
            linhas = f.readlines()

            print("\n---EMPRÉSTIMOS REGISTRADOS---")
            print(f"{'Nome':<40} {'CPF':<15} {'Celular':<15} {'Código do Livro':<20} {'Data de Empréstimo':<20} {'Data de Vencimento':<20}")
            print("-" * 140)
            for linha in linhas[1:]:
                dados = linha.strip().split(",")
                data_emprestimo = datetime.strptime(dados[4], "%d/%m/%Y %H:%M:%S")
                data_vencimento = data_emprestimo + timedelta(days=7)  # Vencimento em 7 dias
                print(f"{dados[0]:<40} {dados[1]:<15} {dados[2]:<15} {dados[3]:<20} {dados[4]:<20} {data_vencimento.strftime('%d/%m/%Y %H:%M:%S'):<20}")


def entregaLivros():
    """
    DESC:
    FUNÇÃO USADA PARA O USUARIO ENTREGAR LIVROS
    """
    arquivo = 'registros.csv' #registros.csv é um arquivo 
    if os.path.exists(arquivo):
        with open(arquivo, mode='r', encoding="utf-8") as f:
            linhas = f.readlines()
            

            print("\n---EMPRÉSTIMOS REGISTRADOS---")
            print(
                f"{'Nome':<40} {'CPF':<15} {'Celular':<15} {'Código do Livro':<20} {'Data de Empréstimo':<20} {'Data de Vencimento':<20}")
            print("-" * 140)
            for linha in linhas[1:]:
                dados = linha.strip().split(",")
                data_emprestimo = datetime.strptime(dados[4], "%d/%m/%Y %H:%M:%S")
                data_vencimento = data_emprestimo + timedelta(days=7)
                print(
                    f"{dados[0]:<40} {dados[1]:<15} {dados[2]:<15} {dados[3]:<20} {dados[4]:<20} {data_vencimento.strftime('%d/%m/%Y %H:%M:%S'):<20}")



def mostrarMenu():
    while True:
        opcao = int(input("\n OPÇÃO 1 == REGISTRAR LIVRO \n OPÇÃO 2 == EDITAR LIVROS \n OPÇÃO 3 == EXCLUIR LIVRO\n OPÇÃO 4 == VISUALIZAR LIVROS \n OPÇÃO 5 == EMPRÉSTIMO DE LIVRO \n OPÇÃO 6 == EXCLUIR EMPRÉSTIMO\n OPÇÃO 7 == VISUALIZAR EMPRÉSTIMOS\n OPÇÃO 8 == ENTREGA DE LIVRO\n OPÇÃO 9 == PARAR \n\n DIGITE UMA OPÇÃO:"))

        if opcao == 1:
            registroLivro() 
        elif opcao == 2:
            editarLivro()
        elif opcao == 3:
            apagarLivro()
        elif opcao == 4:
            exibirLivros()
        elif opcao == 5:
            emprestarLivro()
        elif opcao == 6:
            excluiEmprestimo()
        elif opcao == 7:
            exibirEmprestimos()
        elif opcao == 8:
            entregaLivros()
        elif opcao == 9:
            break
        else:
            print("Opção inválida!")


mostrarMenu()
