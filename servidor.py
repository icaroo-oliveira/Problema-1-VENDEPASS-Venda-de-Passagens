import socket

def start_server():
    # Cria um socket TCP/IP
    # 1- Define ipv4
    # 2- Socket do tipo TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Liga o socket a um endereço e porta
    server_address = ('localhost', 65435)
    server_socket.bind(server_address)

    # Servidor aguarda por conexões
    server_socket.listen(1)
    print("Aguardando conexão...")

    # Espera por uma conexão
    # Bloqueia a execução do programa até alguém se conectar
    # Retorna socket do cliente e seu endereço IP
    connection, client_address = server_socket.accept()
    try:
        print(f"Conectado a {client_address}")

        # Loop para receber dados do cliente
        while True:
            # Recebe até 1024 bytes de dados do cliente
            data = connection.recv(1024)
            
            if data:
                print(f"Recebido: {data.decode('utf-8')}")
                # Envia uma resposta ao cliente
                # Envia de volta ao cliente os dados recebidos
                connection.sendall(data)
            
            # Cliente encerrou a conexão
            else:
                print("Não há mais dados de", client_address)
                break
    finally:
        # Fecha a conexão
        connection.close()

if __name__ == "__main__":
    start_server()
