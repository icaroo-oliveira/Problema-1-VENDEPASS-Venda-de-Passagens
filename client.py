import json
import time
from utils import clear_terminal, imprime_divisoria, soma_valor, sleep_clear
from interface import mostrar_menu_principal, selecionar_cidades, selecionar_caminho
from connection import conecta_server, enviar_mensagem, receber_mensagem, encerrar_conexao

cidades = ["Cuiabá", "Goiânia", "Campo Grande", "Belo Horizonte", "Vitória", 
            "São Paulo", "Rio de Janeiro", "Curitiba", "Florianópolis", "Porto Alegre"]


ip = '172.16.103.7'
def start_client():
    while True:
        escolha = mostrar_menu_principal()

        if escolha == '0':
            break
        
        sair = 0
        go_menu = 0

        while True:
            origem, destino = selecionar_cidades(cidades)
            if origem == "0" or destino == "0":
                sair = 1
                break
            if origem == "100" or destino == "100":
                # Volta pro menu principal
                go_menu = 1
                
                clear_terminal()
                break
            
            # Se não conseguir se conectar ao servidor, volta ao menu principal
            client_socket = conecta_server(ip)
            if client_socket is None:
                go_menu = 1

                sleep_clear(3)
                break

            mensagem = f"0,{origem},{destino},,"
            
            # Se não enviar ou receber dados, encerra conexão automaticamente e volta a escolha das cidades ( tenta reenviar/receber os dados )
            data = enviar_mensagem(client_socket, mensagem)
            if data is None:
                sleep_clear(3)
                continue
            
            data = receber_mensagem(client_socket)
            if data is None:
                sleep_clear(3)
                continue
            
            # Depois de enviar e receber o dado, encerra conexão e sai do loop
            encerrar_conexao(client_socket)
            break
        
        # Volta pro menu principal
        if go_menu:
            continue
        
        # Fecha o programa
        if sair:
            break

        flag, dado = data.decode('utf-8').split(',', 1)

        if flag == "-1":
            imprime_divisoria()
            print("Servidor não identificou a operação solicitada. Encerrando aplicação...")

            time.sleep(4)
            break

        caminhos = json.loads(dado)
        
        sair = 0
        go_menu = 0

        while True:
            if caminhos:
                while True:
                    escolha = selecionar_caminho(cidades, origem, destino, caminhos)

                    if escolha == "0":
                        sair = 1
                        break
                    
                    if escolha == "100":
                        go_menu = 1

                        clear_terminal()
                        break
                    
                    caminho = caminhos[int(escolha)-1]
                    id = input("Digite seu CPF para registro da compra (apenas os números): ")
                    serializa = json.dumps(caminho)

                    # Se não conseguir se conectar ao servidor, volta ao menu principal
                    client_socket = conecta_server(ip)
                    if client_socket is None:
                        go_menu = 1

                        sleep_clear(3)
                        break

                    mensagem = f"1,{origem},{destino},{id},{serializa}"

                    # Se não enviar ou receber dados, encerra conexão automaticamente e volta para escolha do caminho
                    data = enviar_mensagem(client_socket, mensagem)
                    if data is None:
                        time.sleep(3)
                        continue

                    data = receber_mensagem(client_socket)
                    if data is None:
                        time.sleep(3)
                        continue
                    
                    # Depois de enviar e receber o dado, encerra conexão
                    encerrar_conexao(client_socket)
                    break
                
                # se escolheu sair ou ir pro menu principal, sai do while
                if sair or go_menu:
                    break

                flag, dado = data.decode('utf-8').split(',', 1)

                if flag == "-1":
                    imprime_divisoria()
                    print("Servidor não identificou a operação solicitada. Encerrando aplicação...")
                    sair = 1

                    time.sleep(4)
                    break

                elif flag == '2':
                    imprime_divisoria()
                    print("Compra feita com sucesso!")
                    imprime_divisoria()

                    sleep_clear(5)
                    break

                elif flag == '1':
                    caminhos = json.loads(dado)
                    imprime_divisoria()
                    print("Caminho escolhido não mais disponível!")

                    time.sleep(2)

            else:
                imprime_divisoria()
                print(f"Nenhum caminho disponível de {cidades[int(origem)-1]} para {cidades[int(destino)-1]}")
                imprime_divisoria()

                sleep_clear(5)
                break
        
        if sair:
            break
    
    imprime_divisoria()
    print("Até a próxima!")
    imprime_divisoria()

if __name__ == "__main__":
    start_client()

    #servidor cai, volta pro menu cliente
    #o client cai durante a comunicacao





    #teste do cabo com timer 
