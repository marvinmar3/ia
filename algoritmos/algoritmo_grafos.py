"""
Implementa algoritmos de grafos (Prim, Kruskal, detección de ciclos)
"""

import random
from heapq import heappush, heappop


class AlgoritmosGrafo:
    def __init__(self, mapa_juego):
        self.mapa = mapa_juego

    def prim_mst(self):
        """Algoritmo de Prim para Árbol de Expansión Mínima"""
        # Comenzar desde una celda aleatoria no-montaña
        celdas_validas = [(i, j) for i in range(self.mapa.size)
                          for j in range(self.mapa.size)
                          if self.mapa.grid[i, j] != 'MONTAÑA']

        if not celdas_validas:
            return [], 0

        inicio = random.choice(celdas_validas)
        visitados = {inicio}
        aristas = []
        monticulo_aristas = []

        # Añadir aristas iniciales
        for vecino in self.mapa.obtener_vecinos(*inicio):
            costo = self.mapa.obtener_costo(*vecino)
            heappush(monticulo_aristas, (costo, inicio, vecino))

        costo_total = 0

        while monticulo_aristas and len(visitados) < len(celdas_validas):
            costo, del_nodo, al_nodo = heappop(monticulo_aristas)

            if al_nodo in visitados:
                continue

            visitados.add(al_nodo)
            aristas.append((del_nodo, al_nodo))
            costo_total += costo

            for vecino in self.mapa.obtener_vecinos(*al_nodo):
                if vecino not in visitados:
                    costo_vecino = self.mapa.obtener_costo(*vecino)
                    heappush(monticulo_aristas, (costo_vecino, al_nodo, vecino))

        return aristas, costo_total

    def kruskal_mst(self):
        """Algoritmo de Kruskal para MST usando Union-Find"""
        celdas_validas = [(i, j) for i in range(self.mapa.size)
                          for j in range(self.mapa.size)
                          if self.mapa.grid[i, j] != 'MONTAÑA']

        if not celdas_validas:
            return [], 0

        # Crear todas las aristas posibles
        aristas = []
        for i, j in celdas_validas:
            for ni, nj in self.mapa.obtener_vecinos(i, j):
                if (ni, nj) in celdas_validas:
                    costo = self.mapa.obtener_costo(ni, nj)
                    # Evitar duplicados
                    if (i, j) < (ni, nj):
                        aristas.append((costo, (i, j), (ni, nj)))

        # Ordenar aristas por peso
        aristas.sort()

        # Union-Find
        padre = {celda: celda for celda in celdas_validas}

        def find(x):
            if padre[x] != x:
                padre[x] = find(padre[x])
            return padre[x]

        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                padre[px] = py
                return True
            return False

        # Algoritmo de Kruskal
        aristas_mst = []
        costo_total = 0

        for costo, u, v in aristas:
            if union(u, v):
                aristas_mst.append((u, v))
                costo_total += costo
                if len(aristas_mst) == len(celdas_validas) - 1:
                    break

        return aristas_mst, costo_total

    def detectar_ciclos_dfs(self):
        """Detecta ciclos en el grafo usando DFS"""
        visitados = set()
        pila_recursiva = set()
        ciclos_encontrados = []

        def dfs(nodo_actual, padre, ruta_actual):
            visitados.add(nodo_actual)
            pila_recursiva.add(nodo_actual)
            ruta_actual.append(nodo_actual)

            for vecino in self.mapa.obtener_vecinos(*nodo_actual):
                if vecino == padre:
                    continue

                if vecino in pila_recursiva:
                    # Encontrado un ciclo
                    inicio_ciclo = ruta_actual.index(vecino)
                    ciclo = ruta_actual[inicio_ciclo:]
                    ciclos_encontrados.append(ciclo)
                elif vecino not in visitados:
                    dfs(vecino, nodo_actual, ruta_actual.copy())

            pila_recursiva.remove(nodo_actual)

        # Buscar ciclos desde todas las celdas no visitadas
        for i in range(self.mapa.size):
            for j in range(self.mapa.size):
                if (i, j) not in visitados and self.mapa.grid[i, j] != 'MONTAÑA':
                    dfs((i, j), None, [])

        return ciclos_encontrados