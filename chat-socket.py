import socket
import sys

class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(1)

    def wait_for_connections(self):
        print("Aguardando conexões...")
        self.connection, self.client_address = self.socket.accept()
        print("Conexão estabelecida com o cliente:", self.client_address)

    def receive_message(self):
        try:
            data = self.connection.recv(1024).decode()
            if data:
                print("Mensagem recebida:", data)
            else:
                print("Conexão encerrada pelo cliente.")
                return False
        except:
            print("Erro ao receber a mensagem.")
            sys.exit(1)
        return True

    def close(self):
        self.connection.close()
        print("Conexão encerrada.")

class Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.socket.connect((self.server_ip, self.server_port))
            print("Conexão estabelecida com o servidor.")
        except ConnectionRefusedError:
            print("Não foi possível conectar ao servidor.")
            sys.exit(1)

    def send_message(self, message):
        try:
            self.socket.sendall(message.encode())
        except:
            print("Erro ao enviar a mensagem.")
            sys.exit(1)

    def close(self):
        self.socket.close()
        print("Conexão encerrada.")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python chat-socket.py [servidor/cliente] [IP] [porta]")
        sys.exit(1)

    role = sys.argv[1]
    ip = sys.argv[2]
    port = int(sys.argv[3])

    if role == "servidor":
        server = Server(ip, port)
        server.wait_for_connections()

        while True:
            if not server.receive_message():
                break

        server.close()

    elif role == "cliente":
        client = Client(ip, port)
        client.connect()

        while True:
            message = input("msg: ")
            if message == 'sair':
                break

            client.send_message(message)

        client.close()

    else:
        print("Uso: python chat-socket.py [servidor/cliente] [IP] [porta].")
        sys.exit(1)
