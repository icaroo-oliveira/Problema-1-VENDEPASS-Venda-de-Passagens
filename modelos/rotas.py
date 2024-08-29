import json
import os

class Rota_unica:
    def __init__(self, rota):
        self.rota = rota
        self.assentos = 5
    
    def compra_passagem(self):
        if self.assentos>=1:
            self.assentos=self.assentos - 1
        else:
            print("cabou se !! \n tente mais na próxima vez, pobre diabo sem fortuna !!")

    def to_dict(self):
        return {
            'rota': self.rota,
            'assentos': self.assentos
        }
    
    @classmethod
    def from_dict(cls, dicionario):

        instancia = cls(dicionario['rota'])
        instancia.assentos = dicionario['assentos']
        return instancia






class Rotas:
    def __init__(self, rota, lista):
        self.rota = rota
        self.contagem_rotas = 0
        self.trajeto = self.quebrando(lista)
        



    def quebrando(self, lista):
        caminho_json = 'modelos/rotas.json'

        if not os.path.exists(caminho_json):
            dados_existentes = {}
        else:
            try:
                with open(caminho_json, 'r') as arquivo:
                    dados_existentes = json.load(arquivo)
                    
            except json.JSONDecodeError:
                dados_existentes = {}  
            except FileNotFoundError:
                dados_existentes = {}  

      

        if self.rota not in dados_existentes:
            dados_existentes[self.rota] = {}

        dic = {}
        self.contagem_rotas = len(dados_existentes[self.rota])
        for num, item in enumerate(lista):
            if num == len(lista) - 1:
                break

            if num == 0:
    
                dados_existentes[self.rota][self.contagem_rotas]=[]
                        
            rota = lista[num] + '-' + lista[num + 1]
            uniq_route = Rota_unica(rota)

            dados_existentes[self.rota][self.contagem_rotas].append(uniq_route.to_dict())


        with open(caminho_json, 'w') as arquivo:
            json.dump(dados_existentes, arquivo, indent=4)



# rotas = Rotas("Salvador-Recife", ["Salvador", "Aracaju", "Maceió", "Recife"])
# rotas1 = Rotas("Recife-Fortaleza", ["Recife", "Aracaju","Maceió", "Fortaleza"])

# rotas2 = Rotas("Salvador-Recife", ["Salvador", "Aracaju", "biritinga", "Recife"])
# rotas3 = Rotas("Recife-Fortaleza", ["Recife", "Aracaju","serrinha", "Fortaleza"])