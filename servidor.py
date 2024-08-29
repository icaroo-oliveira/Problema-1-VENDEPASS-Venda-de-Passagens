import socket
from modelos.rotas import Rota_unica,Rotas
import json

def lendo():
    with open('modelos/rotas.json', 'r') as arquivo:
        dados_existentes = json.load(arquivo)
        return dados_existentes


def salvar_em_json(i):
        with open('modelos/rotas.json', 'w') as arquivo_json:
            json.dump(i, arquivo_json, indent=4)


def start_server():

    # Cria um socket TCP/IP
    # 1- Define ipv4
    # 2- Socket do tipo TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Liga o socket a um endereço e porta
    server_address = ('localhost', 65435)
    server_socket.bind(server_address)

    # Servidor aguarda por conexões
    server_socket.listen(1)
    print("Aguardando conexão...")

    # Espera por uma conexão
    # Bloqueia a execução do programa até alguém se conectar
    # Retorna socket do cliente e seu endereço IP
    connection, client_address = server_socket.accept()
    
    try:
        print(f"Conectado a {client_address}")

        while True:

            data = connection.recv(1024)
            
            if data:
                print(f"Recebido: {data.decode('utf-8')}")

                dados = lendo()
                
               
                for item in dados[data.decode('utf-8')]:
                    cont=0
                    for trecho in dados[data.decode('utf-8')][item]:
                       
                        if(trecho['assentos']>0):
                            cont+=1

                    if cont==len(dados[data.decode('utf-8')][item]):
                        print(f"caminhos disponíveis: ", dados[data.decode('utf-8')][item])
                        message = "available"

                #salvando o dado do lugar
                lugar = data.decode('utf-8')
                connection.sendall(message.encode('utf-8'))



                data = connection.recv(1024)

                #se n tinha problema com os trechos
                if data:
                    
                    if data.decode('utf-8')!='999':

                        for num,item in enumerate(dados[lugar][data.decode('utf-8')]):

                            rota = Rota_unica.from_dict(item)
                            rota.compra_passagem()
                            dados[lugar][data.decode('utf-8')][num]=rota.to_dict()
                            
                        

                        salvar_em_json(dados)


                        message = "acquired"
                        
                        connection.sendall(message.encode('utf-8'))

                        
                else:
                    message = "weve ran out of tickets! good luck next time"
                    connection.sendall(message.encode('utf-8'))


                    

            
            # Cliente encerrou a conexão
            else:
                print("Não há mais dados de", client_address)
                break
    finally:
        # Fecha a conexão
        connection.close()

if __name__ == "__main__":
    start_server()

#e
