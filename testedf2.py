import threading
import json
from connection import config_server, receber_mensagem, encerrar_conexao, testa_conexao, get_ip_address
from utils_server import cria_arquivo_grafo, carregar_grafo, encontrar_caminhos, verifica_compras_cpf, verifica_caminho_escolhido, registra_caminho_escolhido, verifica_teste, cidades

#IP = get_ip_address('enp3s0f0')
IP = 'localhost'

PORTA = 65433

# Condition para controlar acesso ordenado à região crítica
condition = threading.Condition()

# Thread que opera cliente individualmente
def handle_client(conexao_socket, client_address):
    try:
        print(f"Conectado a {client_address}")

        # Espera resposta do socket conexão
        data = receber_mensagem(conexao_socket)

        # Se receber algum dado, opera
        # Se não receber nenhum dado, vai pro finally e encerra conexão
        if data:
            flag, origem, destino, cpf, caminho = data.decode('utf-8').split(',', 4)
            
            # Se cliente enviou flag Caminhos, servidor retorna caminhos de origem a destino
            if flag == "Caminhos":
                origem = cidades[int(origem) - 1]
                destino = cidades[int(destino) - 1]

                print(f"Recebido a flag: {flag}")
                print(f"Recebido a origem: {origem}")
                print(f"Recebido o destino: {destino}")
                
                # Região crítica - Outra thread não pode mexer no arquivo enquanto tiver carregando informação do arquivo e
                # enviando ao cliente
                with condition:
                    condition.wait_for(lambda: True)  # Aguarda sua vez na fila
                    G = carregar_grafo()
                    caminhos = encontrar_caminhos(G, origem, destino)

                    # Lista de tuplas. Cada tupla = Um caminho
                    serializa = json.dumps(caminhos)

                    mensagem = f"Caminhos_Encontrados,{serializa}"

                    # Verifica se cliente deu close() (encerrou conexão)
                    # Se não encerrou, envia os caminhos encontrados
                    teste = testa_conexao(conexao_socket, mensagem)

                    verifica_teste(teste, "Caminhos enviados com sucesso")
                
                    condition.notify()  # Notifica a próxima thread na fila

            # Se cliente enviou flag Comprar, servidor retorna sucesso de compra ou novos caminhos
            elif flag == "Comprar":
                print(f"Recebido a flag: {flag}")
                print(f"Recebido o caminho: {caminho}")
                print(f"Recebido o cpf: {cpf}")

                # Uma tupla da lista de tuplas = Um caminho
                caminho = json.loads(caminho)
                
                # Primeiro item da lista = origem
                origem = caminho[1][0]

                # Ultimo item da lista = destino
                destino = caminho[1][len(caminho[1]) - 1]
                
                # Região crítica - Outra thread não pode mexer no arquivo enquanto tiver carregando informação do arquivo ou
                # gravando informação nele, e enviando ao cliente
                with condition:
                    condition.wait_for(lambda: True)  # Aguarda sua vez na fila
                    # Pega informação atual do grafo
                    G = carregar_grafo()

                    # Verifica se caminho ainda ta disponível
                    comprar = verifica_caminho_escolhido(G, caminho)
                    
                    # Se retornou false, caminho não ta mais disponível
                    # encontra e retorna novos caminhos para cliente (grafo atualizado)
                    if comprar == False:
                        caminhos = encontrar_caminhos(G, origem, destino)

                        # Lista de tuplas atualizada. Cada tupla = Um caminho
                        serializa = json.dumps(caminhos)

                        mensagem = f"Novos_Caminhos_Encontrados,{serializa}"

                        # Verifica se cliente deu close() (encerrou conexão)
                        # Se não encerrou, envia os novos caminhos encontrados
                        teste = testa_conexao(conexao_socket, mensagem)

                        verifica_teste(teste, "Novos caminhos enviados com sucesso")
                    
                    # Se retornou true, caminho ta disponível
                    else:
                        # Registra compra
                        registra_caminho_escolhido(G, caminho, cpf)

                        mensagem = f"Compra_Feita,"

                        # Verifica se cliente deu close() (encerrou conexão)
                        # Se não encerrou, envia informação indicando exito na compra
                        teste = testa_conexao(conexao_socket, mensagem)

                        verifica_teste(teste, "Compra registrada com sucesso")
                
                    condition.notify()  # Notifica a próxima thread na fila
            
            # Se cliente enviou flag Passagens_Compradas, servidor retorna passagens encontradas ou nenhuma passagem encontrada
            elif flag == "Passagens_Compradas":
                print(f"Recebido a flag: {flag}")
                print(f"Recebido o cpf: {cpf}")

                # Região crítica - Outra thread não pode mexer no arquivo enquanto tiver carregando informação do arquivo ou
                # gravando informação nele
                with condition:
                    condition.wait_for(lambda: True)  # Aguarda sua vez na fila
                    # Pode vir vazio se não encontrou passagens no CPF
                    compras = verifica_compras_cpf(cpf)
                
                    condition.notify()  # Notifica a próxima thread na fila

                # Lista de dicionários. Cada dicionário = Uma compra de determinado CPF
                serializa = json.dumps(compras)

                mensagem = f"Passagens_Encontradas,{serializa}"

                # Verifica se cliente deu close() (encerrou conexão)
                # Se não encerrou, envia informação indicando exito na compra
                teste = testa_conexao(conexao_socket, mensagem)

                verifica_teste(teste, "Passagens encontradas enviadas com sucesso")

            # Se cliente enviou flag inválida (não corresponde a nenhuma operação), 
            # servidor retorna informação referente
            else:
                print(f"Recebido a flag: {flag}")
                print("Operação não identificada.")

                mensagem = f"Flag_Invalida,"

                # Verifica se cliente deu close() (encerrou conexão)
                # Se não encerrou, envia informação indicando flag inválida recebida
                teste = testa_conexao(conexao_socket, mensagem)

                verifica_teste(teste, "Operação não identificada enviada com sucesso")

    finally:
        encerrar_conexao(conexao_socket)
        print("\nConexão encerrada. Aguardando nova conexão...\n")

def start_server():
    # Se não conseguir criar e configurar servidor, encerra programa
    server_socket = config_server(IP, PORTA)
    if server_socket is None:
        print("Erro ao iniciar o servidor. Encerrando aplicação.")
        return
    
    # Se não existir o arquivo, cria um novo
    cria_arquivo_grafo()
    
    # Retorna IP e Porta associada ao socket do servidor
    print(f"\nServidor -> IP: {server_socket.getsockname()[0]}  |  Porta: {server_socket.getsockname()[1]}\n")
    print("Aguardando conexão...")

    # Fica procurando solicitações de conexão constantemente
    while True:
        try:
            # Bloqueia a execução do programa até alguém se conectar
            # Retorna socket da conexão com cliente e informações sobre o cliente (IP e porta)
            conexao_socket, client_address = server_socket.accept()

            # Define um timeout de 10 segundos e cria uma thread para lidar com a nova conexão
            conexao_socket.settimeout(10)
            client_thread = threading.Thread(target=handle_client, args=(conexao_socket, client_address))
            client_thread.start()

        # Se não conseguir se conectar com um cliente, volta a procurar conexões
        except (OSError, Exception) as e:
            print(f"Erro ao aceitar conexão: {e}.")

if __name__ == "__main__":
    start_server()
