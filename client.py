import json
import time
from utils_client import *
from interface import mostrar_menu_principal, selecionar_cidades, selecionar_caminho, verificar_passagens_compradas, exibe_compras_cpf
from connection import conecta_server, encerrar_conexao, enviar_e_receber_mensagem

#IP = '172.16.103.7' #passando o ip de uma outra máquina (docker e sem docker)
IP = 'localhost' #testando na mesma máquina
#IP = 'server' #quando for testar servidor e cliente na mesma máquina em containers diferentes.


PORTA = 65433

def start_client():
    while True:
        # Escolhe entre comprar uma passagem, ver passagens compradas em um CPF ou sair do programa
        escolha = mostrar_menu_principal()

        if escolha == '0':
            break

        sair = 0
        menu = 0
        
        # Se escolheu comprar uma passagem
        if escolha == '1':
            # Caso cliente não consiga se conectar, enviar ou receber dados ao servidor, 
            # ele escolhe origem e destino de novo e tenta conectar e enviar ou receber os dados novamente
            while True:
                origem, destino = selecionar_cidades(cidades)
                
                # Encerra aplicação
                if origem == "0" or destino == "0":
                    sair = 1
                    break

                # Volta pro menu principal
                if origem == "100" or destino == "100":
                    menu = 1
                    
                    clear_terminal()
                    break
                
                # Se não conseguir se conectar ao servidor, volta a escolha das cidades
                client_socket = conecta_server(IP, PORTA)
                if client_socket is None:
                    sleep_clear(3)
                    continue

                mensagem = f"Caminhos,{origem},{destino},,"

                # Se não enviar ou receber dados, encerra conexão automaticamente e volta a escolha das cidades
                data = enviar_e_receber_mensagem(client_socket, mensagem)
                if data is None:
                    sleep_clear(3)
                    continue
                
                # Se conseguiu enviar e receber dados, encerra conexão e sai do loop
                encerrar_conexao(client_socket)
                break
            
            # Volta pro menu principal
            if menu:
                continue
            
            # Fecha o programa
            if sair:
                break

            flag, dado = data.decode('utf-8').split(',', 1)

            # Servidor não identificou flag enviada pelo cliente, encerra aplicação
            if flag == "Flag_Invalida":
                imprime_divisoria()
                print("Servidor não identificou a operação solicitada. Encerrando aplicação...")

                time.sleep(4)
                break
            
            # Lista de tuplas. Cada tupla = Um caminho
            caminhos = json.loads(dado)

            while True:
                # Verifica se servidor achou algum caminho de origem à destino, se achou
                # exibe caminhos e aguarda escolha do usuário entre voltar ao menu principal, sair do programa
                # ou tentar comprar um caminho
                if caminhos:
                    # Caso cliente não consiga se conectar, enviar ou receber dados do servidor, 
                    # ele escolhe caminho e cpf de novo e tenta conectar e enviar ou receber os dados novamente
                    while True:
                        escolha, cpf = selecionar_caminho(cidades, origem, destino, caminhos)

                        # Encerra aplicação
                        if escolha == "0" or cpf == "0":
                            sair = 1
                            break
                        
                        # Volta ao menu principal
                        if escolha == "100" or cpf == "100":
                            menu = 1

                            clear_terminal()
                            break

                        # Se não conseguir se conectar ao servidor, volta para escolha do caminho
                        client_socket = conecta_server(IP, PORTA)
                        if client_socket is None:
                            sleep_clear(3)
                            continue
                        
                        caminho = caminhos[int(escolha)-1]

                        # Uma tupla da lista de tuplas = Um caminho
                        serializa = json.dumps(caminho)

                        mensagem = f"Comprar,,,{cpf},{serializa}"

                        # Se não enviar ou receber dados, encerra conexão automaticamente e volta para escolha do caminho
                        data = enviar_e_receber_mensagem(client_socket, mensagem)
                        if data is None:
                            sleep_clear(3)
                            continue
                        
                        # Se enviar e receber os dados, encerra conexão
                        encerrar_conexao(client_socket)
                        break
                    
                    # se escolheu sair ou ir pro menu principal, sai do while e volta ao menu principal ou encerra programa
                    if sair or menu:
                        break

                    flag, dado = data.decode('utf-8').split(',', 1)

                    # Servidor não identificou flag enviada pelo cliente, encerra aplicação
                    if flag == "Flag_Invalida":
                        imprime_divisoria()
                        print("Servidor não identificou a operação solicitada. Encerrando aplicação...")
                        sair = 1

                        time.sleep(4)
                        break
                    
                    # Servidor enviou flag indicando que compra foi feita, volta ao menu principal automaticamente
                    elif flag == "Compra_Feita":
                        imprime_divisoria()
                        print("Compra feita com sucesso!")
                        imprime_divisoria()

                        sleep_clear(5)
                        break
                    
                    # Servidor enviou flag indicando que o caminho escolhido não estava mais disponível
                    # Servidor retornou novos caminhos ou caminho vazio (não tem mais nenhum caminho de origem a destino)
                    elif flag == "Novos_Caminhos_Encontrados":
                        # Lista de tuplas atualizada. Cada tupla = Um caminho
                        caminhos = json.loads(dado)

                        imprime_divisoria()
                        print("Caminho escolhido não mais disponível!")

                        time.sleep(2)

                # Caso servidor retorne nenhum caminho, volta ao menu principal automaticamente
                else:
                    imprime_divisoria()
                    print(f"Nenhum caminho disponível de {cidades[int(origem)-1]} para {cidades[int(destino)-1]}")
                    imprime_divisoria()

                    sleep_clear(5)
                    break
            
            # Encerra aplicação
            if sair:
                break
        
        # Se escolheu verificar passagens compradas em um CPF
        elif escolha == '2':
            # Caso cliente não consiga se conectar, enviar ou receber dados do servidor, 
            # ele escolhe cpf de novo e tenta conectar e enviar ou receber os dados novamente
            while True:
                cpf = verificar_passagens_compradas()
                
                # Encerra aplicação
                if cpf == "0":
                    sair = 1
                    break

                # Volta pro menu principal
                if cpf == "100":
                    menu = 1
                    
                    clear_terminal()
                    break
                
                # Se não conseguir se conectar ao servidor, volta a escolha do cpf
                client_socket = conecta_server(IP, PORTA)
                if client_socket is None:
                    sleep_clear(3)
                    continue

                mensagem = f"Passagens_Compradas,,,{cpf},"

                # Se não enviar ou receber dados, encerra conexão automaticamente e volta a escolha do cpf
                data = enviar_e_receber_mensagem(client_socket, mensagem)
                if data is None:
                    sleep_clear(3)
                    continue
                
                # Se conseguiu enviar e receber dados, encerra conexão e sai do loop
                encerrar_conexao(client_socket)
                break
            
            # Volta pro menu principal
            if menu:
                continue
            
            # Fecha o programa
            if sair:
                break
            
            flag, dado = data.decode('utf-8').split(',', 1)

            # Servidor não identificou flag enviada pelo cliente, encerra aplicação
            if flag == "Flag_Invalida":
                imprime_divisoria()
                print("Servidor não identificou a operação solicitada. Encerrando aplicação...")

                time.sleep(4)
                break
            
            # Lista de dicionários. Cada dicionário = Uma compra de determinado CPF
            passagens = json.loads(dado)
            
            # Se servidor encontrou passagens compradas no CPF, 
            # exibe e aguarda escolha do usuário entre voltar ao menu principal ou sair do programa
            if passagens:
                escolha = exibe_compras_cpf(cpf, passagens)
                
                if escolha == '0':
                    break

                clear_terminal()

            # Se servidor não encontrou passagens compradas no CPF, volta ao menu principal automaticamente
            else:
                imprime_divisoria()
                print(f"Não existem passagens compradas para CPF: {cpf}")
                imprime_divisoria()

                sleep_clear(5)
   
    imprime_divisoria()
    print("Até a próxima!")
    imprime_divisoria()

if __name__ == "__main__":
    start_client()
