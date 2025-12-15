import numpy as np
import random
from heapq import heappush, heappop

class GeneradorLaberinto:
    def __init__(self, tamano):
        self.tamano = tamano

    def generar_laberinto_prim(self):
        """
        Genera laberinto usando algoritmo de Prim

        CÓMO FUNCIONA:
        1. Todo el mapa empieza como MONTAÑA (paredes)
        2. Elige una celda aleatoria como inicio
        3. Usa Prim para "tallar" caminos conectando celdas
        4. Resultado: ¡Un laberinto perfecto sin ciclos!
        """
        # Todo es pared inicialmente
        grid = np.full((self.tamano, self.tamano), 'MONTAÑA', dtype=object)

        # Celda inicial aleatoria (debe ser impar para que funcione)
        inicio_x = random.randrange(1, self.tamano, 2)
        inicio_y = random.randrange(1, self.tamano, 2)
        grid[inicio_x, inicio_y] = 'LLANURA'

        # Paredes candidatas (celdas que podemos "romper")
        paredes = []
        self._agregar_paredes(inicio_x, inicio_y, paredes, grid)

        # Algoritmo de Prim
        while paredes:
            # Elegir pared aleatoria
            pared = paredes.pop(random.randint(0, len(paredes) - 1))
            px, py = pared

            # Verificar si podemos romper esta pared
            if self._puede_romper_pared(px, py, grid):
                grid[px, py] = 'LLANURA'

                # Encontrar la celda al otro lado
                vecino = self._encontrar_celda_opuesta(px, py, grid)
                if vecino:
                    nx, ny = vecino
                    grid[nx, ny] = 'LLANURA'
                    self._agregar_paredes(nx, ny, paredes, grid)

        # Agregar variedad de terrenos en los pasillos
        self._agregar_variedad_terreno(grid)

        return grid

    def generar_laberinto_kruskal(self):
        """
        Genera laberinto usando algoritmo de Kruskal

        CÓMO FUNCIONA:
        1. Cada celda empieza siendo su propio "set"
        2. Aleatoriamente une sets rompiendo paredes
        3. Usa Union-Find para evitar ciclos
        4. Resultado: ¡Laberinto perfecto con caminos largos!
        """
        grid = np.full((self.tamano, self.tamano), 'MONTAÑA', dtype=object)

        # Crear lista de todas las celdas (solo impares)
        celdas = [(i, j) for i in range(1, self.tamano, 2)
                  for j in range(1, self.tamano, 2)]

        # Marcar todas las celdas como camino
        for x, y in celdas:
            grid[x, y] = 'LLANURA'

        # Union-Find
        padre = {celda: celda for celda in celdas}

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

        # Crear lista de paredes entre celdas
        paredes = []
        for x, y in celdas:
            # Pared derecha
            if y + 2 < self.tamano:
                paredes.append(((x, y), (x, y + 2), (x, y + 1)))
            # Pared abajo
            if x + 2 < self.tamano:
                paredes.append(((x, y), (x + 2, y), (x + 1, y)))

        # Mezclar paredes aleatoriamente
        random.shuffle(paredes)

        # Algoritmo de Kruskal
        for celda1, celda2, pared in paredes:
            if union(celda1, celda2):
                # Romper la pared
                grid[pared[0], pared[1]] = 'LLANURA'

        # Agregar variedad
        self._agregar_variedad_terreno(grid)

        return grid

    def generar_laberinto_kruskal(self):
        """
        Genera laberinto usando algoritmo de Kruskal

        CÓMO FUNCIONA:
        1. Cada celda empieza siendo su propio "set"
        2. Aleatoriamente une sets rompiendo paredes
        3. Usa Union-Find para evitar ciclos
        4. Resultado: ¡Laberinto perfecto con caminos largos!
        """
        grid = np.full((self.tamano, self.tamano), 'MONTAÑA', dtype=object)

        # Crear lista de todas las celdas (solo impares)
        celdas = [(i, j) for i in range(1, self.tamano, 2)
                  for j in range(1, self.tamano, 2)]

        # Marcar todas las celdas como camino
        for x, y in celdas:
            grid[x, y] = 'LLANURA'

        # Union-Find
        padre = {celda: celda for celda in celdas}

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

        # Crear lista de paredes entre celdas
        paredes = []
        for x, y in celdas:
            # Pared derecha
            if y + 2 < self.tamano:
                paredes.append(((x, y), (x, y + 2), (x, y + 1)))
            # Pared abajo
            if x + 2 < self.tamano:
                paredes.append(((x, y), (x + 2, y), (x + 1, y)))

        # Mezclar paredes aleatoriamente
        random.shuffle(paredes)

        # Algoritmo de Kruskal
        for celda1, celda2, pared in paredes:
            if union(celda1, celda2):
                # Romper la pared
                grid[pared[0], pared[1]] = 'LLANURA'

        # Agregar variedad
        self._agregar_variedad_terreno(grid)

        return grid

    def _agregar_paredes(self, x, y, paredes, grid):
        """Agrega paredes adyacentes a la lista"""
        for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.tamano and 0 <= ny < self.tamano:
                if grid[nx, ny] == 'MONTAÑA':
                    # Agregar la pared entre (x,y) y (nx,ny)
                    pared_x, pared_y = x + dx // 2, y + dy // 2
                    if (pared_x, pared_y) not in paredes:
                        paredes.append((pared_x, pared_y))

    def _puede_romper_pared(self, x, y, grid):
        """Verifica si podemos romper esta pared"""
        # Contar cuántas celdas vecinas son camino
        celdas_camino = 0
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.tamano and 0 <= ny < self.tamano:
                if grid[nx, ny] == 'LLANURA':
                    celdas_camino += 1

        # Solo romper si conecta exactamente 1 camino con pared
        return celdas_camino == 1

    def _encontrar_celda_opuesta(self, px, py, grid):
        """Encuentra la celda al otro lado de la pared"""
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = px + dx, py + dy
            if 0 <= nx < self.tamano and 0 <= ny < self.tamano:
                if grid[nx, ny] == 'MONTAÑA':
                    return (nx, ny)
        return None

    def _agregar_variedad_terreno(self, grid):
        """Agrega diferentes tipos de terreno en los pasillos"""
        for i in range(self.tamano):
            for j in range(self.tamano):
                if grid[i, j] == 'LLANURA':
                    rand = random.random()
                    if rand < 0.15:
                        grid[i, j] = 'BOSQUE'
                    elif rand < 0.25:
                        grid[i, j] = 'PANTANO'
                    elif rand < 0.28:
                        grid[i, j] = 'AGUA'

