import threading
import json
import queue
import time
from connection import config_server, receber_mensagem, encerrar_conexao, testa_conexao, get_ip_address
from utils_server import cria_arquivo_grafo, carregar_grafo, encontrar_caminhos, verifica_compras_cpf, verifica_caminho_escolhido, registra_caminho_escolhido, verifica_teste, cidades

IP = get_ip_address('enp3s0f0')
#IP = 'localhost'
PORTA = 65433

# Mutex para impedir que mais de uma thread acesse uma região crítica
lock = threading.Lock()
waiting_queue = queue.Queue()

# Funções para garantir ordem de aquisição e liberação do lock
def acquire_lock():
    thread_id = threading.get_ident()
    waiting_queue.put(thread_id)

    # Aguarda até que seja a vez da thread (verificando o topo da fila)
    while waiting_queue.queue[0] != thread_id:
        time.sleep(0.01)  # Pequeno delay para evitar consumo de CPU desnecessário
    
    lock.acquire()  # Adquire o lock quando for a vez da thread

def release_lock():
    waiting_queue.get()  # Remove a thread da fila
    lock.release()  # Libera o lock

# Thread que opera cliente individualmente
def handle_client(conexao_socket, client_address):
    try:
        print(f"Conectado a {client_address}")
        data = receber_mensagem(conexao_socket)

        if data:
            flag, origem, destino, cpf, caminho = data.decode('utf-8').split(',', 4)
            
            if flag == "Caminhos":
                origem = cidades[int(origem) - 1]
                destino = cidades[int(destino) - 1]

                print(f"Recebido a flag: {flag}")
                print(f"Recebido a origem: {origem}")
                print(f"Recebido o destino: {destino}")
                
                # Região crítica
                acquire_lock()
                try:
                    G = carregar_grafo()
                    caminhos = encontrar_caminhos(G, origem, destino)
                    serializa = json.dumps(caminhos)
                    mensagem = f"Caminhos_Encontrados,{serializa}"
                    teste = testa_conexao(conexao_socket, mensagem)
                    verifica_teste(teste, "Caminhos enviados com sucesso")
                finally:
                    release_lock()

            elif flag == "Comprar":
                print(f"Recebido a flag: {flag}")
                print(f"Recebido o caminho: {caminho}")
                print(f"Recebido o cpf: {cpf}")
                caminho = json.loads(caminho)
                origem = caminho[1][0]
                destino = caminho[1][len(caminho[1]) - 1]

                # Região crítica
                acquire_lock()
                try:
                    G = carregar_grafo()
                    comprar = verifica_caminho_escolhido(G, caminho)
                    if not comprar:
                        caminhos = encontrar_caminhos(G, origem, destino)
                        serializa = json.dumps(caminhos)
                        mensagem = f"Novos_Caminhos_Encontrados,{serializa}"
                        teste = testa_conexao(conexao_socket, mensagem)
                        verifica_teste(teste, "Novos caminhos enviados com sucesso")
                    else:
                        registra_caminho_escolhido(G, caminho, cpf)
                        mensagem = f"Compra_Feita,"
                        teste = testa_conexao(conexao_socket, mensagem)
                        verifica_teste(teste, "Compra registrada com sucesso")
                finally:
                    release_lock()

            elif flag == "Passagens_Compradas":
                print(f"Recebido a flag: {flag}")
                print(f"Recebido o cpf: {cpf}")
                
                # Região crítica
                acquire_lock()
                try:
                    compras = verifica_compras_cpf(cpf)
                    serializa = json.dumps(compras)
                    mensagem = f"Passagens_Encontradas,{serializa}"
                    teste = testa_conexao(conexao_socket, mensagem)
                    verifica_teste(teste, "Passagens encontradas enviadas com sucesso")
                finally:
                    release_lock()

            else:
                print(f"Recebido a flag: {flag}")
                print("Operação não identificada.")
                mensagem = f"Flag_Invalida,"
                teste = testa_conexao(conexao_socket, mensagem)
                verifica_teste(teste, "Operação não identificada enviada com sucesso")

    finally:
        encerrar_conexao(conexao_socket)
        print("\nConexão encerrada. Aguardando nova conexão...\n")

def start_server():
    server_socket = config_server(IP, PORTA)
    if server_socket is None:
        print("Erro ao iniciar o servidor. Encerrando aplicação.")
        return
    
    cria_arquivo_grafo()
    
    print(f"\nServidor -> IP: {server_socket.getsockname()[0]}  |  Porta: {server_socket.getsockname()[1]}\n")
    print("Aguardando conexão...")

    while True:
        try:
            conexao_socket, client_address = server_socket.accept()
            conexao_socket.settimeout(10)
            client_thread = threading.Thread(target=handle_client, args=(conexao_socket, client_address))
            client_thread.start()

        except (OSError, Exception) as e:
            print(f"Erro ao aceitar conexão: {e}.")

if __name__ == "__main__":
    start_server()
