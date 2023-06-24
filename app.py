import sqlite3
from pushbullet import Pushbullet
import datetime
from tabulate import tabulate
import colorama
from colorama import Fore, Style

# API Pushbullet para enviar notificaçãoo
pb = Pushbullet('o.ZMG4L5olcoV4dVFRppVWNKBsRqGuP9s9')

conn = sqlite3.connect('clientes.db')
cursor = conn.cursor()
# Cria tabela
cursor.execute("""CREATE TABLE IF NOT EXISTS clientes
                (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                endereco TEXT NOT NULL,
                qtd_pizzas INTEGER NOT NULL,
                valor REAL NOT NULL,
                data_pagamento TEXT, 
                pago INTEGER)""")

# Função para enviar notificação
def push_notificacao(titulo, msg):
    pb.push_note(titulo, msg)

# Função para verificar se o pagamento vence hoje e se vencer, envia notificação para o Pushbullet
def verificar_data_pagamento():
    hoje = datetime.datetime.today().strftime("%d/%m/%Y")
    cursor.execute(
        """SELECT * FROM clientes WHERE data_pagamento = ?""", (hoje,))
    rows = cursor.fetchall()

    if len(rows) > 0:
        for row in rows:
            if row[6] == 0:
                msg = f"O pagamento do cliente {row[1]} vence hoje!"
                push_notificacao('Vencimento de pagamento', msg)

# Cadastrar cliente na base de dados
def cadastrar_cliente():
    nome = input('Digite o nome do cliente: ')
    endereco = input('Digite o endereço do cliente: ')
    qtd_pizzas = int(input('Digite a quantidade de pizzas: '))
    valor = float(input('Digite o valor: '))
    data_pagamento = input('Digite a data de pagamento: ')
    pago = int(input('O pagamento foi realizado?(0 - Não, 1 - Sim): '))

    cursor.execute("""INSERT INTO clientes (nome, endereco, qtd_pizzas, valor, data_pagamento, pago)
                    VALUES (?,?,?,?,?,?)""", (nome, endereco, qtd_pizzas, valor, data_pagamento, pago))
    conn.commit()

    print('O cliente foi cadastrado com sucesso!')

# Editar status de pagamento
def editar_pagamento():
    cliente_id = int(input('Digite o ID do cliente: '))
    pago = int(input('Informe o novo status de pagamento (0 - Não, 1 - Sim):  '))

    cursor.execute("""UPDATE clientes SET pago = ? WHERE id = ?""", (pago, cliente_id))
    conn.commit()

# Exibe tabela de clientes coom o tabulate
def exibir_cliente():
    cursor.execute("""SELECT * FROM clientes""")
    rows = cursor.fetchall()

    headers = ['ID', 'Nome', 'Endereço',
               'Quantidade adquirida', 'Valor', 'Data de pagamento', "Pago"]
    table_data = [[row[0], f"{Fore.GREEN}{row[1]}{Style.RESET_ALL}",
                   row[2], row[3], f"R$ {row[4]:.2f}", row[5], "Sim" if row[6] else "Não"] for row in rows]

    print(tabulate(table_data, headers, tablefmt="psql"))
    print()
# Função para excluir cliente
def excluir_cliente():
    cliente_id = int(input('Digite o ID do cliente:'))
    cursor.execute("""DELETE FROM clientes WHERE id = ?""", (cliente_id,))
    conn.commit()
    print('O cliente foi excluído com sucesso!')



# Criação de menu
def menu():
    print(Fore.GREEN + '1 - Cadastrar Cliente')
    print('2 - Alterar status de pagamento')
    print('3 - Exibir Clientes')
    print('4 - Excluir Cliente')
    print(Style.RESET_ALL)

# Função principal
def main():
    colorama.init()

    while True:
        menu()
        op = int(input('Digite a opção desejada: '))
        if op == 1:
            cadastrar_cliente()
        elif op == 2:
            editar_pagamento()
        elif op == 3:
            exibir_cliente()
        elif op == 4:
            excluir_cliente()
        else:
            print('Opção inválida!')
            continue
        verificar_data_pagamento()
    conn.close()

# Execução do programa
if __name__ == '__main__':
    main()
