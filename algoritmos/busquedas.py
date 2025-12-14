"""
Implementa algoritmos de búsqueda de caminos
"""

from heapq import heappush, heappop
from collections import deque


class Busquedas:
    def __init__(self, mapa_juego):
        self.mapa = mapa_juego
        self.visitados = set()
        self.frontera = []
        self.vino_de = {}
        self.costo_hasta_ahora = {}

    def heuristica(self, a, b):
        """Heurística Manhattan para A*"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_estrella(self, inicio, meta):
        """Algoritmo A* - devuelve camino, nodos visitados y frontera"""
        self.visitados = set()
        self.frontera = []
        self.vino_de = {}
        self.costo_hasta_ahora = {}

        heappush(self.frontera, (0, inicio))
        self.vino_de[inicio] = None
        self.costo_hasta_ahora[inicio] = 0

        orden_visitados = []
        estados_frontera = []

        while self.frontera:
            prioridad_actual, actual = heappop(self.frontera)

            if actual in self.visitados:
                continue

            self.visitados.add(actual)
            orden_visitados.append(actual)
            estados_frontera.append([nodo for _, nodo in self.frontera])

            if actual == meta:
                break

            for siguiente_nodo in self.mapa.obtener_vecinos(*actual):
                nuevo_costo = self.costo_hasta_ahora[actual] + self.mapa.obtener_costo(*siguiente_nodo)

                if siguiente_nodo not in self.costo_hasta_ahora or nuevo_costo < self.costo_hasta_ahora[siguiente_nodo]:
                    self.costo_hasta_ahora[siguiente_nodo] = nuevo_costo
                    prioridad = nuevo_costo + self.heuristica(siguiente_nodo, meta)
                    heappush(self.frontera, (prioridad, siguiente_nodo))
                    self.vino_de[siguiente_nodo] = actual

        camino = self._reconstruir_camino(inicio, meta)
        costo_total = self.costo_hasta_ahora.get(meta, float('inf'))

        return camino, orden_visitados, estados_frontera, costo_total

    def greedy(self, inicio, meta):
        """Búsqueda Ávida (Greedy Best-First Search)"""
        self.visitados = set()
        self.frontera = []
        self.vino_de = {}

        heappush(self.frontera, (0, inicio))
        self.vino_de[inicio] = None

        orden_visitados = []
        estados_frontera = []

        while self.frontera:
            _, actual = heappop(self.frontera)

            if actual in self.visitados:
                continue

            self.visitados.add(actual)
            orden_visitados.append(actual)
            estados_frontera.append([nodo for _, nodo in self.frontera])

            if actual == meta:
                break

            for siguiente_nodo in self.mapa.obtener_vecinos(*actual):
                if siguiente_nodo not in self.vino_de:
                    # Solo usa heurística (diferencia clave con A*)
                    prioridad = self.heuristica(siguiente_nodo, meta)
                    heappush(self.frontera, (prioridad, siguiente_nodo))
                    self.vino_de[siguiente_nodo] = actual

        camino = self._reconstruir_camino(inicio, meta)

        # Calcular el coste real del camino
        costo_total = 0
        if camino:
            for i in range(len(camino) - 1):
                costo_total += self.mapa.obtener_costo(*camino[i + 1])

        return camino, orden_visitados, estados_frontera, costo_total

    def bfs(self, inicio, meta):
        """Búsqueda en Amplitud (BFS)"""
        self.visitados = set()
        self.frontera = deque([inicio])
        self.vino_de = {inicio: None}

        orden_visitados = []
        estados_frontera = []

        while self.frontera:
            actual = self.frontera.popleft()

            if actual in self.visitados:
                continue

            self.visitados.add(actual)
            orden_visitados.append(actual)
            estados_frontera.append(list(self.frontera))

            if actual == meta:
                break

            for siguiente_nodo in self.mapa.obtener_vecinos(*actual):
                if siguiente_nodo not in self.vino_de:
                    self.frontera.append(siguiente_nodo)
                    self.vino_de[siguiente_nodo] = actual

        camino = self._reconstruir_camino(inicio, meta)

        # Calcular coste real del camino BFS
        costo_total = 0
        if camino:
            for i in range(len(camino) - 1):
                costo_total += self.mapa.obtener_costo(*camino[i + 1])

        return camino, orden_visitados, estados_frontera, costo_total

    def _reconstruir_camino(self, inicio, meta):
        """Reconstruye el camino desde la meta hasta el inicio"""
        if meta not in self.vino_de:
            return []

        camino = []
        actual = meta
        while actual is not None:
            camino.append(actual)
            actual = self.vino_de[actual]
        camino.reverse()
        return camino