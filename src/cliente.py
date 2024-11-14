from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

# Função para escutar mensagens do servidor
def escutar_servidor(s):
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

# Função para enviar mensagens para o servidor
def enviar_para_servidor(s):
    while True:
        try:
            mensagem = input("Digite sua mensagem (use @nome_cliente para enviar a um cliente específico): ")
            s.send(mensagem.encode())
        except BrokenPipeError:
            print("Conexão com o servidor foi interrompida.")
            break
        except KeyboardInterrupt:
            print("Encerrando o cliente.")
            s.close()
            break

# Configuração do cliente e conexão ao servidor
s = socket(AF_INET, SOCK_STREAM)
s.connect(('127.0.0.1', 8000))

# Solicita ao usuário um nome
nome_cliente = input("Digite seu nome: ")
s.send(nome_cliente.encode())

print(f'Conectado ao servidor na porta 8000 como {nome_cliente}')

# Inicia threads para enviar e escutar mensagens
Thread(target=escutar_servidor, args=(s,)).start()
Thread(target=enviar_para_servidor, args=(s,)).start()
