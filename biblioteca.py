import csv
import os
from datetime import datetime, timedelta

ARQ_LIVROS = "livros.csv"
ARQ_REGISTROS = "registros.csv"

def carregarLivrosEmprestados():
    """Retorna um conjunto com os códigos de livros que estão atualmente emprestados."""
    emprestados = set()

    if os.path.exists(ARQ_REGISTROS):
        with open(ARQ_REGISTROS, mode='r', encoding="utf-8", newline="") as f:
            leitor = list(csv.reader(f))

        for linha in leitor[1:]:
            while len(linha) < 7:
                linha.append("")

            cod = linha[3].strip()
            entregue = linha[5].strip().lower()

            if entregue == "nao":
                emprestados.add(cod)

    return emprestados


def registroLivro():
    print("\n---INFORMAÇÕES DO LIVRO---")
    livro = input("Nome do livro: ")
    autor = input("Nome do autor: ")
    codLivro = input("Código do livro: ")
    data = datetime.today().strftime("%d/%m/%Y %H:%M:%S")

    file_exists = os.path.exists(ARQ_LIVROS)
    with open(ARQ_LIVROS, mode="a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        if not file_exists or os.stat(ARQ_LIVROS).st_size == 0:
            escritor.writerow(["livro", "autor", "Código do Livro", "Data de Registro"])
        escritor.writerow([livro, autor, codLivro, data])

    print("---REGISTRO CONCLUÍDO---")


def apagarLivro():
    arquivo = ARQ_LIVROS
    if not os.path.exists(arquivo):
        print("Nenhum arquivo de livros encontrado.")
        return

    with open(arquivo, mode='r', encoding="utf-8", newline="") as f:
        leitor = list(csv.reader(f))
    if len(leitor) <= 1:
        print("Nenhum livro registrado.")
        return

    print("\n---LIVROS REGISTRADOS---")
    print(f"{'Livro':<30} {'Autor':<30} {'Código do Livro':<20} {'Data de Registro':<20}")
    print("-" * 100)
    for linha in leitor[1:]:
        while len(linha) < 4:
            linha.append("")
        print(f"{linha[0]:<30} {linha[1]:<30} {linha[2]:<20} {linha[3]:<20}")

    codigoExcluir = input("\nDigite o código do livro que deseja apagar: ").strip()

    novas_linhas = [leitor[0]]
    encontrado = False
    for linha in leitor[1:]:
        while len(linha) < 4:
            linha.append("")
        if linha[2] != codigoExcluir:
            novas_linhas.append(linha)
        else:
            encontrado = True

    if not encontrado:
        print("Código não encontrado ou livro já foi apagado.")
        return

    with open(arquivo, mode='w', encoding="utf-8", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerows(novas_linhas)

    print("---REGISTRO APAGADO COM SUCESSO---")


def editarLivro():
    arquivo = ARQ_LIVROS
    if not os.path.exists(arquivo):
        print("Nenhum arquivo de livros encontrado.")
        return

    with open(arquivo, mode='r', encoding="utf-8", newline="") as f:
        leitor = list(csv.reader(f))
    if len(leitor) <= 1:
        print("Nenhum livro registrado.")
        return

    print("\n---LIVROS REGISTRADOS---")
    print(f"{'Livro':<30} {'Autor':<30} {'Código do Livro':<20} {'Data de Registro':<20}")
    print("-" * 100)
    for linha in leitor[1:]:
        while len(linha) < 4:
            linha.append("")
        print(f"{linha[0]:<30} {linha[1]:<30} {linha[2]:<20} {linha[3]:<20}")

    codigoEditar = input("\nDigite o código do livro que deseja editar: ").strip()
    novas_linhas = []
    encontrado = False

    for linha in leitor:
        while len(linha) < 4:
            linha.append("")
        if linha[2] == codigoEditar:
            encontrado = True
            print("\n---EDITANDO REGISTRO---")
            novo_nome = input(f"Novo nome do livro ({linha[0]}): ") or linha[0]
            novo_autor = input(f"Novo autor ({linha[1]}): ") or linha[1]
            nova_data = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
            novas_linhas.append([novo_nome, novo_autor, codigoEditar, nova_data])
        else:
            novas_linhas.append(linha)

    if not encontrado:
        print("Código não encontrado.")
        return

    with open(arquivo, mode='w', encoding="utf-8", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerows(novas_linhas)

    print("---REGISTRO EDITADO COM SUCESSO---")


def exibirLivros():
    arquivo = ARQ_LIVROS
    if not os.path.exists(arquivo):
        print("\nNenhum arquivo de livros encontrado.")
        return

    emprestados = carregarLivrosEmprestados()

    with open(arquivo, mode='r', encoding="utf-8", newline="") as f:
        leitor = list(csv.reader(f))
    if len(leitor) <= 1:
        print("\nNenhum livro cadastrado.")
        return

    print("\n---LIVROS DISPONÍVEIS---\n")
    print(f"{'Livro':<30} {'Autor':<30} {'Código do Livro':<20} {'Data de Registro':<20}")
    print("-" * 100)

    for linha in leitor[1:]:
        while len(linha) < 4:
            linha.append("")
        if linha[2] not in emprestados:
            print(f"{linha[0]:<30} {linha[1]:<30} {linha[2]:<20} {linha[3]:<20}")


def emprestarLivro():
    print("\n---EMPRÉSTIMO DE LIVRO---")

    exibirLivros()

    nome = input("\nNome completo: ")
    cpf = input("CPF: ")
    celular = input("Celular para contato: ")
    codLivro = input("Código do livro: ")
    data_emprestimo = datetime.today().strftime("%d/%m/%Y %H:%M:%S")

    emprestados = carregarLivrosEmprestados()
    if codLivro in emprestados:
        print("Esse livro está emprestado no momento.")
        return

    # valida se o livro existe
    livro_existe = False
    if os.path.exists(ARQ_LIVROS):
        with open(ARQ_LIVROS, mode="r", encoding="utf-8", newline="") as f:
            leitor = list(csv.reader(f))
            for linha in leitor[1:]:
                while len(linha) < 4:
                    linha.append("")
                if linha[2] == codLivro:
                    livro_existe = True
                    break

    if not livro_existe:
        print("Código do livro não encontrado.")
        return

    file_exists = os.path.exists(ARQ_REGISTROS)
    if not file_exists or os.stat(ARQ_REGISTROS).st_size == 0:
        with open(ARQ_REGISTROS, mode="w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(["Nome", "CPF", "Celular", "Código do Livro", "Data de Empréstimo", "Entregue", "Data de Entrega"])

    with open(ARQ_REGISTROS, mode="a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow([nome, cpf, celular, codLivro, data_emprestimo, "nao", ""])

    print("---EMPRÉSTIMO REGISTRADO COM SUCESSO---")


def excluiEmprestimo():
    arquivo = ARQ_REGISTROS
    if not os.path.exists(arquivo):
        print("Nenhum registro de empréstimo encontrado.")
        return

    exibirEmprestimos()

    codLivro = input("Código do livro: ").strip()
    nome = input("Nome completo: ").strip()

    with open(arquivo, mode='r', encoding="utf-8", newline="") as f:
        leitor = list(csv.reader(f))

    if len(leitor) <= 1:
        print("Nenhum empréstimo para excluir.")
        return

    header = leitor[0]
    novas = [header]
    removido = False

    for linha in leitor[1:]:
        while len(linha) < 7:
            linha.append("")
        row_nome = linha[0].strip()
        row_cod = linha[3].strip() if len(linha) > 3 else ""
        if not (row_cod == codLivro and row_nome.lower() == nome.lower()):
            novas.append(linha)
        else:
            removido = True

    if not removido:
        print("Registro não encontrado (verifique nome e código).")
        return

    with open(arquivo, mode='w', encoding="utf-8", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerows(novas)

    print("---EMPRÉSTIMO EXCLUÍDO COM SUCESSO---")


def exibirEmprestimos():
    arquivo = ARQ_REGISTROS
    if not os.path.exists(arquivo):
        print("\nNenhum empréstimo registrado.")
        return

    with open(arquivo, mode='r', encoding="utf-8", newline="") as f:
        leitor = list(csv.reader(f))

    if len(leitor) <= 1:
        print("\nNenhum empréstimo registrado.")
        return

    print("\n---EMPRÉSTIMOS REGISTRADOS---")
    print(f"{'Nome':<30} {'CPF':<15} {'Celular':<15} {'Código do Livro':<15} {'Data Empr.':<20} {'Entregue':<8} {'Data Entrega':<20} {'Status':<20}")
    print("-" * 150)

    agora = datetime.today()
    for linha in leitor[1:]:

        while len(linha) < 7:
            linha.append("")

        nome, cpf, celular, codigo, data_emp_str, entregue, data_ent_str = linha

        entregue_txt = "Sim" if entregue.lower() == "sim" else "Não"

        try:
            data_emp = datetime.strptime(data_emp_str, "%d/%m/%Y %H:%M:%S")
        except:
            try:
                data_emp = datetime.strptime(data_emp_str, "%d/%m/%Y")
            except:
                data_emp = None

        data_ent = None
        if data_ent_str and data_ent_str.strip():
            try:
                data_ent = datetime.strptime(data_ent_str, "%d/%m/%Y %H:%M:%S")
            except:
                try:
                    data_ent = datetime.strptime(data_ent_str, "%d/%m/%Y")
                except:
                    data_ent = None

        if data_emp:
            vencimento = data_emp + timedelta(days=7)
        else:
            vencimento = None

        if entregue.lower() == "sim":
            if data_ent and vencimento:
                if data_ent > vencimento:
                    status = "PASSOU DO PRAZO"
                else:
                    status = "ENTREGUE DENTRO DO PRAZO"
            else:
                status = "ENTREGUE (data inválida)"
        else:
            if vencimento:
                if agora > vencimento:
                    status = "ATRASADO"
                else:
                    status = "PENDENTE"
            else:
                status = "PENDENTE (data inválida)"

        data_emp_display = data_emp_str if data_emp_str else "-"
        data_ent_display = data_ent_str if data_ent_str else "-"

        print(f"{nome:<30} {cpf:<15} {celular:<15} {codigo:<15} {data_emp_display:<20} {entregue_txt:<8} {data_ent_display:<20} {status:<20}")


def entregaLivros():
    arquivo = ARQ_REGISTROS
    if not os.path.exists(arquivo):
        print("Nenhum registro de empréstimo encontrado.")
        return

    with open(arquivo, mode='r', encoding="utf-8", newline="") as f:
        leitor = list(csv.reader(f))

    if len(leitor) <= 1:
        print("Nenhum empréstimo registrado.")
        return

    print("\n---EMPRÉSTIMOS ABERTOS---")
    abertos = []
    for linha in leitor[1:]:
        while len(linha) < 7:
            linha.append("")
        if linha[5].lower() != "sim":
            abertos.append(linha)

    if not abertos:
        print("Não há empréstimos em aberto.")
        return

    for l in abertos:
        print(f"Nome: {l[0]} | Código: {l[3]} | Data Empr.: {l[4]}")

    codLivro = input("\nCódigo do livro entregue: ").strip()
    nome = input("Nome completo (do tomador): ").strip()
    data_entrega = datetime.today().strftime("%d/%m/%Y %H:%M:%S")

    encontrado = False
    for linha in leitor[1:]:
        while len(linha) < 7:
            linha.append("")
        if linha[3] == codLivro and linha[0].strip().lower() == nome.strip().lower() and linha[5].lower() != "sim":
            linha[5] = "sim"
            linha[6] = data_entrega
            encontrado = True
            break

    if not encontrado:
        print("Registro não encontrado ou já entregue.")
        return

    with open(arquivo, mode='w', encoding="utf-8", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerows(leitor)

    print("---LIVRO ENTREGUE E REGISTRO ATUALIZADO---")


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


if __name__ == "__main__":
    mostrarMenu()
