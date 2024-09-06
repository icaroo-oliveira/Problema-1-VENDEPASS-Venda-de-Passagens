import heapq
import json
import networkx as nx

cidades = ["Cuiabá", "Goiânia", "Campo Grande", "Belo Horizonte", "Vitória", 
            "São Paulo", "Rio de Janeiro", "Curitiba", "Florianópolis", "Porto Alegre"]

arquivo_grafo = 'grafo.json'

# Função para quando abrir servidor, carregar ou criar o grafo
def cria_arquivo_grafo():
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

# Função que carrega um grafo do arquivo
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

# Função que salva um grafo no arquivo (atualiza)
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

# Função que encontra 10 caminhos entre origem e destino, e retorna ordenado considerando distancia total (menor ao maior)
def encontrar_caminhos(grafo, cidade_inicial, cidade_fim):
    caminhos = []
    
    # Retorna todos os caminhos possíveis entre origem e destino
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