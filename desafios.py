import textwrap
from datetime import datetime

# =================== MENU ===================
def menu():
    menu = """\n
    ================ MENU ================
    [d] Depositar
    [s] Sacar
    [t] Transferir
    [e] Extrato
    [rm] Relatório mensal
    [nc] Nova conta
    [lc] Listar contas
    [nu] Novo usuário
    [q] Sair
    => """
    return input(textwrap.dedent(menu))


# =================== DEPÓSITO ===================
def depositar(saldo, valor, extrato, /, limite_min=1, limite_max=10000):
    if valor < limite_min:
        print(f"\nOperação não realizada: depósito mínimo é R$ {limite_min:.2f}.")
    elif valor > limite_max:
        print(f"\nOperação não realizada: depósito máximo permitido é R$ {limite_max:.2f}.")
    else:
        saldo += valor
        extrato.append((datetime.now(), f"Depósito: R$ {valor:.2f}"))
        print("\nOperação concluída com sucesso.")
    return saldo, extrato


# =================== SAQUE ===================
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques, taxa=2, saque_min=10, saque_max=1000):
    excedeu_saldo = valor + taxa > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques
    abaixo_minimo = valor < saque_min
    acima_maximo = valor > saque_max

    if excedeu_saldo:
        print("\nOperação não realizada: saldo insuficiente.")
    elif excedeu_limite:
        print(f"\nOperação não realizada: limite de saque é R$ {limite:.2f}.")
    elif excedeu_saques:
        print("\nOperação não realizada: número máximo de saques atingido.")
    elif abaixo_minimo:
        print(f"\nOperação não realizada: saque mínimo é R$ {saque_min:.2f}.")
    elif acima_maximo:
        print(f"\nOperação não realizada: saque máximo permitido é R$ {saque_max:.2f}.")
    else:
        saldo -= (valor + taxa)
        extrato.append((datetime.now(), f"Saque: R$ {valor:.2f} (Taxa: R$ {taxa:.2f})"))
        numero_saques += 1
        print("\nOperação concluída com sucesso.")
    return saldo, extrato, numero_saques


# =================== TRANSFERÊNCIA ===================
def transferir(contas, origem, destino, valor, taxa=5):
    if origem["saldo"] < valor + taxa:
        print("\nOperação não realizada: saldo insuficiente.")
        return
    origem["saldo"] -= (valor + taxa)
    destino["saldo"] += valor
    origem["extrato"].append((datetime.now(), f"Transferência enviada: R$ {valor:.2f} (Taxa: R$ {taxa:.2f})"))
    destino["extrato"].append((datetime.now(), f"Transferência recebida: R$ {valor:.2f}"))
    print("\nTransferência concluída com sucesso.")


# =================== EXTRATO ===================
def exibir_extrato(saldo, extrato):
    print("\n================ EXTRATO ================")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        for data, mov in extrato:
            print(f"{data.strftime('%d/%m/%Y %H:%M:%S')} - {mov}")
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("==========================================")


# =================== RELATÓRIO MENSAL ===================
def relatorio_mensal(extrato):
    print("\n=========== RELATÓRIO MENSAL ===========")
    if not extrato:
        print("Nenhuma movimentação registrada.")
    else:
        for data, mov in extrato:
            if data.month == datetime.now().month:
                print(f"{data.strftime('%d/%m/%Y')} - {mov}")
    print("==========================================")


# =================== USUÁRIOS E CONTAS ===================
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nOperação não realizada: já existe usuário com esse CPF.")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("Usuário criado com sucesso.")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nConta criada com sucesso.")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario, "saldo": 0, "extrato": []}
    print("\nOperação não realizada: usuário não encontrado.")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
            Saldo:\t\tR$ {conta['saldo']:.2f}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


# =================== MAIN ===================
def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            if not contas:
                print("Nenhuma conta cadastrada.")
                continue
            conta = contas[0]  # simplificação: primeira conta
            valor = float(input("Informe o valor do depósito: "))
            conta["saldo"], conta["extrato"] = depositar(conta["saldo"], valor, conta["extrato"])

        elif opcao == "s":
            if not contas:
                print("Nenhuma conta cadastrada.")
                continue
            conta = contas[0]
            valor = float(input("Informe o valor do saque: "))
            conta["saldo"], conta["extrato"], _ = sacar(
                saldo=conta["saldo"],
                valor=valor,
                extrato=conta["extrato"],
                limite=500,
                numero_saques=0,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "t":
            if len(contas) < 2:
                print("É necessário pelo menos duas contas para transferir.")
                continue
            origem = contas[0]
            destino = contas[1]
            valor = float(input("Informe o valor da transferência: "))
            transferir(contas, origem, destino, valor)

        elif opcao == "e":
            if not contas:
                print("Nenhuma conta cadastrada.")
                continue
            exibir_extrato(contas[0]["saldo"], contas[0]["extrato"])

        elif opcao == "rm":
            if not contas:
                print("Nenhuma conta cadastrada.")
                continue
            relatorio_mensal(contas[0]["extrato"])

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()
