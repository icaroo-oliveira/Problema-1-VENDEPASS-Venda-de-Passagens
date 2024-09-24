import os
import platform
import time

cidades = ["Cuiabá", "Goiânia", "Campo Grande", "Belo Horizonte", "Vitória", 
            "São Paulo", "Rio de Janeiro", "Curitiba", "Florianópolis", "Porto Alegre"]

# Função para limpar terminal (reconhece qual SO utilizado)
def clear_terminal():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

# Função para calcular valor de um caminho (a cada 100km soma 115 reais)
# Parâmetros ->     km: quilometragem total de um caminho
# Retorno ->        valor: preço daquele caminho
def soma_valor(km):
    valor = (km / 100) * 115
    return round(valor, 2)

# Função para melhorar frontend
def imprime_divisoria():
    print("\n" + "=" * 120 + "\n")

# Função para limpar terminal após n segundos
# Parâmetros ->     segundos: segundos que o programa deve congelar
# Retorno ->        Sem retorno
def sleep_clear(segundos):
    time.sleep(segundos)
    clear_terminal()
