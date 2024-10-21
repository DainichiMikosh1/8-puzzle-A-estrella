import numpy as np

class Tablero:
    def __init__(self, estado, padre=None, operador=None, profundidad=0, costo_g=0):
        self.padre = padre
        self.estado = np.array(estado)
        self.operador = operador
        self.profundidad = profundidad  # g(n): costo desde el inicio hasta este nodo
        self.costo_g = costo_g  # g(n)
        self.costo_h = self.calcular_heuristica()  # h(n)
        self.costo_f = self.costo_g + self.costo_h  # f(n) = g(n) + h(n)
        self.cero = self.encontrar_cero()
    
    def __lt__(self, otro):
        return self.costo_f < otro.costo_f

    def __str__(self):
        return str(self.estado[:3]) + '\n' \
               + str(self.estado[3:6]) + '\n' \
               + str(self.estado[6:]) + '\n' \
               + f"g(n): {self.costo_g}, h(n): {self.costo_h}, f(n): {self.costo_f}\n"

    def prueba_objetivo(self):
        return np.array_equal(self.estado, self.estado_objetivo)

    def encontrar_cero(self):
        return np.where(self.estado == 0)[0][0]

    def calcular_heuristica(self):
        # Distancia Manhattan
        distancia = 0
        for indice_actual, valor in enumerate(self.estado):
            if valor != 0:
                indice_objetivo = np.where(self.estado_objetivo == valor)[0][0]
                distancia += abs(indice_actual // 3 - indice_objetivo // 3) + abs(indice_actual % 3 - indice_objetivo % 3)
        return distancia

    estado_objetivo = np.array([1, 2, 3, 4, 5, 6, 7, 8, 0])  # Estado objetivo

    def generar_hijos(self):
        hijos = []
        movimientos = [('Arriba', -3), ('Abajo', 3), ('Izquierda', -1), ('Derecha', 1)]
        for operador, movimiento in movimientos:
            indice_cero = self.cero
            indice_nuevo = indice_cero + movimiento
            if self.es_movimiento_valido(indice_cero, indice_nuevo):
                nuevo_estado = self.estado.copy()
                nuevo_estado[indice_cero], nuevo_estado[indice_nuevo] = nuevo_estado[indice_nuevo], nuevo_estado[indice_cero]
                hijo = Tablero(
                    nuevo_estado,
                    padre=self,
                    operador=operador,
                    profundidad=self.profundidad + 1,
                    costo_g=self.costo_g + 1  # Costo del movimiento
                )
                hijos.append(hijo)
        return hijos

    def es_movimiento_valido(self, indice_cero, indice_nuevo):
        if indice_nuevo < 0 or indice_nuevo >= 9:
            return False
        if indice_cero % 3 == 0 and indice_nuevo % 3 == 2:
            return False  # Evitar moverse de la primera columna a la ultima
        if indice_cero % 3 == 2 and indice_nuevo % 3 == 0:
            return False  # Evitar moverse de la ultima columna a la primera
        return True

    def __eq__(self, otro):
        return np.array_equal(self.estado, otro.estado)

    def __hash__(self):
        return hash(tuple(self.estado))
    