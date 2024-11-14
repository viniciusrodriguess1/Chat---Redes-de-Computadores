from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from colorama import Fore, Style

# Função para escutar mensagens do servidor
def escutar_servidor(s):
    while True:
        try:
            mensagem = s.recv(1500)
            if not mensagem:
                print(f"{Fore.RED}Conexão com o servidor encerrada.{Style.RESET_ALL}")
                break
            print(f"{Fore.MAGENTA}Mensagem recebida do servidor: {Style.RESET_ALL}{mensagem.decode()}")
        except ConnectionResetError:
            print(f"{Fore.RED}Servidor desconectado.{Style.RESET_ALL}")
            break

# Função para enviar mensagens para o servidor
def enviar_para_servidor(s):
    while True:
        try:
            mensagem = input(f"{Fore.YELLOW}Digite sua mensagem (use @nome_cliente para enviar a um cliente específico): {Style.RESET_ALL}")
            s.send(mensagem.encode())
        except BrokenPipeError:
            print(f"{Fore.RED}Conexão com o servidor foi interrompida.{Style.RESET_ALL}")
            break
        except KeyboardInterrupt:
            print(f"{Fore.RED}Encerrando o cliente...{Style.RESET_ALL}")
            s.close()
            break

# Configuração do cliente e conexão ao servidor
s = socket(AF_INET, SOCK_STREAM)
s.connect(('127.0.0.1', 8000))

# Solicita ao usuário um nome
nome_cliente = input(f"{Fore.YELLOW}Digite seu nome: {Style.RESET_ALL}")
s.send(nome_cliente.encode())

print(f"{Fore.GREEN}Conectado ao servidor na porta 8000 como {nome_cliente}{Style.RESET_ALL}")

# Inicia threads para enviar e escutar mensagens
Thread(target=escutar_servidor, args=(s,)).start()
Thread(target=enviar_para_servidor, args=(s,)).start()
