import time

def menu():
    print ('-='*12, "Banco JBO", '-='*12 )
    print ('''-  MENU 
        [N] Novo usuário
        [V] Visualizar usuários
        [C] Criar conta
        [L] Listar contas
        [D] Depósito
        [S] Saque
        [E] Extrato
        [X] Sair ''')
    

def sacar (*, saldo, saque, extrato, lim_diario, qsaque):

    while True:
        try:   
            time.sleep(1.5)
            lim_diario += saque
            if lim_diario < 501:
                
                if saque <= 0:
                    print('Valor inválido')       
                elif saque > saldo:
                    print(f'Saldo insuficiente! O valor do seu saldo é R$ {saldo:.2f}')
                elif saque > 500:
                    print('Seu limite de saque é de R$ 500,00')
                elif qsaque > 2:
                    print('Limite de saques diário atingido')
                    break
                elif saque > 500:
                    print('Limite díario atingido')
                else:                
                    qsaque += 1 
                    saldo -= saque
                    msg = (f'Saque R$ {saque:.2f}')
                    extrato.append(msg)
                    print(f'Seu saldo atual é R$ {saldo:.2f}')
                    print('-='*30)
                    break
            elif lim_diario == 500:
                break
            else:
                lim_diario -= saque
                print('-='*30)
                print('Limite díario atingido. O limite de saque diário é de R$ 500,00! Aperte V para voltar')
                saque_rest = 500 - lim_diario
                print(f'O valor que pode ser sacado hoje é R$ {saque_rest:.2f}')
        except:
            back = input('Valor inválido. Aperte V para voltar:  ').upper()
            time.sleep(1.5)
            if back == "V":
                break
            print('-'*60)
            continue
        
        
    return saldo, extrato

def deposito(saldo, depto, extrato, /):
    while True:
        
        time.sleep(1.5)
        if depto <= 0:
            print('Valor inválido')
        else: 
            saldo += depto
            msg = (f'Depósito R$ {depto:.2f}')
            extrato.append(msg)
            print('DEPÓSITO REALIZADO COM SUCESSO!')
            time.sleep(1)
            print('. .'*30)

        print(f'Seu saldo atual é R$ {saldo:.2f}')
        print('-='*30)    
        
        return saldo, extrato  
        

def exibir_extrato(saldo, /, *, extrato):
    print('*'*15, 'EXTRATO', '*'*15)  
    print("Não foram realizadas movimentações." if not extrato else extrato)     
    for i in extrato:
        print(i)
    print(f'Seu saldo atual é R$ {saldo:.2f}')
    print('-='*30)
    time.sleep(1.5)


def novo_usuario(usuarios):
    cpf = input('Informe o CPF (somente números):')
    usuario = verificar_usuario(cpf, usuarios)

    if usuario:
        print(f'XX-- CPF já cadastrado --XX')
        time.sleep(1.5)
        return

    nome = input('Nome completo: ')
    data_nasc = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (logradouro, num - bairro - cidade/estado):")
    usuarios.append ({"nome": nome, "data_nasc": data_nasc, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")

def verificar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            return usuario
        else: 
            None            


def listar_usuarios(usuarios):
    for usuario in usuarios:
        print(usuario)

def criar_conta(agencia, num_conta, usuarios):
    cpf = input('Informe o CPF do usuário: ')
    usuario = verificar_usuario(cpf, usuarios)

    if usuario:
        print('\n -=- Conta criada com sucesso! -=-')
        return{"agencia": agencia, "num_conta": num_conta, "usuario": usuario}
    
    print('\nUsuario não encontrado')

def listar_contas(contas):
    for conta in contas:
        texto = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['num_conta']}
            Titular:\t{conta['usuario']['nome']}
            """
        
        print("=" * 100)
        print(texto)

def main():

    AGENCIA = "0001"

    saldo = 100.00
    qsaque = 0
    lim_diario = 0
    extrato = []
    usuarios = []
    contas = []

    while True:

        inicio = menu()

        opcao = input("Qual operação deseja realizar? ").upper()
        print('-'*60)

        if opcao == 'D':
            depto = float(input("Qual valor deseja depositar? "))
            saldo, extrato = deposito(saldo, depto, extrato)

        elif opcao == 'S':
            saque = float(input("Qual valor deseja sacar? "))
            saldo, extrato = sacar(
                saldo=saldo, saque=saque, extrato=extrato, 
                lim_diario=lim_diario, qsaque=qsaque,)
        
        elif opcao == 'E':
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "X":
            print('Saindo ...')
            time.sleep(2)
            break

        elif opcao == "N":
            novo_usuario(usuarios)

        elif opcao == "V":
            if usuarios == []:
                print('Não há usuários cadastrados!')   
                time.sleep(1.5) 
 
            listar_usuarios(usuarios)
            time.sleep(1)

        elif opcao == "C":
            num_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, num_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "L":
            listar_contas(contas)

        else:
            print('-='*30)
            print('Opção inválida!')
            print('-='*30)
            print('Por favor escolha uma opção válida!')


main()