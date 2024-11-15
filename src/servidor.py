from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from colorama import Fore, Style

# Dicionário para armazenar clientes conectados
clientes_conectados = {}

# Função para gerenciar a comunicação com um cliente específico
def conexao_cliente(cliente_socket, endereco_cliente):
    # Solicita um nome para o cliente
    cliente_socket.send(f"{Fore.GREEN}Digite seu nome: {Style.RESET_ALL}".encode())
    nome_cliente = cliente_socket.recv(1500).decode()

    # Registra o cliente no dicionário de clientes conectados
    clientes_conectados[nome_cliente] = cliente_socket
    print(f"{Fore.CYAN}Conexão estabelecida com o cliente {nome_cliente} ({endereco_cliente}){Style.RESET_ALL}")
    
    try:
        while True:
            # Recebe a mensagem do cliente
            mensagem = cliente_socket.recv(1500)
            if not mensagem:
                print(f"{Fore.YELLOW}Cliente {nome_cliente} desconectado.{Style.RESET_ALL}")
                break
            
            # Exibe a mensagem recebida
            mensagem_decodificada = mensagem.decode()
            print(f"{Fore.MAGENTA}Mensagem recebida de {nome_cliente} ({endereco_cliente}): {Style.RESET_ALL}{mensagem_decodificada}")
            
            # Verifica se a mensagem é direcionada a um cliente específico
            if mensagem_decodificada.startswith('@'):
                # Roteamento de mensagem para um cliente específico
                partes = mensagem_decodificada.split(' ', 1)
                if len(partes) > 1:
                    destinatario = partes[0][1:]  # Remove o '@' do nome do cliente
                    mensagem_para_destinatario = partes[1]

                    # Envia a mensagem para o cliente destinatário
                    if destinatario in clientes_conectados:
                        clientes_conectados[destinatario].send(f"{Fore.CYAN}Mensagem de {nome_cliente}: {mensagem_para_destinatario}{Style.RESET_ALL}".encode())
                    else:
                        cliente_socket.send(f"{Fore.RED}Cliente {destinatario} não encontrado.{Style.RESET_ALL}".encode())
                else:
                    cliente_socket.send(f"{Fore.RED}Mensagem para destinatário não especificada.{Style.RESET_ALL}".encode())
            else:
                # Envia a mensagem para todos os clientes conectados
                for cliente, socket_cliente in clientes_conectados.items():
                    if cliente != nome_cliente:
                        socket_cliente.send(f"{Fore.CYAN}Mensagem de {nome_cliente}: {mensagem_decodificada}{Style.RESET_ALL}".encode())
        
    except ConnectionResetError:
        print(f"{Fore.RED}Cliente {nome_cliente} desconectado abruptamente.{Style.RESET_ALL}")
    
    # Remove o cliente do dicionário e fecha a conexão
    del clientes_conectados[nome_cliente]
    cliente_socket.close()

# Configuração do servidor
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('127.0.0.1', 8000))
server_socket.listen()
print(f"{Fore.GREEN}Servidor está pronto e aguardando conexões na porta 8000...{Style.RESET_ALL}")

# Loop principal para aceitar conexões de múltiplos clientes
while True:
    # Aceita a conexão de um novo cliente
    cliente_socket, endereco_cliente = server_socket.accept()

    # Cria uma nova thread para gerenciar a comunicação com esse cliente
    Thread(target=conexao_cliente, args=(cliente_socket, endereco_cliente)).start()
