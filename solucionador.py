from abc import ABC, abstractmethod

class Solucionador(ABC):
    solucion = None
    frontera = None
    nodos_expandidos = 0
    max_profundidad = 0
    nodos_explorados = set()
    estado_inicial = None

    def __init__(self, estado_inicial):
        self.estado_inicial = estado_inicial

    def cadena_ancestral(self):
        actual = self.solucion
        cadena = [actual]
        while actual.padre is not None:
            cadena.append(actual.padre)
            actual = actual.padre
        return cadena

    @property
    def camino(self):
        camino = [nodo.operador for nodo in self.cadena_ancestral()[-2::-1]]
        return camino

    @abstractmethod
    def resolver(self):
        pass

    def establecer_solucion(self, tablero):
        self.solucion = tablero
        self.nodos_expandidos = len(self.nodos_explorados) - len(self.frontera) - 1
    
    def cadena_estados(self):
        cadena = []
        actual = self.solucion
        while actual is not None:
            cadena.append(actual.estado)
            actual = actual.padre
        cadena.reverse()
        return cadena
