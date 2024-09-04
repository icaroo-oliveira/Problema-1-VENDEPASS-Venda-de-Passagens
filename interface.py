from utils import imprime_divisoria

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
        return origem, destino

    while True:
        destino = input("Escolha o número referente à cidade destino: ")
        if destino.isdigit() and (0 <= int(destino) <= 10 or int(destino) == 100):
            break
        print("Entrada inválida.")
    
    return origem, destino