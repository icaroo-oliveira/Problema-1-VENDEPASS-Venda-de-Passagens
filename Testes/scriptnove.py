import subprocess
import time
import threading

client_script = "client.py"

escolhas = ['1', '1', '2', '1', '213213213']

def abrir_terminal(escolhas):
    escolha_str = ' '.join(escolhas)
    comando = f'gnome-terminal -- bash -c "python3 {client_script} {escolha_str}; exec bash"'
    
    print(f"Executando comando: {comando}")

    # Executa o comando no sistema
    subprocess.Popen(comando, shell=True)

# Número de clientes/terminais
num_clients = 5

# Abrindo múltiplos terminais com os mesmos parâmetros
for i in range(num_clients):
    client_thread = threading.Thread(target=abrir_terminal, args=(escolhas,))
    client_thread.start()
    
   
