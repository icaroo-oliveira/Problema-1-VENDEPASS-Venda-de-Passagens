import subprocess
import time
import threading

client_script = "client.py"  


escolhas = ['1', '1', '2', '1', '0000000000']

#isso tudo é uma viagem, kkkkkk é sério...
def abrir_terminal(escolhas):
    
    escolha_str = ' '.join(escolhas)  
    comando = f'start cmd /k python {client_script} {escolha_str}'

    
    print(f"Executando comando: {comando}")

    # Executa o comando no sistema
    subprocess.Popen(comando, shell=True)

# Número de clientes/terminais 
num_clients = 5

# abrindo múltiplos terminais com mesmos parâmetros
for i in range(num_clients):
    abrir_terminal(escolhas) 
        
    # client_thread = threading.Thread(target=abrir_terminal, args=(escolhas,))
    # client_thread.start()

    #time.sleep(1) 
   
