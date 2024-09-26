import socket
import subprocess

# Função para retornar IP da máquina
# Parâmetros ->     interface_name: nome da interface de rede para obter endereço IP
# Retorno ->        endereço IP da interface caso seja bem sucedido ou None caso ocorra algum erro
def get_ip_address(interface_name):
    try:
        # Executa o comando `ifconfig` e captura a saída
        result = subprocess.run(
            ['ifconfig', interface_name],
            capture_output=True,
            text=True,
            check=True
        )

        # Busca pela linha que contém 'inet ' (IPv4)
        for line in result.stdout.splitlines():
            if 'inet ' in line and 'netmask' in line:
                # Divide a linha para extrair o IP (primeiro após 'inet')
                ip_address = line.strip().split()[1]
                return ip_address
    
    except subprocess.CalledProcessError:
        return None

# Função pra configurar o socket do servidor
# Parâmetros ->     ip: endereço IP a ser configurado o socket do servidor
#                   porta: porta a ser configurado o socket do servidor
# Retorno ->        socket do servidor caso seja bem sucedido ou None caso ocorra algum erro
def config_server(ip, porta):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define SO_REUSEADDR para permitir a reutilização da porta
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = (ip, porta)

    try:
        server_socket.bind(server_address)
        server_socket.listen(50)
        return server_socket
    
    except (OSError, Exception) as e:
        print(f"Erro ao associar o socket ao endereço: {e}")
        return None

# Função para cliente conectar ao servidor ( cria socket do cliente )
# Parâmetros ->     ip: endereço IP a ser configurado o socket do cliente
#                   porta: porta a ser configurado o socket do cliente
# Retorno ->        socket do cliente caso seja bem sucedido ou None caso ocorra algum erro
def conecta_server(ip, porta):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (ip, porta)
    
    try:
        client_socket.settimeout(10)  # Define um timeout de 10 segundos
        client_socket.connect(server_address) 
        return client_socket
    
    except (OSError, socket.timeout, Exception) as e:
        print(f"Erro ao conectar ao servidor: {e}. Retornando...")
        return None

# Função para enviar dados de cliente pra servidor ou o contrario
# Parâmetros ->     new_socket: socket que deseja enviar uma mensagem
#                   mensagem: dado a ser enviado pelo socket
# Retorno ->        1 caso seja bem sucedido ou None caso ocorra algum erro
def enviar_mensagem(new_socket, mensagem):
    try:
        new_socket.sendall(mensagem.encode('utf-8'))
        return 1
    
    # conexão encerrada, conexão demorou muito, outro erro qualquer
    except (OSError, socket.timeout, Exception) as e:
        print(f"Erro no envio de dados: {e}. Retornando ...")
        encerrar_conexao(new_socket)
        return None

# Função para receber dados de cliente pra servidor ou o contrario
# Parâmetros ->     new_socket: socket que deseja receber uma mensagem
# Retorno ->        mensagem recebida caso seja bem sucedido ou None caso ocorra algum erro
def receber_mensagem(new_socket):
    try:
        data = new_socket.recv(4096)

        # Um dos lados encerrou conexão
        if data == b'':
            print("Conexão foi encerrada antes de receber dados.")
            return None
        
        return data

    # conexão encerrada, conexão demorou muito, outro erro qualquer
    except (OSError, socket.timeout, Exception) as e:
        print(f"Erro no recebimento de dados: {e}. Retornando ...")
        encerrar_conexao(new_socket)
        return None

# Função pra encerrar conexão
# Parâmetros ->     new_socket: socket que deseja encerrar conexão
# Retorno ->        Sem retorno
def encerrar_conexao(new_socket):
    try:
        new_socket.close()
    
    # tentar fechar socket ja fechado ou qualquer outro problema
    except (OSError, Exception) as e:
        print(f"Erro ao fechar o socket: {e}")

# Função para cliente enviar e receber mensagem ao servidor 
# (sempre que cliente envia mensagem, ele deve esperar resposta do servidor)
# Parâmetros ->     client_socket: socket do cliente
#                   mensagem: dado a ser enviado pelo socket
# Retorno ->        mensagem recebida caso seja bem sucedido ou None caso ocorra algum erro
def enviar_e_receber_mensagem(client_socket, mensagem):
    data = testa_conexao(client_socket, mensagem)
    if data is None:
        return None
    
    return receber_mensagem(client_socket)

# Função para verificar se ainda tem conexão ativa cliente/servidor, antes de enviar dados (evita enviar dados atoa)
# Caso não exista conexão, evita que cliente ou servidor envie dado para lugar algum
# Parâmetros ->     new_socket: socket que deseja testar conexão
#                   mensagem: dado a ser enviado pelo socket
# Retorno ->        1 caso seja bem sucedido ou None caso ocorra algum erro
def testa_conexao(new_socket, mensagem):
    # Impede de recv congelar fluxo para esperar dados
    new_socket.setblocking(False)
    try:
        # Tenta ler do socket para verificar se conexão ainda existe (lança exceção se não tem dados disponíveis)
        data = new_socket.recv(1024)
        
        # Se não fechou conexão, envia mensagem (recv = b'', indica que não tem conexão = algum dos lados encerrou conexão )
        if data != b'':
            new_socket.setblocking(True)

            # Redefine timeout ( setblocking(false) reseta timeout )
            new_socket.settimeout(10)
            data = enviar_mensagem(new_socket, mensagem)
            
            # Pode ser 1 = sucesso, None = deu ruim
            return data

        # Caso conexão esteja fechada      
        else:
            print("Conexão foi encerrada antes de enviar dados.")
            return None
   
    # Caso conexão esteja open, mas lado oposto não tem dado a enviar ( ta esperando retorno )
    except BlockingIOError:
        new_socket.setblocking(True)  # Volta ao modo bloqueante para enviar

        # Redefine timeout ( setblocking(false) reseta timeout )
        new_socket.settimeout(10)
        data = enviar_mensagem(new_socket, mensagem)
        
        # Pode ser 1 = sucesso, None = deu ruim
        return data
