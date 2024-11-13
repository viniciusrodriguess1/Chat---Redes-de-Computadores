from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from time import sleep
from datetime import datetime

# Função para enviar mensagens ao servidor
def enviar_mensagens(s):
    while True:
        try:
            mensagem = input("Digite sua mensagem para o servidor: ")
            s.send(mensagem.encode())
        except BrokenPipeError:
            print("Conexão com o servidor foi interrompida.")
            break
        except KeyboardInterrupt:
            print("Encerrando o cliente.")
            s.close()
            break

# Função para escutar mensagens do servidor
def escutar_mensagens(s):
    while True:
        try:
            mensagem = s.recv(1500)
            if not mensagem:
                print("Conexão com o servidor encerrada.")
                break
            print(f'Mensagem recebida do servidor: {mensagem.decode()}')
        except ConnectionResetError:
            print("Servidor desconectado.")
            break

# Configuração e conexão do socket do cliente
s = socket(AF_INET, SOCK_STREAM)
s.connect(('127.0.0.1', 8000))
print('Conectado ao servidor na porta 8000')

# Iniciar threads para enviar e escutar mensagens
Thread(target=enviar_mensagens, args=(s,)).start()
Thread(target=escutar_mensagens, args=(s,)).start()
