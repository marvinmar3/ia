"""
Representa el mapa del juego con diferentes tipos de terreno
"""

import numpy as np
import random
from config import TAM_CUADRICULA
from modelos.terreno import TIPOS_TERRENO


class MapaJuego:
    def __init__(self, size=TAM_CUADRICULA):
        self.size = size
        self.grid = self._generar_terreno()
        self.inicio = None
        self.meta = None

    def _generar_terreno(self):
        """Genera un mapa con terrenos variados"""
        grid = np.full((self.size, self.size), 'LLANURA', dtype=object)

        # Añadir bosques (grupos)
        for _ in range(15):
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size and random.random() > 0.5:
                        grid[nx, ny] = 'BOSQUE'

        # Añadir pantanos
        for _ in range(10):
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size and random.random() > 0.6:
                        grid[nx, ny] = 'PANTANO'

        # Añadir agua (ríos)
        for _ in range(3):
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            direccion = random.choice([(0, 1), (1, 0), (1, 1)])
            for _ in range(random.randint(5, 10)):
                if 0 <= x < self.size and 0 <= y < self.size:
                    grid[x, y] = 'AGUA'
                x += direccion[0]
                y += direccion[1]

        # Añadir montañas
        for _ in range(8):
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            grid[x, y] = 'MONTAÑA'
            if random.random() > 0.5:
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size and random.random() > 0.5:
                        grid[nx, ny] = 'MONTAÑA'

        return grid

    def obtener_costo(self, x, y):
        """Obtiene el coste de movimiento de una celda"""
        if not (0 <= x < self.size and 0 <= y < self.size):
            return float('inf')
        return TIPOS_TERRENO.INFO[self.grid[x, y]]['costo']

    def obtener_vecinos(self, x, y):
        """Obtiene vecinos válidos (4 direcciones)"""
        vecinos = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if self.grid[nx, ny] != 'MONTAÑA':
                    vecinos.append((nx, ny))
        return vecinos

    def cargar_mapa_generado(self, mapa_generado):
        """Carga un mapa generado proceduralmente"""
        self.grid = mapa_generado
        self.inicio = None
        self.meta = None