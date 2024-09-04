import socket
import threading
import networkx as nx
import heapq
import json
import time
cont = 0

def carregar_grafo(arquivo):
    # Abre arquivo e retorna os dados do grafo
    with open(arquivo, 'r') as arq:
        dados_existentes = json.load(arq)
    
    # Cria novo grafo para armazenar dados do grafo retornado
    grafo = nx.DiGraph()

    # Salva cada trecho no grafo
    for trecho in dados_existentes['trecho']:
        grafo.add_edge(
            trecho['v1'], trecho['v2'], 
            distancia = trecho['distancia'], 
            assentos = trecho['assentos'],
            id = trecho['id']
        )
    
    return grafo

def salvar_grafo(grafo, arquivo):

    # Novo grafo a ser salvo em arquivo
    dados_novos = {'trecho': []}

    # Salva novos dados de cada trecho (atualiza na lista de cada trecho. LISTA = informações como distancia e etc)
    for v1, v2, atributos in grafo.edges(data=True):
        dados_novos['trecho'].append({
            'v1': v1,
            'v2': v2,
            'distancia': atributos['distancia'],
            'assentos': atributos['assentos'],
            'id': atributos['id']
        })

    # Salva novo grafo em arquivo
    with open(arquivo, 'w') as arq:
        json.dump(dados_novos, arq, indent=4)

def encontrar_caminhos(grafo, cidade_inicial, cidade_fim):
    caminhos = []
    
    # Retorna todos os caminhos possíveis entre v1 e v2
    for path in nx.all_simple_paths(grafo, source=cidade_inicial, target=cidade_fim):

        # Verifica se algum trecho do caminho encontrado não possui assentos
        caminho_valido = True
        for i in range(len(path) - 1):
            trecho = (path[i], path[i + 1])
            if grafo[trecho[0]][trecho[1]]['assentos'] == 0:
                caminho_valido = False
                break
        
        if caminho_valido:
            # Calcula distancia do caminho encontrado
            dist = sum(grafo[path[i]][path[i + 1]]['distancia'] for i in range(len(path) - 1))

            # Organiza os caminhos em fila de prioridade (menor ao maior) a depender da distancia
            heapq.heappush(caminhos, (dist, path))
    
    # Converte o heap em uma lista ordenada e limita a 10 elementos
    caminhos_ordenados = [heapq.heappop(caminhos) for _ in range(min(len(caminhos), 10))]
    
    return caminhos_ordenados






def handle_client(connection, client_address):

    global cont

    cidades = ["Cuiabá", "Goiânia", "Campo Grande", "Belo Horizonte", "Vitória", 
               "São Paulo", "Rio de Janeiro", "Curitiba", "Florianópolis", "Porto Alegre"]
    arquivo_grafo = 'grafo.json'
    
    

    try:
        
        
        print(f"Conectado a {client_address}")
        # if cont==0:
        #     time.sleep(20)
        # if cont==1:
        #     time.sleep(20)
        # if cont==2:
        #     time.sleep(20)
        data = connection.recv(1024)
        #cont+=1
        if data:
            flag, origem, destino, id, caminho = data.decode('utf-8').split(',', 4)
            origem = cidades[int(origem) - 1]
            destino = cidades[int(destino) - 1]
            
            if flag == '0':
                print(f"Recebido a flag: {flag}")
                print(f"Recebido a origem: {origem}")
                print(f"Recebido o destino: {destino}")
                G = carregar_grafo(arquivo_grafo)
                caminhos = encontrar_caminhos(G, origem, destino)
                serializa = json.dumps(caminhos)
                connection.sendall(serializa.encode('utf-8'))

            elif flag == '1':
                G = carregar_grafo(arquivo_grafo)
                caminho = json.loads(caminho)
                print(f"Recebido a flag: {flag}")
                print(f"Recebido {caminho}, {id}")

                comprar = True
                for i in range(len(caminho[1]) - 1):
                    trecho = (caminho[1][i], caminho[1][i + 1])
                    if G[trecho[0]][trecho[1]]['assentos'] == 0:
                        message = '1'
                        caminhos = encontrar_caminhos(G, origem, destino)
                        serializa = json.dumps(caminhos)
                        envia = f"{message},{serializa}"
                        connection.sendall(envia.encode('utf-8'))
                        comprar = False
                        break

                if comprar:
                    for i in range(len(caminho[1]) - 1):
                        trecho = (caminho[1][i], caminho[1][i + 1])
                        G[trecho[0]][trecho[1]]['assentos'] -= 1
                        G[trecho[0]][trecho[1]]['id'].append(id)
                    salvar_grafo(G, arquivo_grafo)
                    message = '0'
                    nada = "d"
                    envia = f"{message}, {nada}"
                    connection.sendall(envia.encode('utf-8'))
    finally:
        connection.close()
        print("\nConexão encerrada. Aguardando nova conexão...\n")
        print(cont)


