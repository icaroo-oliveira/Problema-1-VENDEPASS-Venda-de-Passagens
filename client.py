import json
import os

class Rota_unica:
    def __init__(self,ligacao,peso):
        self.ligacao = ligacao
        self.assentos = 5
        self.peso=peso


    
    def compra_passagem(self):
        if self.assentos>=1:
            self.assentos=self.assentos - 1
        else:
            print("cabou se !! \n tente mais na próxima vez, pobre diabo sem fortuna !!")

    def to_dict(self):
        return {
            'rota': self.rota,
            'assentos': self.assentos,
            'peso':self.peso
        }
    
    @classmethod
    def from_dict(cls, dicionario):

        instancia = cls(dicionario['rota'])
        instancia.assentos = dicionario['assentos']
        instancia.peso = dicionario['peso']
        return instancia



class No:
    def __init__(self,nome_inicio,lista):
        self.inicio = nome_inicio
        self.ligacoes = lista
        self.adicione_Rota_Unica()



    def adicione_Rota_Unica(self):
         
        for num,item in enumerate(self.ligacoes):
             rota = Rota_unica(self.inicio + '-' + item,1)
         





        


