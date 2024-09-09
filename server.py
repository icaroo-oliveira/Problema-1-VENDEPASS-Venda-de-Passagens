import threading
import json
from connection import config_server, receber_mensagem, encerrar_conexao, testa_conexao_com_cliente, get_ip_address
from utils_server import cria_arquivo_grafo, carregar_grafo, salvar_grafo, encontrar_caminhos, cidades, arquivo_grafo

#ip = get_ip_address('enp3s0f0')
ip = 'localhost'

porta = 65433

# Mutex para impedir que mais de uma thread acesse uma região crítica
lock = threading.Lock()

# Thread que opera cliente individualmente
def handle_client(conexao_socket, client_address):
    try:
        print(f"Conectado a {client_address}")

        # Espera resposta do socket conexão
        data = receber_mensagem(conexao_socket)

        # Se receber algum dado, opera
        # Se não receber nenhum dado, vai pro finally e encerra conexão
        if data:
            flag, origem, destino, id, caminho = data.decode('utf-8').split(',', 4)
            origem = cidades[int(origem) - 1]
            destino = cidades[int(destino) - 1]
            
            # Se cliente enviou flag Caminhos, servidor retorna caminhos de origem a destino
            if flag == "Caminhos":
                print(f"Recebido a flag: {flag}")
                print(f"Recebido a origem: {origem}")
                print(f"Recebido o destino: {destino}")
                
                # Região crítica - Outra thread não pode mexer no arquivo enquanto tiver carregando informação do arquivo e
                # enviando ao cliente
                with lock:
                    G = carregar_grafo(arquivo_grafo)
                    caminhos = encontrar_caminhos(G, origem, destino)
                    serializa = json.dumps(caminhos)

                    mensagem = f"0,{serializa}"

                    # Verifica se cliente deu close() (encerrou conexão)
                    # Se não encerrou, envia os caminhos encontrados
                    testa_conexao_com_cliente(conexao_socket, mensagem, "Caminhos enviados com sucesso")

            # Se cliente enviou flag Comprar, servidor retorna sucesso de compra ou novos caminhos
            elif flag == "Comprar":
                print(f"Recebido a flag: {flag}")
                print(f"Recebido {caminho}, {id}")
                caminho = json.loads(caminho)

                comprar = True
                
                # Região crítica - Outra thread não pode mexer no arquivo enquanto tiver carregando informação do arquivo ou
                # gravando informação nele, e enviando ao cliente
                with lock:
                    # Pega informação atual do grafo
                    G = carregar_grafo(arquivo_grafo)

                    # Verifica se caminho escolhido pelo cliente ainda ta disponível (compara com grafo atual)
                    for i in range(len(caminho[1]) - 1):
                        trecho = (caminho[1][i], caminho[1][i + 1])

                        # Se algum trecho do caminho escolhido pelo cliente não tiver mais assento
                        # encontra e retorna novos caminhos para ele (grafo atualizado)
                        if G[trecho[0]][trecho[1]]['assentos'] == 0:
                            comprar = False
                            caminhos = encontrar_caminhos(G, origem, destino)
                            serializa = json.dumps(caminhos)
                            mensagem = f"Novos_Caminhos,{serializa}"

                            # Verifica se cliente deu close() (encerrou conexão)
                            # Se não encerrou, envia os novos caminhos encontrados
                            testa_conexao_com_cliente(conexao_socket, mensagem, "Novos caminhos enviados com sucesso")

                            break
                    
                    # Se todos os trechos do caminho escolhido pelo cliente estiverem ainda disponíveis
                    # no grafo atualizado, registra compra e atualiza o grafo
                    if comprar:
                        for i in range(len(caminho[1]) - 1):
                            trecho = (caminho[1][i], caminho[1][i + 1])
                            G[trecho[0]][trecho[1]]['assentos'] -= 1
                            G[trecho[0]][trecho[1]]['id'].append(id)
                        salvar_grafo(G, arquivo_grafo)
                        mensagem = f"Compra_Feita,"

                        # Verifica se cliente deu close() (encerrou conexão)
                        # Se não encerrou, envia informação indicando exito na compra
                        testa_conexao_com_cliente(conexao_socket, mensagem, "Compra feita")

            # Se cliente enviou flag inválida (não corresponde a nenhuma operação), 
            # servidor retorna informação referente
            else:
                print("Operação não identificada.")
                mensagem = f"Flag_Invalida,"

                # Verifica se cliente deu close() (encerrou conexão)
                # Se não encerrou, envia informação indicando flag inválida recebida
                testa_conexao_com_cliente(conexao_socket, mensagem, "Operação não identificada informada ao cliente.")
        
    finally:
        encerrar_conexao(conexao_socket)
        print("\nConexão encerrada. Aguardando nova conexão...\n")

def start_server():
    # Se não existir o arquivo, cria um novo
    cria_arquivo_grafo()

    # Se não conseguir criar e configurar servidor, encerra programa
    server_socket = config_server(ip, porta)
    if server_socket is None:
        print("Erro ao iniciar o servidor. Encerrando aplicação.")
        return
    
    # Retorna IP e Porta associada ao socket do servidor
    print(f"\nServidor -> IP: {server_socket.getsockname()[0]}  |  Porta: {server_socket.getsockname()[1]}\n")
    print("Aguardando conexão...")

    # Fica procurando solicitações de conexão constantemente
    while True:
        try:
            # Bloqueia a execução do programa até alguém se conectar
            # Retorna socket da conexão com cliente e informações sobre o cliente (IP e porta)
            conexao_socket, client_address = server_socket.accept()

            # Define um timeout de 10 segundos
            conexao_socket.settimeout(10)
            client_thread = threading.Thread(target=handle_client, args=(conexao_socket, client_address))
            client_thread.start()

        # Se não conseguir se conectar com um cliente, volta a procurar conexões
        except (OSError, Exception) as e:
            print(f"Erro ao aceitar conexão: {e}.")

if __name__ == "__main__":
    start_server()