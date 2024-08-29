import socket

def start_client():
    # Cria um socket TCP/IP
    # 1- Define ipv4
    # 2- Socket do tipo TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conecta ao servidor
    server_address = ('localhost', 65435)
    client_socket.connect(server_address)

    try:
        # Solicitando viagem para :
        message = "Salvador-Recife"
        print(f"Enviando: {message}")

        # Transforma mensagem em bytes e envia ao servidor
        client_socket.sendall(message.encode('utf-8'))

        # Recebe a resposta do servidor (até 1024 bytes).
        data = client_socket.recv(1024)
        print(f"Recebido: {data.decode('utf-8')}")






        #se tem passagem disponível, já compra
        if data.decode('utf-8') == "available":

            message = input("Caminho")

            print(f"Enviando: {message}")
            client_socket.sendall(message.encode('utf-8'))
            


            
            data = client_socket.recv(1024)
            print(f"Recebido: {data.decode('utf-8')}")



    finally:
        # Fecha a conexão
        client_socket.close()

if __name__ == "__main__":
    start_client()
