"""
Algoritmos de generación procedural de mapas
Implementa Perlin Noise y Autómatas Celulares
"""

import numpy as np
import random
from noise import pnoise2


class GeneradorMapa:
    def __init__(self, tamano):
        self.tamano = tamano

    def generar_con_perlin_noise(self, octavas=6, persistencia=0.5, lacunaridad=2.0):
        """
        Genera terreno realista usando Perlin Noise

        Perlin Noise crea patrones suaves y naturales sumando
        múltiples capas de ruido a diferentes frecuencias.

        Parámetros:
        - octavas: Número de capas de detalle (más = más detallado)
        - persistencia: Cómo disminuye amplitud en cada octava
        - lacunaridad: Cómo aumenta frecuencia en cada octava
        """
        mapa = np.empty((self.tamano, self.tamano), dtype=object)

        # Generar ruido Perlin
        escala = 10.0
        semilla = random.randint(0, 1000)

        for i in range(self.tamano):
            for j in range(self.tamano):
                # Obtener valor de ruido entre -1 y 1
                valor_ruido = pnoise2(
                    i / escala,
                    j / escala,
                    octaves=octavas,
                    persistence=persistencia,
                    lacunarity=lacunaridad,
                    repeatx=self.tamano,
                    repeaty=self.tamano,
                    base=semilla
                )

                # Mapear ruido a tipos de terreno
                # Valores bajos = agua, valores altos = montaña
                if valor_ruido < -0.3:
                    mapa[i, j] = 'AGUA'
                elif valor_ruido < -0.1:
                    mapa[i, j] = 'PANTANO'
                elif valor_ruido < 0.2:
                    mapa[i, j] = 'LLANURA'
                elif valor_ruido < 0.4:
                    mapa[i, j] = 'BOSQUE'
                else:
                    mapa[i, j] = 'MONTAÑA'

        return mapa

    def generar_con_automatas_celulares(self, iteraciones=5, prob_pared_inicial=0.45):
        """
        Genera mapas tipo cueva usando Autómatas Celulares

        Algoritmo:
        1. Inicializa mapa aleatoriamente (45% paredes, 55% suelo)
        2. Repite 5 veces:
           - Para cada celda, cuenta vecinos que son pared
           - Si tiene 5+ vecinos pared → se vuelve pared
           - Si tiene 2- vecinos pared → se vuelve suelo
        3. Resultado: Cuevas orgánicas con formas naturales

        Parámetros:
        - iteraciones: Veces que aplica la regla (más = más suave)
        - prob_pared_inicial: % de celdas que inician como pared
        """
        # PASO 1: Inicialización aleatoria
        mapa = np.random.choice(
            ['LLANURA', 'MONTAÑA'],
            size=(self.tamano, self.tamano),
            p=[1 - prob_pared_inicial, prob_pared_inicial]
        )

        # PASO 2: Aplicar reglas de autómata celular
        for _ in range(iteraciones):
            nuevo_mapa = mapa.copy()

            for i in range(self.tamano):
                for j in range(self.tamano):
                    # Contar vecinos que son pared
                    vecinos_pared = self._contar_vecinos_pared(mapa, i, j)

                    # REGLA DEL AUTÓMATA:
                    # Muchos vecinos pared (5+) → esta celda se vuelve pared
                    if vecinos_pared >= 5:
                        nuevo_mapa[i, j] = 'MONTAÑA'
                    # Pocos vecinos pared (2-) → esta celda se vuelve suelo
                    elif vecinos_pared <= 2:
                        nuevo_mapa[i, j] = 'LLANURA'
                    # 3-4 vecinos → mantiene su estado

            mapa = nuevo_mapa

        # PASO 3: Añadir variedad de terrenos en zonas de suelo
        for i in range(self.tamano):
            for j in range(self.tamano):
                if mapa[i, j] == 'LLANURA':
                    aleatorio = random.random()
                    if aleatorio < 0.2:
                        mapa[i, j] = 'BOSQUE'
                    elif aleatorio < 0.3:
                        mapa[i, j] = 'PANTANO'
                    elif aleatorio < 0.35:
                        mapa[i, j] = 'AGUA'

        return mapa

    def _contar_vecinos_pared(self, mapa, x, y):
        """
        Cuenta cuántos de los 8 vecinos son MONTAÑA (pared)

        Vecinos:
        [NW][N][NE]
        [W ][X][E ]
        [SW][S][SE]
        """
        contador = 0

        # Revisar las 8 direcciones
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                # Saltar la celda central
                if dx == 0 and dy == 0:
                    continue

                nx, ny = x + dx, y + dy

                # Si está dentro del mapa
                if 0 <= nx < self.tamano and 0 <= ny < self.tamano:
                    if mapa[nx, ny] == 'MONTAÑA':
                        contador += 1
                else:
                    # Bordes del mapa cuentan como pared
                    # (esto hace que el mapa tenga bordes cerrados)
                    contador += 1

        return contador