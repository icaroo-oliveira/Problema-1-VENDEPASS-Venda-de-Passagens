import subprocess
import time


client_script = "client.py"  


escolhas = ['1', '1', '2', '1', '0000000000']


def abrir_terminal(escolhas):
    
    escolha_str = ' '.join(escolhas)  
    comando = f'start cmd /k python {client_script} {escolha_str}'

    
    print(f"Executando comando: {comando}")

    # Executa o comando no sistema
    subprocess.Popen(comando, shell=True)

# Número de clientes/terminais 
num_clients = 4

# abrindo múltiplos terminais com mesmos parâmetros
for i in range(4):
    abrir_terminal(escolhas)  
   
