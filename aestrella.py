from solucionador import Solucionador
import heapq

class AEstrella(Solucionador):
    def resolver(self):
        self.frontera = []
        heapq.heappush(self.frontera, self.estado_inicial)
        self.nodos_explorados = set()
        self.max_profundidad = 0
        self.arbol = []  # Lista para almacenar las relaciones del árbol

        while self.frontera:
            estado_actual = heapq.heappop(self.frontera)

            if estado_actual.prueba_objetivo():
                self.establecer_solucion(estado_actual)
                return

            self.nodos_explorados.add(estado_actual)

            hijos = estado_actual.generar_hijos()
            for hijo in hijos:
                if hijo not in self.nodos_explorados:
                    heapq.heappush(self.frontera, hijo)
                    if hijo.profundidad > self.max_profundidad:
                        self.max_profundidad = hijo.profundidad
                    # Agregar relacion padre-hijo al arbol
                    self.arbol.append((estado_actual, hijo))

        # Si no se encuentra solucion
        messagebox.showerror("Sin solución", "No se encontró una solución al puzzle.")
