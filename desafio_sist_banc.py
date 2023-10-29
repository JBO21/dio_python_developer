import time

print ('-='*12, "Banco JBO", '-='*12 )
print ('''-  MENU 
    [D] Depósito
    [S] Saque
    [E] Extrato
    [X] Sair ''')

print('-='*30)
saldo = 100.00
qsaque = 0
lim_diario = 0
extrato = []
while True:
    opcao = input("Qual operação deseja realizar? ").upper()
    print('-'*60)
    if opcao == "D":
        while True:
            depto = float(input("Qual valor deseja depositar? "))
            time.sleep(1.5)
            if depto <= 0:
                print('Valor inválido')
            else: 
                saldo += depto
                msg = (f'Depósito R$ {depto:.2f}')
                extrato.append(msg)
                break
        print(f'Seu saldo atual é R$ {saldo:.2f}')
        print('-='*30)
        
    elif opcao == "S":           
        while True:
            try:
                saque = float(input("Qual valor deseja sacar? "))         
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
        
        print(f'Seu saldo atual é R$ {saldo:.2f}')
        print('-='*30)
        
        
    elif opcao == "E": 
        print('*'*15, 'EXTRATO', '*'*15)       
        for i in extrato:
            print(i)
        print(f'Seu saldo atual é R$ {saldo:.2f}')
        print('-='*30)
        time.sleep(1.5)
    elif opcao == "X":
        print('Saindo ...')
        time.sleep(2)
        break
    else:
        print('-='*30)
        print('Opção inválida!')
        print('-='*30)
        print('Por favor escolha uma opção válida!')
        print ('''-  MENU 
        d = Deposito
        s = Saque
        e = Extrato
        x = Sair ''')