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

        if self.mapa.inicio and self.mapa.inicio in celdas_validas:
            inicio = self.mapa.inicio
        else:
            inicio = random.choice(celdas_validas)

            visitados = {inicio}
            aristas = []
            monticulo_aristas = [] #cola de prioridad

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

            #obtenemos los vecinos del nodo recien agregado
            for vecino in self.mapa.obtener_vecinos(*al_nodo):
                if vecino not in visitados:
                    costo_vecino = self.mapa.obtener_costo(*vecino)
                    heappush(monticulo_aristas, (costo_vecino, al_nodo, vecino))

        return aristas, costo_total

    def prim_mst_conectado(self):
        """
        Prim MST que GARANTIZA conectar inicio y meta
        Retorna: (aristas, costo_total, conectado)
        """
        if not self.mapa.inicio or not self.mapa.meta:
            return self.prim_mst()

        celdas_validas = [(i, j) for i in range(self.mapa.size)
                          for j in range(self.mapa.size)
                          if self.mapa.grid[i, j] != 'MONTAÑA']

        if not celdas_validas:
            return [], 0, False

        inicio = self.mapa.inicio
        visitados = {inicio}
        aristas = []
        monticulo_aristas = []

        # Añadir aristas iniciales
        for vecino in self.mapa.obtener_vecinos(*inicio):
            costo = self.mapa.obtener_costo(*vecino)
            heappush(monticulo_aristas, (costo, inicio, vecino))

        costo_total = 0
        meta_alcanzada = (inicio == self.mapa.meta)

        while monticulo_aristas and len(visitados) < len(celdas_validas):
            costo, del_nodo, al_nodo = heappop(monticulo_aristas)

            if al_nodo in visitados:
                continue

            visitados.add(al_nodo)
            aristas.append((del_nodo, al_nodo))
            costo_total += costo

            if al_nodo == self.mapa.meta:
                meta_alcanzada = True

            for vecino in self.mapa.obtener_vecinos(*al_nodo):
                if vecino not in visitados:
                    costo_vecino = self.mapa.obtener_costo(*vecino)
                    heappush(monticulo_aristas, (costo_vecino, al_nodo, vecino))

        return aristas, costo_total, meta_alcanzada

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

                    if self.mapa.inicio and self.mapa.meta:
                        if (i, j) == self.mapa.inicio or (ni, nj) == self.mapa.inicio:
                            prioridad_extra = -0.1  # Slight boost
                        if (i, j) == self.mapa.meta or (ni, nj) == self.mapa.meta:
                            prioridad_extra = -0.1

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
