import socket
import json
import heapq

def start_client():

    # While do menu principal
    while True:
        print("Sistema de vendas\n")

        escolha = (input("1- Comprar\n0- Encerrar programa\n>>> "))

        while escolha != '1' and escolha != '0':
            escolha = (input("Entrada inválida.\n\n1- Comprar\n0- Encerrar programa\n>>> "))

        if escolha == '0':
            break
        
        # Exibe cidades disponíveis
        print("\n1- Cuiabá\n2- Goiânia\n3- Campo Grande\n4- Belo Horizonte\n5- Vitória")
        print("6- São Paulo\n7- Rio de Janeiro\n8- Curitiba\n9- Florianópolis\n10- Porto Alegre\n")

        # Se em algum momento escolhe sair, programa é encerrado e loop quebrado
        # Se em algum momento escolhe menu, loop é reiniciado, voltando ao menu principal
        print("0- Encerrar programa\n100- Menu\n")

        while True:
            origem = input("Escolha o número refetente a cidade origem: ")

            if int(origem) < 0 or (int(origem) > 10 and int(origem) < 100) or int(origem) > 100:
                origem = (input("Entrada inválida."))
            
            else:
                break
        
        if origem == "0":
            break
        
        if origem == "100":
            continue

        while True:
            destino = input("Escolha o número refetente a cidade destino: ")

            if int(destino) < 0 or (int(destino) > 10 and int(destino) < 100) or int(destino) > 100:
                destino = (input("Entrada inválida."))
            
            else:
                break
        
        if destino == "0":
            break
        
        if destino == "100":
            continue
        
        # Se não escolheu sair ou menu, conexão com server é iniciada para verificar voos disponíveis!!!!!!

        # Cria um socket TCP/IP
        # 1- Define ipv4
        # 2- Socket do tipo TCP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conecta ao servidor
        server_address = ('localhost', 65435)
        client_socket.connect(server_address)

        try:
            mensagem = f"{origem},{destino}"
            # Transforma cidade origem e destino em bytes e envia ao servidor
            client_socket.sendall(mensagem.encode('utf-8'))

            # Recebe a resposta do servidor (até 1024 bytes) -> Nesse caso seria uma lista de caminhos disponíveis
            # Cada termo da lista é uma tupla contendo distancia em km e uma lista com os trechos
            # Exemplo da lista com caminho de São Paulo até Vitória
            # Ex: [ 
            #       (22, ["São Paulo", "Rio de Janeiro", "Vitória"]), -> Lista[0] tem tudo isso
            #       (30, ["São Paulo", "Vitória"])                    -> Lista[1] tem tudo isso
            #     ]
            data = client_socket.recv(1024)

            # Transforma em lista novamente
            caminhos = json.loads(data.decode('utf-8'))

            cidades = ["Cuiaba", "Goiania", "Campo Grande", "Belo Horizonte", "Vitoria", 
                       "Sao Paulo", "Rio de Janeiro", "Curitiba", "Florianopolis", "Porto Alegre"]

            # Listando os caminhos do menor para o maior
            if caminhos:
                print(f"Voos de {cidades[int(origem)-1]} para {cidades[int(destino)-1]}\n")
        
                i = 1
                tam = len(caminhos)
                while caminhos:
                    # Pega o primeiro item da lista, remove ele da lista e atualiza lista
                    dist, path = heapq.heappop(caminhos)
                    print(f"{i}. Caminho: {' -> '.join(path)} | {dist}km\n")
                    i+=1

                print("0- Encerrar programa\n100- Menu\n")

                while True:
                    escolha = input("Escolha um caminho: ")

                    if (int(escolha) < 0 or int(escolha) > 100 or (int(escolha) > tam and int(escolha) <= 99)):
                        escolha = (input("Entrada inválida."))
                    
                    else:
                        break

                if escolha == "0":
                    break
                
                if escolha == "100":
                    continue
                
                id = input("Digite seu CPF para registro da compra (apenas os números): ")

                mensagem = f"{escolha},{id}"

                # Se escolheu um caminho, envia para o server e compra seu assento
                client_socket.sendall(mensagem.encode('utf-8'))

                # Recebe a resposta do servidor (até 1024 bytes).
                data = client_socket.recv(1024)
                print(f"{data.decode('utf-8')}")

            # Se a lista veio vazia, não tem caminhos, volta ao menu        
            else:
                print(f"\nNenhum caminho disponível de {cidades[int(origem)-1]} para {cidades[int(destino)-1]}\n")

        finally:
            # Fecha a conexão
            client_socket.close()
    
    print("Até a próxima\n")

if __name__ == "__main__":
    start_client()
