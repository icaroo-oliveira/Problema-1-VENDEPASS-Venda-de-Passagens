class Grafo:
    def __init__(self):
        self.grafo = {}

    def adicionar_no(self, no):
        if no not in self.grafo:
            self.grafo[no] = []

    def adicionar_aresta(self, no1, no2):
        if no1 not in self.grafo:
            self.adicionar_no(no1)
        if no2 not in self.grafo:
            self.adicionar_no(no2)
        self.grafo[no1].append(no2)
        self.grafo[no2].append(no1)

    def exibir_grafo(self):
        for no, arestas in self.grafo.items():
            print(f"{no} -> {arestas}")




g = Grafo()
g.adicionar_no(1)
g.adicionar_no(2)
g.adicionar_aresta(1, 2)
g.adicionar_aresta(2, 3)

g.exibir_grafo()
