import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime   

class Cliente:
    def __init__(self, nome):
        self.nome = nome
        self.contas = []
    
    def efetuar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def add_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nasc, cpf, endereco):
        super().__init__(nome)
        self.data_nasc = data_nasc
        self.cpf = cpf
        self.endereco = endereco


class PessoaJuridica(Cliente):
    pass

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        sem_saldo = valor > saldo

        if sem_saldo:
            print('\n \033[1;0;41mXXX Operação não realizada! Saldo insuficiente. XXX\033[m')

        elif valor > 0:
            self._saldo -= valor
            print('\n\033[1;0;42m=== Saque realizado! ===\033[m')
            return True
        
        else:
            print('\n \033[1;0;41mXXX Operação não realizada! Valor inválido! XXX\033[m')

        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('\n \033[1;0;42m=== Depósito realizado! === \033[m')

        else:
            print('\n \033[1;0;41mXXX Operação não realizada! Valor inválido. XXX\033[m')
            return False
        
        return True
    

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, lim_saques = 3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._lim_saques = lim_saques

    def sacar(self, valor):
        num_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__] 
        )

        excedeu_lim = valor > self._limite
        excedeu_saques = num_saques >=self._lim_saques

        if excedeu_lim:
            print('\n \033[1;0;41mXXX Operação não realizada! O valor do saque excede o Limite. XXX\033[m')

        elif excedeu_saques:
            print('\n \033[1;0;41mXXX Operação não realizada! Número máximo de saque atingido. XXX\033[m')

        else:
            return super().sacar(valor)
        
        False

    def __str__(self):
        return f"""\
            Agência:\t {self.agencia} 
            C/c:\t\t {self.numero}
            Titular:\t {self.cliente.nome}
        """
        


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def add_transacao(self, transacao):
        self._transacoes.append(
            {
                'tipo': transacao.__class__.__name__, 
                'valor': transacao.valor, 
                'data': datetime.now()
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao_ok = conta.sacar(self.valor)

        if transacao_ok:
            conta.historico.add_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao_ok = conta.depositar(self.valor)

        if transacao_ok:
            conta.historico.add_transacao(self)



def menu():
    print ('-='*12, "Banco JBO", '-='*12 )
    print ('''-  MENU 
        [N]\t Novo cliente
        [C]\t Criar conta
        [L]\t Listar contas
        [D]\t Depósito
        [S]\t Saque
        [E]\t Extrato
        [X]\t Sair ''')
    
    return input('Opção: ').lower().strip()

def check_cliente(cpf, clientes):
    clientes_verificados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_verificados[0] if clientes_verificados else None

def check_conta_cliente(cliente):
    if not cliente.contas:
        print('\n \033[1;0;41mXXX Cliente não possui conta. XXX\033[m')
        return
    
    return cliente.contas[0]

def depositar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = check_cliente(cpf, clientes)

    if not cliente:
        print('\n \033[1;0;41mXXX Cliente não encontrado! XXX\033[m')
        return
    
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = check_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.efetuar_transacao(conta, transacao)

def saque(clientes):
    cpf = input('Informe o CPF do Cliente: ')
    cliente = check_cliente(cpf, clientes)

    if not cliente:
        print('\n \033[1;0;41mXXX Cliente não encontrado! XXX\033[m')
        return
    
    valor = float(input('Informe o valor do saque: '))
    transacao = Saque(valor)

    conta = check_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.efetuar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = check_cliente(cpf, clientes)

    if not cliente:
        print('\n \033[1;0;41mXXX Cliente não encontrado! XXX\033[m')
        return
    
    conta = check_conta_cliente(cliente)

    print('=-'*15,'EXTRATO','=-'*15)
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = 'Não foram realizadas movimentações.'
    else:
        for transacao in transacoes:
            extrato += f'\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}'

    print(extrato)
    print(f'\nSaldo:\n\tR$ {conta.saldo:.2f}')
    print('=-'*37)
    

def novo_cliente(clientes):
    cpf = input('Informe o CPF(somente números): ')
    cliente = check_cliente(cpf, clientes)

    if cliente:
        print('\n \033[1;0;41mXXX Cliente já existente! XXX\033[m')
        return
    
    nome = input('Nome Completo: ')
    data_nasc = input('Data de nascimento(dd-mm-aaaa): ')
    endereco = input('Endereço completo: ')

    cliente = PessoaFisica(nome=nome, data_nasc=data_nasc, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print('\n \033[1;0;42m=== Cliente cadastrado com sucesso! ===\033[m')


def nova_conta(num_conta, clientes, contas):
    cpf = input('Informe o CPF do cliente: ')
    cliente = check_cliente(cpf, clientes)

    if not cliente:
        print('\n \033[1;0;41 XXX Cliente não encontrado! XXX\033[m')
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=num_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print('\n \033[1;0;42m=== Conta criada com sucesso! ===\033[m')


def listar_contas(contas):
    for conta in contas:
        print('-='*40)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 'd':
            depositar(clientes)

        elif opcao == 's':
            saque(clientes)

        elif opcao == 'e':
            exibir_extrato(clientes)

        elif opcao == 'n':
            novo_cliente(clientes)

        elif opcao == 'c':
            num_conta = len(contas)+1
            nova_conta(num_conta, clientes, contas)

        elif opcao == 'l':
            listar_contas(contas)

        elif opcao == 'x':
            break

        else:
            print('\n\033[1;0;41m XXX Operação inválida, favo selecionar uma opção válida XXX\033[m')



main()

