from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

# Função para gerenciar a comunicação com um cliente específico
def conexao_cliente(cliente_socket, endereco_cliente):
    # Solicita um nome para o cliente
    cliente_socket.send("Digite seu nome: ".encode())
    nome_cliente = cliente_socket.recv(1500).decode()

    print(f'Conexão estabelecida com o cliente {nome_cliente} ({endereco_cliente})')
    
    while True:
        try:
            # Recebe a mensagem do cliente
            mensagem = cliente_socket.recv(1500)
            if not mensagem:
                print(f'Cliente {nome_cliente} desconectado.')
                break
            
            # Exibe a mensagem recebida
            print(f'Mensagem recebida de {nome_cliente} ({endereco_cliente}): {mensagem.decode()}')
            
            # Enviar uma resposta personalizada de volta ao cliente
            resposta = input(f"Digite sua resposta para o cliente {nome_cliente} ({endereco_cliente}): ")
            cliente_socket.send(resposta.encode())
        
        except ConnectionResetError:
            print(f"Cliente {nome_cliente} desconectado abruptamente.")
            break

    # Fecha a conexão com o cliente
    cliente_socket.close()

# Configuração do servidor
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('127.0.0.1', 8000))
server_socket.listen()
print('Servidor está pronto e aguardando conexões na porta 8000')

# Loop principal para aceitar conexões de múltiplos clientes
while True:
    # Aceita a conexão de um novo cliente
    cliente_socket, endereco_cliente = server_socket.accept()

    # Cria uma nova thread para gerenciar a comunicação com esse cliente
    Thread(target=conexao_cliente, args=(cliente_socket, endereco_cliente)).start()
