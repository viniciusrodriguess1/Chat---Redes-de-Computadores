from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

# Worker para gerenciar a comunicação com o cliente
def conexao_cliente(cliente_socket, endereco_cliente):
    print(f'Conexão estabelecida com o {endereco_cliente}')

    # Envia uma mensagem para o cliente
    cliente_socket.send('Olá, cliente!'.encode())

    while True:
        # Receber uma mensagem do cliente
        mensagem = cliente_socket.recv(1500)
        print(f'Mensagem recebida do cliente ({endereco_cliente}): {mensagem.decode()}')

    # Fecha a conexão com o cliente
    # cliente_socket.close()

# Cria o socket servidor
server_socket = socket(AF_INET, SOCK_STREAM)

# Liga o servidor ao endereço IP e porta
server_socket.bind(('127.0.0.1', 8000))

# Coloca o servidor em modo de escuta
server_socket.listen()

print('Aguardando por novas requisiçõse na porta 8000')

# Ficar esperando por novas conexões de diferentes clientes
while True:
    # Aceita a conexão
    cliente_socket, endereco_cliente = server_socket.accept()
    Thread(target=conexao_cliente, args=(cliente_socket, endereco_cliente)).start()