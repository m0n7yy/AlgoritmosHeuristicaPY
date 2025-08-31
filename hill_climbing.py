"""
    Edgar Sebastian Montalvo Duran
    Fundamentos de inteligencia artificial
    05/09/2025
    Algiritmos de busqueda Heuristica
"""

from queue import PriorityQueue

#Definimos el nodo
class Nodo:
    def __init__(self, estado, padre=None, costo=0, heuristica=0):
        self.estado = estado
        self.padre = padre
        self.costo = costo
        self.heuristica = heuristica

    def __lt__(self, otro):
        return (self.costo + self.heuristica) < (otro.costo + otro.heuristica)

def hill_climbing(estado_inicial, estado_meta, obtener_vecinos, calcular_heuristica):
    cola_prioridad = PriorityQueue()
    visitados = set()

    nodo_inicial = Nodo(
        estado=estado_inicial,
        heuristica=calcular_heuristica(estado_inicial,estado_meta)
    )

    cola_prioridad.put(nodo_inicial)

    while not cola_prioridad.empty():
        nodo_actual = cola_prioridad.get()

        if nodo_actual.estado == estado_meta:
            return reconstruir_camino(nodo_actual)
        
        visitados.add(nodo_actual.estado)

        for estado_vecino, costo in obtener_vecinos(nodo_actual.estado):
            if estado_vecino not in visitados:
                nuevo_costo = nodo_actual.costo + costo
                nueva_heuristica = calcular_heuristica(estado_vecino, estado_meta)

                nodo_vecino = Nodo(
                    estado = estado_vecino,
                    padre = nodo_actual,
                    costo = nuevo_costo,
                    heuristica = nueva_heuristica
                )
                cola_prioridad.put(nodo_vecino)
    return None
        
def reconstruir_camino(nodo):
    camino = []
    while nodo:
        camino.append(nodo.estado)
        nodo = nodo.padre
    return list(reversed(camino))

grafo = {
        'A': [('C', 3)],
        'B': [('A', 4), ('D', 5), ('E',2)],
        'C': [('F',6)],
        'D': [('G', 2)],
        'E': [('G', 5)],
        'F': [],
        'G': [('F',4)]
}    

def obtener_vecinos(nodo):
    return grafo[nodo]

# Función heurística: Distancia estimada mínima al nodo objetivo
def calcular_heuristica(nodo_actual, nodo_objetivo):
    distancias_minimas = {
        'A': 9,  # A -> C -> F (3+6)
        'B': 6,  # B -> E -> G -> F (2+5+4) no es mínima, pero es una estimación
        'C': 6,  # C -> F
        'D': 6,  # D -> G -> F (2+4)
        'E': 9,  # E -> G -> F (5+4)
        'G': 4,  # G -> F
        'F': 0   # Ya está en el objetivo
    }
    return distancias_minimas.get(nodo_actual, 0)

if __name__ == "__main__":
    estado_inicial = 'B'
    estado_meta = 'F'

    camino = hill_climbing(estado_inicial,estado_meta,obtener_vecinos,calcular_heuristica)
    if camino:
        print(" ","->".join(camino))
        costo_total = 0
        for i in range(len(camino)-1):
            actual=camino[i]
            siguiente = camino[i+1]
            for vecino, costo in grafo[actual]:
                if vecino == siguiente:
                    costo_total += costo
                    break
        print(" ",costo_total)
    else:
        print("XD")