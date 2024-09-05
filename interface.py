from utils import imprime_divisoria, soma_valor

def mostrar_menu_principal():
    imprime_divisoria()
    print("\t\t\t\t\tSistema de Vendas de Passagens")
    imprime_divisoria()
    escolha = input("1- Comprar\n0- Encerrar programa\n\n>>> ")

    while escolha not in ['1', '0']:
        print("Entrada inválida.")
        escolha = input("\n1- Comprar\n0- Encerrar programa\n>>> ")
    
    return escolha

def selecionar_cidades(cidades):
    imprime_divisoria()
    print("Cidades disponíveis:\n")
    for i, cidade in enumerate(cidades):
        print(f"{i+1}- {cidade}")
    print("\n0- Encerrar programa\n100- Menu\n")
    
    while True:
        origem = input("Escolha o número referente à cidade origem: ")
        if origem.isdigit() and (0 <= int(origem) <= 10 or int(origem) == 100):
            break
        print("Entrada inválida.")
    
    if origem == "0" or origem == "100":
        return origem, None

    while True:
        destino = input("Escolha o número referente à cidade destino: ")
        if destino.isdigit() and (0 <= int(destino) <= 10 or int(destino) == 100) and origem != destino:
            break
        print("Entrada inválida.")
    
    return origem, destino

def selecionar_caminho(cidades, origem, destino, caminhos):
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
    
    return escolha