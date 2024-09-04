import socket
import json
import os #limpar terminal
import platform #verifica se o SO é Linux ou Windows
import time

def clear_terminal():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def soma_valor(km):
    valor = (km / 100) * 115
    return round(valor, 2)

def conecta_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 65435)
    client_socket.connect(server_address)
    return client_socket

def imprime_divisoria():
    print("\n" + "=" * 120 + "\n")

def start_client():
    cidades = ["Cuiabá", "Goiânia", "Campo Grande", "Belo Horizonte", "Vitória", 
               "São Paulo", "Rio de Janeiro", "Curitiba", "Florianópolis", "Porto Alegre"]

    while True:
        imprime_divisoria()
        print("Sistema de Vendas de Passagens")
        imprime_divisoria()
        escolha = input("1- Comprar\n0- Encerrar programa\n\n>>> ")

        while escolha not in ['1', '0']:
            print("Entrada inválida.")
            escolha = input("\n1- Comprar\n0- Encerrar programa\n>>> ")

        if escolha == '0':
            break
        
        imprime_divisoria()
        print("Cidades disponíveis:\n")
        for i, cidade in enumerate(cidades):
            print(f"{i+1}- {cidade}")

        print("\n0- Encerrar programa\n100- Menu\n")
        
        origem, destino = None, None
        while True:
            origem = input("Escolha o número referente à cidade origem: ")
            if origem.isdigit() and (0 <= int(origem) <= 10 or int(origem) == 100):
                break
            print("Entrada inválida.")

        if origem == "0":
            break
        if origem == "100":
            clear_terminal()
            continue

        while True:
            destino = input("Escolha o número referente à cidade destino: ")
            if destino.isdigit() and (0 <= int(destino) <= 10 or int(destino) == 100):
                break
            print("Entrada inválida.")

        if destino == "0":
            break
        if destino == "100":
            clear_terminal()
            continue
        
        client_socket = conecta_server()

        try:
            mensagem = f"0,{origem},{destino},,"
            client_socket.sendall(mensagem.encode('utf-8'))
            data = client_socket.recv(1024)
        finally:
            client_socket.close()

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

                try:
                    mensagem = f"1,{origem},{destino},{id},{serializa}"
                    client_socket.sendall(mensagem.encode('utf-8'))
                    data = client_socket.recv(1024)
                finally:
                    client_socket.close()

                flag, lista = data.decode('utf-8').split(',', 1)
                if flag == '0':
                    imprime_divisoria()
                    print("Compra feita com sucesso!")
                    imprime_divisoria()

                    time.sleep(5)
                    clear_terminal()
                    break

                elif flag == '1':
                    caminhos = json.loads(lista)
                    imprime_divisoria()
                    print("Caminho escolhido não mais disponível!")

            else:
                imprime_divisoria()
                print(f"Nenhum caminho disponível de {cidades[int(origem)-1]} para {cidades[int(destino)-1]}")
                imprime_divisoria()

                time.sleep(5)
                clear_terminal()
                break

        if encerrar == 1:
            break
    
    imprime_divisoria()
    print("Até a próxima!")
    imprime_divisoria()

if __name__ == "__main__":
    start_client()
