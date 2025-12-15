import random
import numpy as np


class GeneradorDungeon:

    #genera mazmorras con salas conectadas por pasillos
    def __init__(self, tamano):
        self.tamano = tamano

    def generar_dungeon(self, num_salas=8):
        """
        Genera una mazmorra con salas y pasillos

        CÓMO FUNCIONA:
        1. Genera salas aleatorias
        2. Usa MST para conectarlas con pasillos
        3. Agrega enemigos y obstáculos
        """
        grid = np.full((self.tamano, self.tamano), 'MONTAÑA', dtype=object)

        # Generar salas
        salas = []
        intentos = 0
        while len(salas) < num_salas and intentos < 50:
            ancho = random.randint(3, 7)
            alto = random.randint(3, 7)
            x = random.randint(1, self.tamano - ancho - 1)
            y = random.randint(1, self.tamano - alto - 1)

            nueva_sala = (x, y, ancho, alto)

            # Verificar que no se superponga
            if not self._salas_se_superponen(nueva_sala, salas):
                salas.append(nueva_sala)
                self._crear_sala(grid, nueva_sala)

            intentos += 1

        # Conectar salas con pasillos (usando MST)
        self._conectar_salas_mst(grid, salas)

        # Agregar obstáculos dentro de las salas
        self._agregar_obstaculos_salas(grid, salas)

        return grid

    def _salas_se_superponen(self, sala1, salas):
        """Verifica si una sala se superpone con otras"""
        x1, y1, w1, h1 = sala1
        for x2, y2, w2, h2 in salas:
            if not (x1 + w1 + 1 < x2 or x2 + w2 + 1 < x1 or
                    y1 + h1 + 1 < y2 or y2 + h2 + 1 < y1):
                return True
        return False

    def _crear_sala(self, grid, sala):
        """Crea una sala rectangular"""
        x, y, ancho, alto = sala
        for i in range(x, x + ancho):
            for j in range(y, y + alto):
                grid[i, j] = 'LLANURA'

    def _conectar_salas_mst(self, grid, salas):
        """Conecta salas usando Minimum Spanning Tree"""
        if len(salas) < 2:
            return

        # Calcular centros de las salas
        centros = [(x + w // 2, y + h // 2) for x, y, w, h in salas]

        # Crear grafo de distancias
        aristas = []
        for i in range(len(centros)):
            for j in range(i + 1, len(centros)):
                dist = abs(centros[i][0] - centros[j][0]) + \
                       abs(centros[i][1] - centros[j][1])
                aristas.append((dist, i, j))

        # MST con Kruskal
        aristas.sort()
        padre = list(range(len(salas)))

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

        # Conectar salas
        for dist, i, j in aristas:
            if union(i, j):
                self._crear_pasillo(grid, centros[i], centros[j])

    def _crear_pasillo(self, grid, inicio, fin):
        """Crea un pasillo en forma de L entre dos puntos"""
        x1, y1 = inicio
        x2, y2 = fin

        # Pasillo horizontal
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if 0 <= x < self.tamano and 0 <= y1 < self.tamano:
                grid[x, y1] = 'LLANURA'

        # Pasillo vertical
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if 0 <= x2 < self.tamano and 0 <= y < self.tamano:
                grid[x2, y] = 'LLANURA'

    def _agregar_obstaculos_salas(self, grid, salas):
        """Agrega obstáculos dentro de las salas"""
        for x, y, w, h in salas:
            # 20% de probabilidad de tener obstáculos
            if random.random() < 0.3:
                # Agregar 1-3 obstáculos
                for _ in range(random.randint(1, 3)):
                    ox = random.randint(x + 1, x + w - 2)
                    oy = random.randint(y + 1, y + h - 2)
                    grid[ox, oy] = random.choice(['BOSQUE', 'PANTANO', 'AGUA'])