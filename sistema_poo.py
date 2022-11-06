from abc import ABC, abstractclassmethod, abstractproperty
from time import sleep
from datetime import datetime
import textwrap


def dec():
    print(f'=' * 98)


def div():
    print(f'-' * 98)


def pul():
    print('\n')


def load():
    pul()
    print(f'-' * 98)
    print(f'AGUARDE...')
    print(f'-' * 98)
    pul()
    sleep(1)


def msg():
    dec()
    print(f'SUJEITO A ALTERAÇÃO ATÉ O FINAL DO DIA.')
    dec()


class Cliente:
    def __init__(self, endereco):
        # Argumento recebido é o endereco
        self.endereco = endereco
        self.contas = []
        # contas é iniciado vazio, por isso não entrar no construtor

    def realizar_transacao(self, conta, transacao):
        # Foi mapeado o método relizar transacao com dois argumentos, conta e transacao
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        # No acicionar conta um argumento conta
        self.contas.append(conta)
        # Aqui é adicionado a lista contas


class Pessoa_Fisica(Cliente):
    # A classe Pessoa Fisica estende da class Cliente
    def __init__(self, nome, nascimento, cpf, endereco):
        super().__init__(endereco)
        # Aqui é chamado construtor da classe pai(Cliente)
        self.nome = nome
        self.nascimento = nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()
        # Atributos privados _

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
        # Retorna uma instância de conta

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
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print('Falha na operação! Você não tem saldo Suficiente.')

        elif valor > 5:
            self._saldo -= valor
            print('Saque realizado com sucesso!')
            return True

        else:
            print('Operação não realizado! O valor mínimo para saque é de R$5.00.')

        return False

    def depositar(self, valor):
        div()
        if valor > 10:
            self._saldo += valor
            print('Depósito realizado com sucesso!')

        else:
            print('Operação não realizado! O valor mínimo para depósito é de R$10.00.')
            return False

        return True


class Conta_Corrente(Conta):
    def __init__(self, numero, cliente, limite=1500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao['tipo']
             == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques > self.limite_saques

        if excedeu_limite:
            print(f'Falha na operação! O valor do saque excede o limite diário.')

        elif excedeu_saques:
            print('Falha na operação! Número máximo de saques excedido.')

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': datetime.now(),
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(cls, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    opcoes = '''
        =============== MENU ==================
                [1]\t\tDEPÓSITO
                [2]\t\tSAQUE
                [3]\t\tEXTRATO
                [4]\t\tCADASTRAR NOVO CLIENTE
                [5]\t\tCADASTRAR NOVA CONTA
                [6]\t\tLISTAR CONTAS
                [0]\t\tSAIR
                ESCOLHA UMA OPÇÃO
        =======================================
                    ==> '''
    return input(textwrap.dedent(opcoes))


def filtrar_cliente(cpf, cliente):
    clientes_filtrados = [cliente for cliente in cliente if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta(cliente):
    if not cliente.contas:
        print('Cliente nao possui conta!')
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes):
    cpf = input('Informe o CPF: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\nCliente não localizado!')
        return

    valor = float(input('Informe o valor do depósito: '))
    transacao = Deposito(valor)

    conta = recuperar_conta(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input('Informe o CPF: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\nCliente não localizado!')
        return

    valor = float(input('Informe o valor de saque: '))
    transacao = Saque(valor)

    conta = recuperar_conta(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input('Informe o CPF: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\nCliente não localizado!')
        return

    conta = recuperar_conta(cliente)
    if not conta:
        return

    print('\n=============== EXTRATO ===================')
    transacoes = conta.historico.transacoes

    extrato = ''
    if not transacoes:
        extrato = 'Não existem transações no momento.'
    else:
        for transacao in transacoes:
                extrato += f'\n{transacao["tipo"]}:\n\tR$ {transacao["valor"]:,.2f}'


    print(extrato)
    print(f'\nSaldo:\n\tR$ {conta.saldo:,.2f}')
    print('=============================================')


def criar_cliente(clientes):
    cpf = input('Informe o CPF: ')
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print('\nJá existe cliente com esse CPF!')
        return

    nome = input('Informe o nome: ')
    nascimento = input('Informe a data de nascimento(dd-mm-aaaa): ')
    endereco = input('Informe o endereco (logradouro, nº - Bairro = Cidade/UF): ')

    cliente = Pessoa_Fisica(nome=nome, nascimento=nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print('Cliente criado com sucesso!')


def criar_conta(numero, clientes, contas):
    cpf = input('Informe o CPF: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\nCliente não localizado!')
        return

    conta = Conta_Corrente.nova_conta(cliente=cliente, numero=numero)
    contas.append(conta)
    cliente.contas.append(conta)

    print('Conta criada com sucesso!')


def listar_contas(contas):
    for conta in contas:
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []
    while True:
        opcao = int(menu())

        if opcao == 1:
            depositar(clientes)

        elif opcao == 2:
            sacar(clientes)

        elif opcao == 3:
            exibir_extrato(clientes)

        elif opcao == 4:
            criar_cliente(clientes)

        elif opcao == 5:
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == 6:
            listar_contas(contas)

        elif opcao == 0:
            print('Você encerrou, volte sempre')
            break
        else:
            print('Opção inválida, por favor selecione novamente')


main()

