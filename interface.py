from utils_client import imprime_divisoria, soma_valor

# Função que exibe em tela menu principal e suas opções
def mostrar_menu_principal():
    imprime_divisoria()
    print("\t\t\t\t\tSistema de Vendas de Passagens")
    imprime_divisoria()

    while True:
        escolha = input("1- Comprar\n2- Minhas compras\n0- Encerrar programa\n\n>>> ")
        if escolha in ['0', '1', '2']:
            break
        print("Entrada inválida.")
    
    return escolha

# Função que exibe em tela menu de escolha de origem e destino
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
    
    if origem in ["0", "100"]:
        return origem, None

    while True:
        destino = input("Escolha o número referente à cidade destino: ")
        if destino.isdigit() and (0 <= int(destino) <= 10 or int(destino) == 100) and origem != destino:
            break
        print("Entrada inválida.")
    
    return origem, destino

# Função que exibe em tela caminhos encontrados de origem a destino
def selecionar_caminho(cidades, origem, destino, caminhos):
    imprime_divisoria()
    
    print(f"Trechos de {cidades[int(origem)-1]} para {cidades[int(destino)-1]}:\n")
    for i, (dist, path) in enumerate(caminhos):
        print(f"{i+1}. Caminho: {' -> '.join(path)} | {dist}km | R$ {soma_valor(dist)}\n")
    print("0- Encerrar programa\n100- Menu\n")

    while True:
        escolha = input("Escolha um caminho: ")
        if escolha.isdigit() and (0 <= int(escolha) <= len(caminhos) or int(escolha) == 100):
            break
        print("Entrada inválida.")

    if escolha in ["0", "100"]:
        return escolha, None
    
    while True:
        cpf = input("Digite seu CPF para registro da compra (apenas os números): ")
        if cpf.isdigit() and int(cpf) > 100:
            break
        print("Entrada inválida. Apenas números maiores que 100!")
    
    return escolha, cpf

# Função que exibe em tela menu de escolha de cpf para ter acesso as passagens compradas
def verificar_passagens_compradas():
    imprime_divisoria()
    print("0- Encerrar programa\n100- Menu\n")

    while True:
        cpf = input("Digite seu CPF para consultar passagens compradas (apenas os números): ")
        if cpf.isdigit() and (int(cpf) == 0 or int(cpf) >= 100):
            break
        print("Entrada inválida.")
    
    return cpf

# Função que exibe em tela compras de passagens encontradas de um CPF
def exibe_compras_cpf(cpf, passagens):
    imprime_divisoria()
    print(f"Compras do CPF {cpf}: \n")

    # Exibe todas as compras associadas a um CPF
    for i, compra in enumerate(passagens, 1):
        # Exibe caminho (todos os trechos), distancia total e valor
        print(f"Compra {i}: {' -> '.join(compra["caminho"])} | {compra["distancia"]}km | R$ {compra["valor"]}")

        # Exibe número do assento de cada trecho do caminho
        for i in range(len(compra["assentos"])):
            print(f"{i+1}.Trecho {compra["caminho"][i]} -> {compra["caminho"][i+1]}: Assento -> {compra["assentos"][i]}")
        
        print("")

    while True:
        escolha = input("0- Encerrar programa\n100- Menu\n\n>>> ")
        if escolha in ['0', '100']:
            break
        print("Entrada inválida.")
    
    return escolha