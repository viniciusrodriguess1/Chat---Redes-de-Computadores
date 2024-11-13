from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

# Função para escutar mensagens do cliente
def escutar_cliente(cliente_socket, endereco_cliente):
    while True:
        try:
            mensagem = cliente_socket.recv(1500)
            if not mensagem:
                print(f'Conexão com o {endereco_cliente} encerrada')
                break
            print(f'Mensagem recebida do cliente ({endereco_cliente}): {mensagem.decode()}')
        except ConnectionResetError:
            print(f'Cliente {endereco_cliente} desconectado abruptamente.')
            break

# Função para enviar mensagens personalizadas para o cliente
def enviar_para_cliente(cliente_socket):
    while True:
        mensagem = input("Digite sua mensagem para o cliente: ")
        cliente_socket.send(mensagem.encode())

# Configuração do servidor
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('127.0.0.1', 8000))
server_socket.listen()
print('Aguardando por novas requisições na porta 8000')

# Aceita conexões e inicia threads para comunicação bidirecional
while True:
    cliente_socket, endereco_cliente = server_socket.accept()
    print(f'Conexão estabelecida com o {endereco_cliente}')
    Thread(target=escutar_cliente, args=(cliente_socket, endereco_cliente)).start()
    Thread(target=enviar_para_cliente, args=(cliente_socket,)).start()
