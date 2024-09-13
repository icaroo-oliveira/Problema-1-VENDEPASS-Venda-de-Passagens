import heapq
import json
import networkx as nx

cidades = ["Cuiabá", "Goiânia", "Campo Grande", "Belo Horizonte", "Vitória", 
            "São Paulo", "Rio de Janeiro", "Curitiba", "Florianópolis", "Porto Alegre"]

ARQUIVO_GRAFO = 'grafo.json'
ARQUIVO_PASSAGENS_COMṔRADAS = 'passagens.json'

# Função para calcular valor de um caminho (a cada 100km soma 115 reais)
def soma_valor(km):
    valor = (km / 100) * 115
    return round(valor, 2)

# Função para exibir em tela se teste de conexão com cliente deu bom
def verifica_teste(teste, print_msg):
    if teste:
        print(print_msg)

# Função para quando abrir servidor, carregar ou criar o grafo
def cria_arquivo_grafo():
    # Carregando o grafo a partir do arquivo JSON
    try:
        G = carregar_grafo()
        print("Grafo carregado com sucesso.")
    
    except FileNotFoundError:
        print("Arquivo não encontrado. Criando um novo grafo.")
        
        # Criando um novo grafo e salvando
        G = nx.DiGraph()

        # Caminhos de Cuiabá
        G.add_edge("Cuiabá", "Goiânia", distancia=890, assentos=3, cpf=[])
        G.add_edge("Cuiabá", "Campo Grande", distancia=700, assentos=3, cpf=[])

        # Caminhos de Goiânia
        G.add_edge("Goiânia", "Cuiabá", distancia=890, assentos=3, cpf=[])
        G.add_edge("Goiânia", "Campo Grande", distancia=840, assentos=3, cpf=[])
        G.add_edge("Goiânia", "Belo Horizonte", distancia=890, assentos=3, cpf=[])

        # Caminhos de Campo Grande
        G.add_edge("Campo Grande", "Cuiabá", distancia=700, assentos=3, cpf=[])
        G.add_edge("Campo Grande", "Goiânia", distancia=840, assentos=3, cpf=[])
        G.add_edge("Campo Grande", "Belo Horizonte", distancia=1250, assentos=3, cpf=[])
        G.add_edge("Campo Grande", "São Paulo", distancia=980, assentos=3, cpf=[])
        G.add_edge("Campo Grande", "Curitiba", distancia=1000, assentos=3, cpf=[])

        # Caminhos de Belo Horizonte
        G.add_edge("Belo Horizonte", "Goiânia", distancia=890, assentos=3, cpf=[])
        G.add_edge("Belo Horizonte", "Vitória", distancia=510, assentos=3, cpf=[])
        G.add_edge("Belo Horizonte", "Campo Grande", distancia=1250, assentos=3, cpf=[])
        G.add_edge("Belo Horizonte", "São Paulo", distancia=585, assentos=3, cpf=[])
        G.add_edge("Belo Horizonte", "Rio de Janeiro", distancia=440, assentos=3, cpf=[])

        # Caminhos de Vitória
        G.add_edge("Vitória", "Belo Horizonte", distancia=510, assentos=3, cpf=[])
        G.add_edge("Vitória", "Rio de Janeiro", distancia=520, assentos=3, cpf=[])

        # Caminhos de São Paulo
        G.add_edge("São Paulo", "Belo Horizonte", distancia=585, assentos=3, cpf=[])
        G.add_edge("São Paulo", "Campo Grande", distancia=980, assentos=3, cpf=[])
        G.add_edge("São Paulo", "Rio de Janeiro", distancia=440, assentos=3, cpf=[])
        G.add_edge("São Paulo", "Curitiba", distancia=400, assentos=3, cpf=[])

        # Caminhos de Rio de Janeiro
        G.add_edge("Rio de Janeiro", "Vitória", distancia=520, assentos=3, cpf=[])
        G.add_edge("Rio de Janeiro", "Belo Horizonte", distancia=440, assentos=3, cpf=[])
        G.add_edge("Rio de Janeiro", "São Paulo", distancia=440, assentos=3, cpf=[])

        # Caminhos de Curitiba
        G.add_edge("Curitiba", "Campo Grande", distancia=1000, assentos=3, cpf=[])
        G.add_edge("Curitiba", "São Paulo", distancia=400, assentos=3, cpf=[])
        G.add_edge("Curitiba", "Florianópolis", distancia=300, assentos=3, cpf=[])

        # Caminhos de Florianópolis
        G.add_edge("Florianópolis", "Curitiba", distancia=300, assentos=3, cpf=[])
        G.add_edge("Florianópolis", "Porto Alegre", distancia=460, assentos=3, cpf=[])

        # Caminhos de Porto Alegre
        G.add_edge("Porto Alegre", "Florianópolis", distancia=460, assentos=3, cpf=[])

        # Estrutura é parecida com isso
        # { 
        #   ("São Paulo", "Rio de Janeiro") : {'distancia': 980, 'assentos': 3, 'cpf': []}
        #   ("Vitória", "Curitiba") : {'distancia': 34, 'assentos': 3, 'cpf': []}
        #   ...
        # }

        # É um dicionário geral que armazena todas as conexões (grafo)
        # As chaves desse dicionário são tuplas que armazenam a v1 e v2 (cidades com conexão)
        # Os valores dessas chaves são dicionários, onde as chaves serão as distancias, assentos e cpf. Os valores
        # dessas chaves são as informações desses dados
        salvar_grafo(G)

