import subprocess
import time
import threading

client_script = "cliente_teste.py"
#se liga em cima, se der erro puxa pra fora o arquivo pra fora da pasta teste (se ele tiver dentro)
cont=111111111111111
cont2 = 1
cont3 = 2


def abrir_terminal(escolhas):
    escolha_str = ' '.join(escolhas)
    #comando = f'gnome-terminal -- bash -c "python3 {client_script} {escolha_str}; exec bash"'
    comando = f'start cmd /k python {client_script} {escolha_str}'

    print(f"Executando comando: {comando}")

    # Executa o comando no sistema
    subprocess.Popen(comando, shell=True)

# Número de clientes/terminais
num_clients = 2

# Abrindo múltiplos terminais com os mesmos parâmetros
for i in range(num_clients):
    
    escolhas = ['1', str(cont2), str(cont3), '1', str(cont)]

    #client_thread = threading.Thread(target=abrir_terminal, args=(escolhas,))
    #client_thread.start()
    abrir_terminal(escolhas)
    cont+=1
    cont2+=1
    cont3+=1
    
   
