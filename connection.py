import socket

# Função pra configurar o servidor
def config_server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.settimeout(10)  # Define um timeout de 10 segundos
        server_address = ('localhost', 65435)
        server_socket.bind(server_address)
        server_socket.listen(5)
        print("Aguardando conexão...")
        return server_socket
    
    except (OSError, Exception) as e:
        print(f"Erro ao associar o socket ao endereço: {e}")
        return None

# Função para cliente conectar ao servidor
def conecta_server():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(10)  # Define um timeout de 10 segundos
        server_address = ('localhost', 65435)
        client_socket.connect(server_address) 
        return client_socket
    
    except (OSError, socket.timeout, Exception) as e:
        print(f"Erro ao conectar ao servidor: {e}")
        return None

# Função para enviar dados de cliente pra servidor ou o contrario
def enviar_mensagem(new_socket, mensagem):
    try:
        new_socket.sendall(mensagem.encode('utf-8'))
        return 1
    
    # conexão encerrada, conexão demorou muito, outro erro qualquer
    except (socket.error, socket.timeout, Exception) as e:
        print(f"Erro no envio de dados: {e}. Retornando ...")
        encerrar_conexao(new_socket)
        return None

# Função para receber dados de cliente pra servidor ou o contrario
def receber_mensagem(new_socket):
    try:
        data = new_socket.recv(1024)
        return data
    
    # conexão encerrada, conexão demorou muito, outro erro qualquer
    except (OSError, socket.timeout, Exception) as e:
        print(f"Erro no recebimento de dados: {e}. Retornando ...")
        encerrar_conexao(new_socket)
        return None

# Função pra encerrar conexão
def encerrar_conexao(new_socket):
    try:
        new_socket.close()
    
    # tentar fechar socket ja fechado
    except (OSError, Exception) as e:
        print(f"Erro ao fechar o socket: {e}")