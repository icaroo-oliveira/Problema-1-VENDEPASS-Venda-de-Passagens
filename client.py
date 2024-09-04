import json
import time
from utils import clear_terminal, imprime_divisoria, soma_valor, sleep_clear
from interface import mostrar_menu_principal, selecionar_cidades
from connection import conecta_server, enviar_mensagem, receber_mensagem, encerrar_conexao

def start_client():
    cidades = ["Cuiabá", "Goiânia", "Campo Grande", "Belo Horizonte", "Vitória", 
               "São Paulo", "Rio de Janeiro", "Curitiba", "Florianópolis", "Porto Alegre"]

    while True:
        escolha = mostrar_menu_principal()

        if escolha == '0':
            break
        
        origem, destino = selecionar_cidades(cidades)
        if origem == "0" or destino == "0":
            break
        if origem == "100" or destino == "100":
            clear_terminal()
            continue
        
        client_socket = conecta_server()
        if client_socket is None:
            sleep_clear(3)
            continue

        mensagem = f"0,{origem},{destino},,"
        
        data = enviar_mensagem(client_socket, mensagem)
        if data is None:
            sleep_clear(3)
            continue
        
        data = receber_mensagem(client_socket)
        if data is None:
            sleep_clear(3)
            continue
        
        encerrar_conexao(client_socket)

        caminhos = json.loads(data.decode('utf-8'))
        encerrar = 0

        while True:
            if caminhos:
                imprime_divisoria()
                print(f"Voos de {cidades[int(origem)-1]} para {cidades[int(destino)-1]}:\n")
                for i, (dist, path) in enumerate(caminhos):
                    print(f"{i+1}. Caminho: {' -> '.join(path)} | {dist}km | R$ {soma_valor(dist)}\n")

                print("0- Encerrar programa\n100- Menu\n")

                while True:
                    escolha = input("Escolha um caminho: ")
                    if escolha.isdigit() and (0 <= int(escolha) <= len(caminhos) or int(escolha) == 100):
                        break
                    print("Entrada inválida.")

                if escolha == "0":
                    encerrar = 1
                    break
                if escolha == "100":
                    clear_terminal()
                    break
                
                caminho = caminhos[int(escolha)-1]
                id = input("Digite seu CPF para registro da compra (apenas os números): ")
                serializa = json.dumps(caminho)

                client_socket = conecta_server()
                if not client_socket:
                    sleep_clear(3)
                    break

                mensagem = f"1,{origem},{destino},{id},{serializa}"

                data = enviar_mensagem(client_socket, mensagem)
                if data is None:
                    time.sleep(3)
                    continue

                data = receber_mensagem(client_socket)
                if data is None:
                    time.sleep(3)
                    continue
                
                encerrar_conexao(client_socket)

                flag, lista = data.decode('utf-8').split(',', 1)
                if flag == '0':
                    imprime_divisoria()
                    print("Compra feita com sucesso!")
                    imprime_divisoria()

                    sleep_clear(5)
                    break

                elif flag == '1':
                    caminhos = json.loads(lista)
                    imprime_divisoria()
                    print("Caminho escolhido não mais disponível!")
                    time.sleep(2)

            else:
                imprime_divisoria()
                print(f"Nenhum caminho disponível de {cidades[int(origem)-1]} para {cidades[int(destino)-1]}")
                imprime_divisoria()

                sleep_clear(5)
                break

        if encerrar == 1:
            break
    
    imprime_divisoria()
    print("Até a próxima!")
    imprime_divisoria()

if __name__ == "__main__":
    start_client()