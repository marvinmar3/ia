import pygame

import config
from algoritmos.busquedas import Busquedas
from algoritmos.algoritmo_grafos import AlgoritmosGrafo
from algoritmos.generacion_mapas import GeneradorMapa
from modelos.terreno import TIPOS_TERRENO
from ui.boton import Boton
from ui.colores import COLORES
from config import *


class Visualizador:
    def __init__(self, mapa_juego):
        pygame.init()

        self.mapa = mapa_juego
        self.pantalla = pygame.display.set_mode((VENTANA_ANCHO, VENTANA_ALTO))
        pygame.display.set_caption("El Rescate del Explorador Perdido")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.Font(None, 24)
        self.fuente_pequena = pygame.font.Font(None, 18)

        # Estado del juego
        self.modo = 'establecer_inicio'  # 'establecer_inicio', 'establecer_meta', 'listo'
        self.alg_en_ejecucion = False
        self.mostrar_ruta = None  # 'aestrella', 'greedy', 'bfs', 'comparar', None
        self.mostrar_mst = False
        self.mostrar_ciclos = False

        # Resultados de algoritmos
        self.ruta_aestrella = []
        self.visitados_aestrella = []
        self.costo_aestrella = 0

        self.ruta_greedy = []
        self.visitados_greedy = []
        self.costo_greedy = 0

        self.ruta_bfs = []
        self.visitados_bfs = []
        self.costo_bfs = 0

        self.aristas_mst = []
        self.costo_mst = 0

        self.aristas_kruskal = []
        self.costo_kruskal = 0

        self.ciclos = []

        # Animación
        self.paso_animacion = 0
        self.animando = False
        self.tipo_animacion = None

        self.camino_agente = []
        self.indice_agente = 0
        self.animado_agente = False
        self.frames_por_paso = 4 # velocidad (menor es mas rapido)
        self.contador_frames =0

        # Botones
        self.botones = self._crear_botones()

        #sprites
        self.spriteTom = pygame.image.load("assets/sprite/standing/2.png").convert_alpha()
        self.spriteTom = pygame.transform.scale(
            self.spriteTom, (config.TAM_CELDA, config.TAM_CELDA)
        )

        self.spriteJerry= pygame.image.load("assets/sprite/jerry/3.png").convert_alpha()
        self.spriteJerry=pygame.transform.scale(
            self.spriteJerry, (config.TAM_CELDA, config.TAM_CELDA)
        )

    def _crear_botones(self):
        """Crea los botones de control"""
        panel_x = TAM_CUADRICULA * TAM_CELDA + 10
        botones = []

        # ALGORITMOS DE BÚSQUEDA
        botones.append(Boton(panel_x, 50, 135, 35, "A*",
                             lambda: self.ejecutar_algoritmo('aestrella')))
        botones.append(Boton(panel_x + 145, 50, 135, 35, "Greedy",
                             lambda: self.ejecutar_algoritmo('greedy')))
        botones.append(Boton(panel_x, 95, 135, 35, "BFS",
                             lambda: self.ejecutar_algoritmo('bfs')))
        botones.append(Boton(panel_x + 145, 95, 135, 35, "Comparar",
                             lambda: self.ejecutar_algoritmo('comparar')))

        # ALGORITMOS DE GRAFOS
        botones.append(Boton(panel_x, 145, 135, 35, "MST Prim",
                             self.ejecutar_mst))
        botones.append(Boton(panel_x + 145, 145, 135, 35, "MST Kruskal",
                             self.ejecutar_kruskal))
        botones.append(Boton(panel_x, 190, 280, 35, "Detectar Ciclos",
                             self.ejecutar_deteccion_ciclos))

        # GENERACIÓN DE MAPAS
        botones.append(Boton(panel_x, 240, 280, 35, "Mapa: Perlin Noise",
                             self.generar_perlin))
        botones.append(Boton(panel_x, 285, 280, 35, "Mapa: Autómatas Celulares",
                             self.generar_cellular))

        # UTILIDADES
        botones.append(Boton(panel_x, 340, 280, 35, "Limpiar",
                             self.limpiar_visualizacion))
        botones.append(Boton(panel_x, 385, 280, 35, "Mapa Aleatorio",
                             self.resetear_mapa))

        return botones

    def ejecutar_algoritmo(self, algoritmo):
        """Ejecuta el algoritmo de búsqueda seleccionado"""
        if self.mapa.inicio is None or self.mapa.meta is None:
            return

        buscador = Busquedas(self.mapa)

        if algoritmo == 'aestrella':
            self.ruta_aestrella, self.visitados_aestrella, _, self.costo_aestrella = \
                buscador.a_estrella(self.mapa.inicio, self.mapa.meta)
            self.mostrar_ruta = 'aestrella'

        elif algoritmo == 'greedy':
            self.ruta_greedy, self.visitados_greedy, _, self.costo_greedy = \
                buscador.greedy(self.mapa.inicio, self.mapa.meta)
            self.mostrar_ruta = 'greedy'

        elif algoritmo == 'bfs':
            self.ruta_bfs, self.visitados_bfs, _, self.costo_bfs = \
                buscador.bfs(self.mapa.inicio, self.mapa.meta)
            self.mostrar_ruta = 'bfs'

        elif algoritmo == 'comparar':
            self.ruta_aestrella, self.visitados_aestrella, _, self.costo_aestrella = \
                buscador.a_estrella(self.mapa.inicio, self.mapa.meta)
            self.ruta_greedy, self.visitados_greedy, _, self.costo_greedy = \
                buscador.greedy(self.mapa.inicio, self.mapa.meta)
            self.mostrar_ruta = 'comparar'

        self.paso_animacion = 0
        self.animando = True
        self.tipo_animacion = algoritmo

        #preparar la animacion del agente segun algoritmo
        if algoritmo == 'aestrella':
            self.camino_agente = self.ruta_aestrella
        elif algoritmo == 'greedy':
            self.camino_agente = self.ruta_greedy
        elif algoritmo == 'bfs':
            self.camino_agente = self.ruta_bfs
        elif algoritmo == 'comparar':
            self.camino_agente = self.ruta_aestrella #anima a* por defecto

        self.indice_agente = 0
        self.animado_agente=True
        self.contador_frames=0


    def ejecutar_mst(self):
        """Ejecuta el algoritmo de Prim"""
        algoritmo_grafo = AlgoritmosGrafo(self.mapa)
        self.aristas_mst, self.costo_mst = algoritmo_grafo.prim_mst()
        self.mostrar_mst = not self.mostrar_mst

    def ejecutar_kruskal(self):
        """Ejecuta el algoritmo de Kruskal"""
        algoritmo_grafo = AlgoritmosGrafo(self.mapa)
        self.aristas_kruskal, self.costo_kruskal = algoritmo_grafo.kruskal_mst()
        self.mostrar_mst = True

    def ejecutar_deteccion_ciclos(self):
        """Ejecuta la detección de ciclos"""
        algoritmo_grafo = AlgoritmosGrafo(self.mapa)
        self.ciclos = algoritmo_grafo.detectar_ciclos_dfs()
        self.mostrar_ciclos = not self.mostrar_ciclos

    def generar_perlin(self):
        """Genera mapa con Perlin Noise (terreno realista)"""
        generador = GeneradorMapa(self.mapa.size)
        nuevo_mapa = generador.generar_con_perlin_noise()
        self.mapa.cargar_mapa_generado(nuevo_mapa)
        self.limpiar_visualizacion()
        self.modo = 'establecer_inicio'

    def generar_cellular(self):
        """Genera mapa con Autómatas Celulares (cuevas)"""
        generador = GeneradorMapa(self.mapa.size)
        nuevo_mapa = generador.generar_con_automatas_celulares()
        self.mapa.cargar_mapa_generado(nuevo_mapa)
        self.limpiar_visualizacion()
        self.modo = 'establecer_inicio'

    def resetear_mapa(self):
        """Genera un nuevo mapa aleatorio"""
        self.mapa.__init__(self.mapa.size)
        self.limpiar_visualizacion()
        self.modo = 'establecer_inicio'

    def limpiar_visualizacion(self):
        """Limpia todas las visualizaciones"""
        self.ruta_aestrella = []
        self.visitados_aestrella = []
        self.ruta_greedy = []
        self.visitados_greedy = []
        self.ruta_bfs = []
        self.visitados_bfs = []
        self.aristas_mst = []
        self.aristas_kruskal = []
        self.ciclos = []
        self.mostrar_ruta = None
        self.mostrar_mst = False
        self.mostrar_ciclos = False
        self.animando = False

    def dibujar_grid(self):
        """Dibuja el mapa con todos los terrenos"""
        for i in range(self.mapa.size):
            for j in range(self.mapa.size):
                x = j * TAM_CELDA
                y = i * TAM_CELDA
                terreno = self.mapa.grid[i, j]
                color = TIPOS_TERRENO[terreno]['color']

                pygame.draw.rect(self.pantalla, color, (x, y, TAM_CELDA, TAM_CELDA))
                pygame.draw.rect(self.pantalla, COLORES['GRID'],
                                 (x, y, TAM_CELDA, TAM_CELDA), 1)

    def dibujar_visitados(self):
        """Dibuja las celdas visitadas durante la búsqueda"""
        max_pasos = max(len(self.visitados_aestrella), len(self.visitados_greedy), len(self.visitados_bfs))
        paso_actual = min(self.paso_animacion, max_pasos)

        if self.mostrar_ruta in ['aestrella', 'comparar']:
            for nodo in self.visitados_aestrella[:paso_actual]:
                x, y = nodo[1] * TAM_CELDA, nodo[0] * TAM_CELDA
                surf = pygame.Surface((TAM_CELDA, TAM_CELDA))
                surf.set_alpha(100)
                surf.fill(COLORES['VISITADOS'])
                self.pantalla.blit(surf, (x, y))

        if self.mostrar_ruta in ['greedy', 'comparar']:
            for nodo in self.visitados_greedy[:paso_actual]:
                x, y = nodo[1] * TAM_CELDA, nodo[0] * TAM_CELDA
                surf = pygame.Surface((TAM_CELDA, TAM_CELDA))
                surf.set_alpha(100)
                surf.fill((255, 200, 100))  # Naranja claro
                self.pantalla.blit(surf, (x, y))

        if self.mostrar_ruta == 'bfs':
            for nodo in self.visitados_bfs[:paso_actual]:
                x, y = nodo[1] * TAM_CELDA, nodo[0] * TAM_CELDA
                surf = pygame.Surface((TAM_CELDA, TAM_CELDA))
                surf.set_alpha(100)
                surf.fill((200, 150, 230))  # Morado claro
                self.pantalla.blit(surf, (x, y))

    def dibujar_caminos(self):
        """Dibuja los caminos encontrados"""
        if self.mostrar_ruta in ['aestrella', 'comparar'] and self.ruta_aestrella:
            for i in range(len(self.ruta_aestrella) - 1):
                inicio = (self.ruta_aestrella[i][1] * TAM_CELDA + TAM_CELDA // 2,
                          self.ruta_aestrella[i][0] * TAM_CELDA + TAM_CELDA // 2)
                fin = (self.ruta_aestrella[i + 1][1] * TAM_CELDA + TAM_CELDA // 2,
                       self.ruta_aestrella[i + 1][0] * TAM_CELDA + TAM_CELDA // 2)
                pygame.draw.line(self.pantalla, COLORES['RUTA_AESTRELLA'], inicio, fin, 5)

        if self.mostrar_ruta in ['greedy', 'comparar'] and self.ruta_greedy:
            for i in range(len(self.ruta_greedy) - 1):
                inicio = (self.ruta_greedy[i][1] * TAM_CELDA + TAM_CELDA // 2,
                          self.ruta_greedy[i][0] * TAM_CELDA + TAM_CELDA // 2)
                fin = (self.ruta_greedy[i + 1][1] * TAM_CELDA + TAM_CELDA // 2,
                       self.ruta_greedy[i + 1][0] * TAM_CELDA + TAM_CELDA // 2)
                pygame.draw.line(self.pantalla, COLORES['RUTA_GREEDY'], inicio, fin, 4)

        if self.mostrar_ruta == 'bfs' and self.ruta_bfs:
            for i in range(len(self.ruta_bfs) - 1):
                inicio = (self.ruta_bfs[i][1] * TAM_CELDA + TAM_CELDA // 2,
                          self.ruta_bfs[i][0] * TAM_CELDA + TAM_CELDA // 2)
                fin = (self.ruta_bfs[i + 1][1] * TAM_CELDA + TAM_CELDA // 2,
                       self.ruta_bfs[i + 1][0] * TAM_CELDA + TAM_CELDA // 2)
                pygame.draw.line(self.pantalla, COLORES['RUTA_BFS'], inicio, fin, 3)

    def dibujar_mst(self):
        """Dibuja el Árbol de Expansión Mínima"""
        aristas_dibujar = self.aristas_kruskal if self.aristas_kruskal else self.aristas_mst

        if self.mostrar_mst and aristas_dibujar:
            for del_nodo, al_nodo in aristas_dibujar:
                inicio = (del_nodo[1] * TAM_CELDA + TAM_CELDA // 2,
                          del_nodo[0] * TAM_CELDA + TAM_CELDA // 2)
                fin = (al_nodo[1] * TAM_CELDA + TAM_CELDA // 2,
                       al_nodo[0] * TAM_CELDA + TAM_CELDA // 2)
                pygame.draw.line(self.pantalla, COLORES['MST'], inicio, fin, 2)

    def dibujar_ciclos(self):
        """Dibuja las regiones con ciclos detectados"""
        if self.mostrar_ciclos and self.ciclos:
            for ciclo in self.ciclos[:5]:  # Mostrar solo los primeros 5 ciclos
                for nodo in ciclo:
                    x, y = nodo[1] * TAM_CELDA, nodo[0] * TAM_CELDA
                    surf = pygame.Surface((TAM_CELDA, TAM_CELDA))
                    surf.set_alpha(120)
                    surf.fill(COLORES['CICLOS'])
                    self.pantalla.blit(surf, (x, y))

    def dibujar_marcadores(self):
        """Dibuja los marcadores de inicio y objetivo"""
        if self.mapa.inicio:
            if self.animado_agente and self.camino_agente:
                fila, col = self.camino_agente[self.indice_agente]
            else:
                fila, col = self.mapa.inicio

            x = col *TAM_CELDA
            y= fila*TAM_CELDA
            self.pantalla.blit(self.spriteTom, (x,y))
            """x = self.mapa.inicio[1] * TAM_CELDA + TAM_CELDA // 2
            y = self.mapa.inicio[0] * TAM_CELDA + TAM_CELDA // 2
            pygame.draw.circle(self.pantalla, COLORES['INICIO'], (x, y), TAM_CELDA // 3)
            pygame.draw.circle(self.pantalla, (0, 0, 0), (x, y), TAM_CELDA // 3, 2)"""

        if self.mapa.meta:
            fila, col = self.mapa.meta
            x = col * TAM_CELDA
            y = fila * TAM_CELDA
            self.pantalla.blit(self.spriteJerry, (x, y))
            """x = self.mapa.meta[1] * TAM_CELDA + TAM_CELDA // 2
            y = self.mapa.meta[0] * TAM_CELDA + TAM_CELDA // 2
            pygame.draw.circle(self.pantalla, COLORES['META'], (x, y), TAM_CELDA // 3)
            pygame.draw.circle(self.pantalla, (0, 0, 0), (x, y), TAM_CELDA // 3, 2)"""

    def dibujar_panel_control(self):
        """Dibuja el panel de control lateral"""
        panel_x = TAM_CUADRICULA * TAM_CELDA
        pygame.draw.rect(self.pantalla, COLORES['PANEL'],
                         (panel_x, 0, 300, VENTANA_ALTO))
        pygame.draw.line(self.pantalla, COLORES['TEXTO'],
                         (panel_x, 0), (panel_x, VENTANA_ALTO), 2)

        # Título
        titulo = self.fuente.render("PANEL DE CONTROL", True, COLORES['TEXTO'])
        self.pantalla.blit(titulo, (panel_x + 50, 10))

        # Instrucciones según modo
        y_offset = 430
        if self.modo == 'establecer_inicio':
            texto = "Click: Colocar Unidad"
        elif self.modo == 'establecer_meta':
            texto = "Click: Colocar Baliza"
        else:
            texto = "¡Listo para ejecutar!"

        inst = self.fuente_pequena.render(texto, True, COLORES['TEXTO'])
        self.pantalla.blit(inst, (panel_x + 10, y_offset))

        # Resultados
        if self.ruta_aestrella:
            y_offset += 30
            texto_costo = f"A* - Coste: {self.costo_aestrella:.0f}"
            texto_pasos = f"Pasos: {len(self.ruta_aestrella)}"
            self.pantalla.blit(self.fuente_pequena.render(texto_costo, True, COLORES['TEXTO']),
                               (panel_x + 10, y_offset))
            self.pantalla.blit(self.fuente_pequena.render(texto_pasos, True, COLORES['TEXTO']),
                               (panel_x + 10, y_offset + 20))

        if self.ruta_greedy:
            y_offset += 50
            texto_costo = f"Greedy - Coste: {self.costo_greedy:.0f}"
            texto_pasos = f"Pasos: {len(self.ruta_greedy)}"
            self.pantalla.blit(self.fuente_pequena.render(texto_costo, True, COLORES['TEXTO']),
                               (panel_x + 10, y_offset))
            self.pantalla.blit(self.fuente_pequena.render(texto_pasos, True, COLORES['TEXTO']),
                               (panel_x + 10, y_offset + 20))

        if self.ruta_bfs:
            y_offset += 50
            texto_costo = f"BFS - Coste: {self.costo_bfs:.0f}"
            texto_pasos = f"Pasos: {len(self.ruta_bfs)}"
            self.pantalla.blit(self.fuente_pequena.render(texto_costo, True, COLORES['TEXTO']),
                               (panel_x + 10, y_offset))
            self.pantalla.blit(self.fuente_pequena.render(texto_pasos, True, COLORES['TEXTO']),
                               (panel_x + 10, y_offset + 20))

        if self.mostrar_mst:
            y_offset += 50
            costo_mostrar = self.costo_kruskal if self.aristas_kruskal else self.costo_mst
            nombre = "Kruskal" if self.aristas_kruskal else "Prim"
            texto_mst = f"MST {nombre} - Coste: {costo_mostrar:.0f}"
            self.pantalla.blit(self.fuente_pequena.render(texto_mst, True, COLORES['TEXTO']),
                               (panel_x + 10, y_offset))

        if self.mostrar_ciclos:
            y_offset += 30
            texto_ciclos = f"Ciclos: {len(self.ciclos)}"
            self.pantalla.blit(self.fuente_pequena.render(texto_ciclos, True, COLORES['TEXTO']),
                               (panel_x + 10, y_offset))

        #botones
        for boton in self.botones:
            boton.dibujar(self.pantalla, self.fuente_pequena)

    def manejar_click(self, pos):
        """Maneja los clics del ratón en el mapa"""
        if pos[0] >= TAM_CUADRICULA * TAM_CELDA:
            return  # Click en panel de control

        grid_x = pos[1] // TAM_CELDA
        grid_y = pos[0] // TAM_CELDA

        if self.mapa.grid[grid_x, grid_y] == 'MONTAÑA':
            return  # No se puede colocar en montañas

        if self.modo == 'establecer_inicio':
            self.mapa.inicio = (grid_x, grid_y)
            self.modo = 'establecer_meta'
        elif self.modo == 'establecer_meta':
            self.mapa.meta = (grid_x, grid_y)
            self.modo = 'listo'

    def run(self):
        """Bucle principal del juego"""
        ejecutando = True

        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    # Verificar botones primero
                    boton_clickeado = False
                    for boton in self.botones:
                        if boton.manejar_evento(evento):
                            boton_clickeado = True
                            break

                    # Si no se clickeó un botón, manejar click en mapa
                    if not boton_clickeado:
                        self.manejar_click(evento.pos)

                # Manejar hover de botones
                for boton in self.botones:
                    boton.manejar_evento(evento)

            # Actualizar animación
            if self.animando:
                self.paso_animacion += 1
                max_pasos = max(len(self.visitados_aestrella),
                                len(self.visitados_greedy),
                                len(self.visitados_bfs))
                if self.paso_animacion >= max_pasos:
                    self.animando = False

            #animacion de tom
            if self.animado_agente and self.camino_agente:
                self.contador_frames += 1
                if self.contador_frames >= self.frames_por_paso:
                    self.contador_frames = 0
                    self.indice_agente += 1

                    if self.indice_agente >= len(self.camino_agente):
                        self.indice_agente = len(self.camino_agente) - 1
                        self.animado_agente=False

            # Dibujar
            self.pantalla.fill((255, 255, 255))
            self.dibujar_grid()

            if self.animando or self.mostrar_ruta:
                self.dibujar_visitados()

            self.dibujar_ciclos()
            self.dibujar_mst()
            self.dibujar_caminos()
            self.dibujar_marcadores()
            self.dibujar_panel_control()

            pygame.display.flip()
            self.reloj.tick(FPS)

        pygame.quit()