def start_server():
    # Cidades do sistema
    cidades = ["Cuiabá", "Goiânia", "Campo Grande", "Belo Horizonte", "Vitória", 
            "São Paulo", "Rio de Janeiro", "Curitiba", "Florianópolis", "Porto Alegre"]

    # Arquivo JSON onde o grafo será salvo/carregado
    arquivo_grafo = 'grafo.json'

    # Carregando o grafo a partir do arquivo JSON
    try:
        G = carregar_grafo(arquivo_grafo)
        print("Grafo carregado com sucesso.")
    
    except FileNotFoundError:
        print("Arquivo não encontrado. Criando um novo grafo.")
        
        # Criando um novo grafo e salvando
        G = nx.DiGraph()

        # Caminhos de Cuiabá
        G.add_edge("Cuiabá", "Goiânia", distancia=890, assentos=3, id=[])
        G.add_edge("Cuiabá", "Campo Grande", distancia=700, assentos=3, id=[])

        # Caminhos de Goiânia
        G.add_edge("Goiânia", "Cuiabá", distancia=890, assentos=3, id=[])
        G.add_edge("Goiânia", "Campo Grande", distancia=840, assentos=3, id=[])
        G.add_edge("Goiânia", "Belo Horizonte", distancia=890, assentos=3, id=[])

        # Caminhos de Campo Grande
        G.add_edge("Campo Grande", "Cuiabá", distancia=700, assentos=3, id=[])
        G.add_edge("Campo Grande", "Goiânia", distancia=840, assentos=3, id=[])
        G.add_edge("Campo Grande", "Belo Horizonte", distancia=1250, assentos=3, id=[])
        G.add_edge("Campo Grande", "São Paulo", distancia=980, assentos=3, id=[])
        G.add_edge("Campo Grande", "Curitiba", distancia=1000, assentos=3, id=[])

        # Caminhos de Belo Horizonte
        G.add_edge("Belo Horizonte", "Goiânia", distancia=890, assentos=3, id=[])
        G.add_edge("Belo Horizonte", "Vitória", distancia=510, assentos=3, id=[])
        G.add_edge("Belo Horizonte", "Campo Grande", distancia=1250, assentos=3, id=[])
        G.add_edge("Belo Horizonte", "São Paulo", distancia=585, assentos=3, id=[])
        G.add_edge("Belo Horizonte", "Rio de Janeiro", distancia=440, assentos=3, id=[])

        # Caminhos de Vitória
        G.add_edge("Vitória", "Belo Horizonte", distancia=510, assentos=3, id=[])
        G.add_edge("Vitória", "Rio de Janeiro", distancia=520, assentos=3, id=[])

        # Caminhos de São Paulo
        G.add_edge("São Paulo", "Belo Horizonte", distancia=585, assentos=3, id=[])
        G.add_edge("São Paulo", "Campo Grande", distancia=980, assentos=3, id=[])
        G.add_edge("São Paulo", "Rio de Janeiro", distancia=440, assentos=3, id=[])
        G.add_edge("São Paulo", "Curitiba", distancia=400, assentos=3, id=[])

        # Caminhos de Rio de Janeiro
        G.add_edge("Rio de Janeiro", "Vitória", distancia=520, assentos=3, id=[])
        G.add_edge("Rio de Janeiro", "Belo Horizonte", distancia=440, assentos=3, id=[])
        G.add_edge("Rio de Janeiro", "São Paulo", distancia=440, assentos=3, id=[])

        # Caminhos de Curitiba
        G.add_edge("Curitiba", "Campo Grande", distancia=1000, assentos=3, id=[])
        G.add_edge("Curitiba", "São Paulo", distancia=400, assentos=3, id=[])
        G.add_edge("Curitiba", "Florianópolis", distancia=300, assentos=3, id=[])

        # Caminhos de Florianópolis
        G.add_edge("Florianópolis", "Curitiba", distancia=300, assentos=3, id=[])
        G.add_edge("Florianópolis", "Porto Alegre", distancia=460, assentos=3, id=[])

        # Caminhos de Porto Alegre
        G.add_edge("Porto Alegre", "Florianópolis", distancia=460, assentos=3, id=[])

        # Estrutura é parecida com isso
        # { 
        #   ("São Paulo", "Rio de Janeiro") : {'distancia': 980, 'assentos': 3, 'id': []}
        #   ("Vitória", "Curitiba") : {'distancia': 34, 'assentos': 3, 'id': []}
        #   ...
        # }

        # É um dicionário geral que armazena todas as conexões (grafo)
        # As chaves desse dicionário são tuplas que armazenam a v1 e v2 (cidades com conexão)
        # Os valores dessas chaves são dicionários, onde as chaves serão as distancias, assentos e id. Os valores
        # dessas chaves são as informações desses dados
        salvar_grafo(G, arquivo_grafo)


    # Cria um socket TCP/IP
    # 1- Define ipv4
    # 2- Socket do tipo TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # # Configura um endereço ( IP e Porta ) e associa ele a um socket
    server_address = ('localhost', 65435)
    server_socket.bind(server_address)

    # Servidor aguarda por conexões
    server_socket.listen(5)
    print("Aguardando conexão...")

    while True:
        
        # Espera por uma conexão
        # Bloqueia a execução do programa até alguém se conectar
        # Retorna socket do cliente e seu endereço IP
        connection, client_address = server_socket.accept()
        
        client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
        client_thread.start()


        

            

if __name__ == "__main__":
    start_server()