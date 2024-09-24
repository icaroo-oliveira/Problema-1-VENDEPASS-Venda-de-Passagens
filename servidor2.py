import socket

import networkx as nx
import heapq
import json

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
    
    return caminhos

def start_server():

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

        # Caminhos de Cuiaba
        G.add_edge("Cuiaba", "Goiania", distancia=890, assentos=3, id=[])
        G.add_edge("Cuiaba", "Campo Grande", distancia=700, assentos=3, id=[])

        # Caminhos de Goiania
        G.add_edge("Goiania", "Cuiaba", distancia=890, assentos=3, id=[])
        G.add_edge("Goiania", "Campo Grande", distancia=840, assentos=3, id=[])
        G.add_edge("Goiania", "Belo Horizonte", distancia=890, assentos=3, id=[])

        # Caminhos de Campo Grande
        G.add_edge("Campo Grande", "Cuiaba", distancia=700, assentos=3, id=[])
        G.add_edge("Campo Grande", "Goiania", distancia=840, assentos=3, id=[])
        G.add_edge("Campo Grande", "Belo Horizonte", distancia=1250, assentos=3, id=[])
        G.add_edge("Campo Grande", "Sao Paulo", distancia=980, assentos=3, id=[])
        G.add_edge("Campo Grande", "Curitiba", distancia=1000, assentos=3, id=[])

        # Caminhos de Belo Horizonte
        G.add_edge("Belo Horizonte", "Goiania", distancia=890, assentos=3, id=[])
        G.add_edge("Belo Horizonte", "Vitoria", distancia=510, assentos=3, id=[])
        G.add_edge("Belo Horizonte", "Campo Grande", distancia=1250, assentos=3, id=[])
        G.add_edge("Belo Horizonte", "Sao Paulo", distancia=585, assentos=3, id=[])
        G.add_edge("Belo Horizonte", "Rio de Janeiro", distancia=440, assentos=3, id=[])

        # Caminhos de Vitoria
        G.add_edge("Vitoria", "Belo Horizonte", distancia=510, assentos=3, id=[])
        G.add_edge("Vitoria", "Rio de Janeiro", distancia=520, assentos=3, id=[])

        # Caminhos de Sao Paulo
        G.add_edge("Sao Paulo", "Belo Horizonte", distancia=585, assentos=3, id=[])
        G.add_edge("Sao Paulo", "Campo Grande", distancia=980, assentos=3, id=[])
        G.add_edge("Sao Paulo", "Rio de Janeiro", distancia=440, assentos=3, id=[])
        G.add_edge("Sao Paulo", "Curitiba", distancia=400, assentos=3, id=[])

        # Caminhos de Rio de Janeiro
        G.add_edge("Rio de Janeiro", "Vitoria", distancia=520, assentos=3, id=[])
        G.add_edge("Rio de Janeiro", "Belo Horizonte", distancia=440, assentos=3, id=[])
        G.add_edge("Rio de Janeiro", "Sao Paulo", distancia=440, assentos=3, id=[])

        # Caminhos de Curitiba
        G.add_edge("Curitiba", "Campo Grande", distancia=1000, assentos=3, id=[])
        G.add_edge("Curitiba", "Sao Paulo", distancia=400, assentos=3, id=[])
        G.add_edge("Curitiba", "Florianopolis", distancia=300, assentos=3, id=[])

        # Caminhos de Florianopolis
        G.add_edge("Florianopolis", "Curitiba", distancia=300, assentos=3, id=[])
        G.add_edge("Florianopolis", "Porto Alegre", distancia=460, assentos=3, id=[])

        # Caminhos de Porto Alegre
        G.add_edge("Porto Alegre", "Florianopolis", distancia=460, assentos=3, id=[])

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

    # Liga o socket a um endereço e porta
    server_address = ('localhost', 65435)
    server_socket.bind(server_address)

    # Servidor aguarda por conexões
    server_socket.listen(1)
    print("Aguardando conexão...\n")

    while True:
        # Espera por uma conexão
        # Bloqueia a execução do programa até alguém se conectar
        # Retorna socket do cliente e seu endereço IP
        connection, client_address = server_socket.accept()
        
        try:
            print(f"Conectado a {client_address}")

            # Cidade origem e destino
            data = connection.recv(1024)

            if data:
                cidades = ["Cuiaba", "Goiania", "Campo Grande", "Belo Horizonte", "Vitoria", 
                        "Sao Paulo", "Rio de Janeiro", "Curitiba", "Florianopolis", "Porto Alegre"]
                
                origem, destino = data.decode('utf-8').split(',')

                origem = cidades[int(origem)-1]
                destino = cidades[int(destino)-1]

                print(f"Recebido a origem: {origem}")
                print(f"Recebido o destino: {destino}")
            
                # Verifica caminhos
                caminhos = encontrar_caminhos(G, origem, destino)

                # Transforma lista e envia para o cliente
                serializa = json.dumps(caminhos)
                connection.sendall(serializa.encode('utf-8'))

                if caminhos:
                    # Espera escolha do cliente
                    data = connection.recv(1024)

                    if data:
                        indice, cpf = data.decode('utf-8').split(',')
                        print(f"Recebido {indice}, {cpf}")

                        # Escolha do caminho pelo cliente
                        dist, path = caminhos[int(indice) - 1]
                        
                        # Remove um asssento de determinado trecho no grafo
                        # Adiciona um ID ao assento comprado
                        for i in range(len(path) - 1):
                            trecho = (path[i], path[i + 1])
                            G[trecho[0]][trecho[1]]['assentos'] -= 1
                            G[trecho[0]][trecho[1]]['id'].append(cpf)
                        
                        salvar_grafo(G, arquivo_grafo)

                        message = "\nCompra feita com sucesso\n"                    
                        connection.sendall(message.encode('utf-8'))

        finally:
            # Fecha a conexão
            connection.close()
            print("Conexão encerrada. Aguardando nova conexão...\n")

if __name__ == "__main__":
    start_server()