# Função que carrega um grafo do arquivo
def carregar_grafo():
    # Abre arquivo e retorna os dados do grafo
    with open(ARQUIVO_GRAFO, 'r') as arq:
        dados_existentes = json.load(arq)
    
    # Cria novo grafo para armazenar dados do grafo retornado
    grafo = nx.DiGraph()

    # Salva cada trecho no grafo
    for trecho in dados_existentes['trecho']:
        grafo.add_edge(
            trecho['v1'], trecho['v2'], 
            distancia = trecho['distancia'], 
            assentos = trecho['assentos'],
            cpf = trecho['cpf']
        )
    
    return grafo

# Função que carrega todas as passagens compradas no sistema
def carregar_passagens_compradas():
    try:
        with open(ARQUIVO_PASSAGENS_COMṔRADAS, 'r') as arq:
            # Retorna dicionário (cpf são as chaves)
            return json.load(arq)
        
    except FileNotFoundError:
        # Retorna um dicionário vazio se o arquivo não existir (não teve nenhuma compra ainda)
        return {}

# Função que salva um grafo no arquivo (atualiza)
def salvar_grafo(grafo_att):
    # Novo _att a ser salvo em arquivo
    dados_novos = {'trecho': []}

    # Salva novos dados de cada trecho (atualiza na lista de cada trecho. LISTA = informações como distancia e etc)
    for v1, v2, atributos in grafo_att.edges(data=True):
        dados_novos['trecho'].append({
            'v1': v1,
            'v2': v2,
            'distancia': atributos['distancia'],
            'assentos': atributos['assentos'],
            'cpf': atributos['cpf']
        })

    # Salva novo grafo em arquivo
    with open(ARQUIVO_GRAFO, 'w') as arq:
        json.dump(dados_novos, arq, indent=4)

# Função que salva um dicionário no arquivo (atualiza)
def salvar_passagem_comprada(dicionario_att):
    with open(ARQUIVO_PASSAGENS_COMṔRADAS, 'w') as arq:
        json.dump(dicionario_att, arq, indent=4)

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

# Função para verificar se existe compras em um CPF
def verifica_compras_cpf(cpf):
    # Carrega todas as compras do sistema
    compras = carregar_passagens_compradas()

    if cpf in compras:
        print("Achei passagens")
        return compras[cpf]
    
    else:
        print("Não achei passagens")
        return []

# Função para registrar nova compra de passagem em um CPF
# ps: É um dicionário geral onde a chave vai ser o CPF e o valor de cada CPF vai ser uma lista
# A cada nova compra em um CPF, é adicionado um dicionário nessa lista, logo é uma lista de dicionários
def registra_compra(cpf, caminho, distancia, assentos):
    # Carrega todas as compras do sistema
    compras =  carregar_passagens_compradas()

    # Cria uma nova compra
    # ps: caminho = lista contendo cidades que monta o caminho
    #     assentos = lista contendo númeração dos assentos em cada trecho que forma o caminho
    #     distancia = inteiro numero em km da distancia total do caminho (soma dos trechos)
    #     valor = inteiro indicando valor do caminho
    compra_att = {"caminho": caminho, "assentos": assentos, "distancia": distancia, "valor": soma_valor(distancia)}
    
    # Se já existir uma compra no cpf, adiciona nova compra no cpf (mais um dicionário a lista)
    if cpf in compras:
        compras[cpf].append(compra_att)
    
    # Se não existir, cria uma nova chave no dicionário geral
    else:
        compras[cpf] = [compra_att]

    # Salva dicionário atualizado no arquivo
    salvar_passagem_comprada(compras)

# Função para verificar se caminho escolhido pelo cliente ainda está disponível (compara com o arquivo atual)
def verifica_caminho_escolhido(G, caminho):
    comprar = True

    for i in range(len(caminho[1]) - 1):
        trecho = (caminho[1][i], caminho[1][i + 1])

        # Se algum trecho do caminho escolhido pelo cliente não tiver mais assento, caminho ta indisponível
        if G[trecho[0]][trecho[1]]['assentos'] == 0:
            comprar = False
            break
    
    return comprar

# Função para registrar compra de um caminho (atualiza grafo e salva compra de passagem)
def registra_caminho_escolhido(G, caminho, cpf):
    # Número do assento em cada trecho
    assentos = []
    
    # Passa por cada trecho do caminho, desconta um assento e registra CPF de quem comprou o assento
    for i in range(len(caminho[1]) - 1):
        trecho = (caminho[1][i], caminho[1][i + 1])
        G[trecho[0]][trecho[1]]['assentos'] -= 1
        G[trecho[0]][trecho[1]]['cpf'].append(cpf)

        # Adiciona número de assento referente a posição do cpf na lista de cada trecho
        # Se um trecho tem 3 cpf's, o tamanho da sua lista é 3, logo o número do assento do ultimo cpf adicionado é 3
        assentos.append(len(G[trecho[0]][trecho[1]]['cpf']))
    
    salvar_grafo(G)

    # Atualiza dicionário com nova passagem comprada e salva em arquivo
    # ps: caminho[1] = lista com cidades (trechos), caminho[0] = distancia total do caminho (soma dos trechos)
    registra_compra(cpf, caminho[1], caminho[0], assentos)
