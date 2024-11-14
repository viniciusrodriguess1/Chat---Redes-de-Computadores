from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

# Dicionário para armazenar clientes conectados
clientes_conectados = {}

# Função para gerenciar a comunicação com um cliente específico
def conexao_cliente(cliente_socket, endereco_cliente):
    # Solicita um nome para o cliente
    cliente_socket.send("Digite seu nome: ".encode())
    nome_cliente = cliente_socket.recv(1500).decode()

    # Registra o cliente no dicionário de clientes conectados
    clientes_conectados[nome_cliente] = cliente_socket
    print(f'Conexão estabelecida com o cliente {nome_cliente} ({endereco_cliente})')
    
    try:
        while True:
            # Recebe a mensagem do cliente
            mensagem = cliente_socket.recv(1500)
            if not mensagem:
                print(f'Cliente {nome_cliente} desconectado.')
                break
            
            # Exibe a mensagem recebida
            mensagem_decodificada = mensagem.decode()
            print(f'Mensagem recebida de {nome_cliente} ({endereco_cliente}): {mensagem_decodificada}')
            
            # Verifica se a mensagem é direcionada a um cliente específico
            if mensagem_decodificada.startswith('@'):
                # Roteamento de mensagem para um cliente específico
                partes = mensagem_decodificada.split(' ', 1)
                if len(partes) > 1:
                    destinatario = partes[0][1:]  # Remove o '@' do nome do cliente
                    mensagem_para_destinatario = partes[1]

                    # Envia a mensagem para o cliente destinatário
                    if destinatario in clientes_conectados:
                        clientes_conectados[destinatario].send(f"Mensagem de {nome_cliente}: {mensagem_para_destinatario}".encode())
                    else:
                        cliente_socket.send(f"Cliente {destinatario} não encontrado.".encode())
                else:
                    cliente_socket.send("Mensagem para destinatário não especificada.".encode())
            else:
                # Envia a mensagem para todos os clientes conectados
                for cliente, socket_cliente in clientes_conectados.items():
                    if cliente != nome_cliente:
                        socket_cliente.send(f"Mensagem de {nome_cliente}: {mensagem_decodificada}".encode())
        
    except ConnectionResetError:
        print(f"Cliente {nome_cliente} desconectado abruptamente.")
    
    # Remove o cliente do dicionário e fecha a conexão
    del clientes_conectados[nome_cliente]
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
