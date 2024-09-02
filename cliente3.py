import socket
import json

def conecta_server():
    # Cria um socket TCP/IP
    # 1- Define ipv4
    # 2- Socket do tipo TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Configura um endereço ( IP e Porta )
    server_address = ('localhost', 65435)
    
    # conecta ao servidor
    client_socket.connect(server_address)

    return client_socket

def start_client():

    # Lista de cidades do sistema
    cidades = ["Cuiabá", "Goiânia", "Campo Grande", "Belo Horizonte", "Vitória", 
                "São Paulo", "Rio de Janeiro", "Curitiba", "Florianópolis", "Porto Alegre"]

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
        
        client_socket = conecta_server()

        try:
            # Envia 0 pra indicar ao servidor que é pra retornar os caminhos
            mensagem = f"{'0'},{origem},{destino},{""},{""}"
            
            client_socket.sendall(mensagem.encode('utf-8'))

            # Recebe a resposta do servidor (até 1024 bytes) -> Nesse caso seria uma lista de caminhos disponíveis
            # Cada termo da lista é uma tupla contendo distancia em km e uma lista com os trechos
            # Exemplo da lista com caminho de São Paulo até Vitória
            # Ex: [ 
            #       (22, ["São Paulo", "Rio de Janeiro", "Vitória"]), -> Lista[0] tem tudo isso
            #       (30, ["São Paulo", "Vitória"])                    -> Lista[1] tem tudo isso
            #     ]
            data = client_socket.recv(1024)

        finally:
            # Fecha a conexão
            client_socket.close()
    
        # Transforma em lista novamente
        caminhos = json.loads(data.decode('utf-8'))

        encerrar = 0
        while True:
            
            # Se o servidor achou caminhos
            if caminhos:
                print(f"Voos de {cidades[int(origem)-1]} para {cidades[int(destino)-1]}\n")

                tam = len(caminhos)

                for i in range(tam):
                    dist, path = caminhos[i]
                    print(f"{i+1}. Caminho: {' -> '.join(path)} | {dist}km\n")

                print("0- Encerrar programa\n100- Menu\n")

                while True:
                    escolha = input("Escolha um caminho: ")

                    if (int(escolha) < 0 or int(escolha) > 100 or (int(escolha) > tam and int(escolha) <= 99)):
                        escolha = (input("Entrada inválida."))
                    
                    else:
                        break
                
                if escolha == "0":
                    encerrar = 1
                    break
                
                if escolha == "100":
                    encerrar = 0
                    break
                
                # Caminho escolhido ( tupla com distancia e lista de trechos ) -> Envia ao servidor pra verificar se caminho ainda ta disponível
                caminho = caminhos[int(escolha)-1]
                
                id = input("Digite seu CPF para registro da compra (apenas os números): ")

                # Transforma tupla e envia para o servidor
                serializa = json.dumps(caminho)
                
                # Reestabelece conexão para enviar caminho escolhido
                client_socket = conecta_server()
            
                try:
                    # Envia 1 para indicar que agora ele quer tentar comprar um caminho
                    mensagem = f"{'1'},{origem},{destino},{id},{serializa}"
                    
                    client_socket.sendall(mensagem.encode('utf-8'))

                    # Recebe a resposta do servidor (até 1024 bytes).
                    # Pode receber uma mensagem de exito ou uma nova lista de caminhos excluindo os indisponíveis
                    data = client_socket.recv(1024)
                
                finally:
                    # Fecha a conexão
                    client_socket.close()
                
                flag, lista = data.decode('utf-8').split(',',1)

                # Se o servidor enviou 0, a escolha ainda tava disponível e comprou
                if flag == '0':
                    print("\nCompra feita com sucesso\n")
                    break
                
                # Se o servidor enviou 1, não tinha mais o caminho, servidor envia caminhos atualizados
                elif flag == '1':
                    # Transforma em lista novamente
                    caminhos = json.loads(lista)

                    print("\nCaminho escolhido não mais disponível!!\n")
            
            # Se a lista veio vazia, não tem caminhos, volta ao menu e não precisa reestabelecer conexão     
            else:
                print(f"\nNenhum caminho disponível de {cidades[int(origem)-1]} para {cidades[int(destino)-1]}\n")
                break

        if encerrar == 1:
            break
    
    print("Até a próxima\n")

if __name__ == "__main__":
    start_client()
