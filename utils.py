import os
import platform
import time

def clear_terminal():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def soma_valor(km):
    valor = (km / 100) * 115
    return round(valor, 2)

def imprime_divisoria():
    print("\n" + "=" * 120 + "\n")

# Sleep de n segundos e limpa tela
def sleep_clear(segundos):
    time.sleep(segundos)
    clear_terminal()
