import threading
import json
import time
from connection import config_server, receber_mensagem, enviar_mensagem, encerrar_conexao
from utils_server import cria_arquivo_grafo, carregar_grafo, salvar_grafo, encontrar_caminhos, cidades, arquivo_grafo

lock = threading.Lock()

def handle_client(liga_socket, client_address):
    try:
        print(f"Conectado a {client_address}")

        data = receber_mensagem(liga_socket)

        if data:
            flag, origem, destino, id, caminho = data.decode('utf-8').split(',', 4)
            origem = cidades[int(origem) - 1]
            destino = cidades[int(destino) - 1]
            
            if flag == "Caminhos":
                print(f"Recebido a flag: {flag}")
                print(f"Recebido a origem: {origem}")
                print(f"Recebido o destino: {destino}")
                
                with lock:
                    G = carregar_grafo(arquivo_grafo)
                    caminhos = encontrar_caminhos(G, origem, destino)
                    serializa = json.dumps(caminhos)

                    mensagem = f"0,{serializa}"
                    
                    data = enviar_mensagem(liga_socket, mensagem)
                    if data:
                        print("Caminhos enviados com sucesso")

            elif flag == "Comprar":
                print(f"Recebido a flag: {flag}")
                print(f"Recebido {caminho}, {id}")
                caminho = json.loads(caminho)

                comprar = True
                
                with lock:
                    G = carregar_grafo(arquivo_grafo)

                    for i in range(len(caminho[1]) - 1):
                        trecho = (caminho[1][i], caminho[1][i + 1])
                        if G[trecho[0]][trecho[1]]['assentos'] == 0:
                            comprar = False
                            caminhos = encontrar_caminhos(G, origem, destino)
                            serializa = json.dumps(caminhos)
                            mensagem = f"Novos_Caminhos,{serializa}"

                            data = enviar_mensagem(liga_socket, mensagem)
                            if data:
                                print("Novos caminhos enviados com sucesso")

                            break

                    if comprar:
                        for i in range(len(caminho[1]) - 1):
                            trecho = (caminho[1][i], caminho[1][i + 1])
                            G[trecho[0]][trecho[1]]['assentos'] -= 1
                            G[trecho[0]][trecho[1]]['id'].append(id)
                        salvar_grafo(G, arquivo_grafo)
                        mensagem = f"Compra_Feita,"
                        
                        data = enviar_mensagem(liga_socket, mensagem)
                        if data:
                            print("Compra feita")
                
            else:
                print("Operação não identificada.")
                mensagem = f"Flag_Invalida,"
                data = enviar_mensagem(liga_socket, mensagem)
                if data:
                    print("Operação não identificada informada ao cliente.")
        
    finally:
        encerrar_conexao(liga_socket)
        print("\nConexão encerrada. Aguardando nova conexão...\n")

def start_server():
    cria_arquivo_grafo()

    # Se não conseguir criar e configurar servidor, encerra programa
    server_socket = config_server()
    if server_socket is None:
        print("Erro ao iniciar o servidor. Encerrando aplicação.")
        return

    while True:
        # Espera por uma conexão
        # Bloqueia a execução do programa até alguém se conectar
        # Retorna socket do cliente e seu endereço IP
        try:
            liga_socket, client_address = server_socket.accept()
            liga_socket.settimeout(10)  # Define um timeout de 10 segundos
            client_thread = threading.Thread(target=handle_client, args=(liga_socket, client_address))
            client_thread.start()

        # Se não conseguir se conectar com um cliente, volta a procurar conexões
        except (OSError, Exception) as e:
            print(f"Erro ao aceitar conexão: {e}.")

if __name__ == "__main__":
    start_server()