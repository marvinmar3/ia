import random
from heapq import heappush, heappop


class PRM:
    def __init__(self, mapa_juego, num_samples=100, radio_conexion=5):
        """
        Inicializa PRM

        Args:
            mapa_juego: Referencia al mapa del juego
            num_samples: Número de puntos aleatorios a generar
            radio_conexion: Radio máximo para conectar puntos
        """
        self.mapa = mapa_juego
        self.num_samples = num_samples
        self.radio_conexion = radio_conexion

        # Grafo de roadmap (waypoints y sus conexiones)
        self.waypoints = []  # Lista de puntos (x, y)
        self.conexiones = {}  # {punto: [puntos_conectados]}

    def generar_roadmap(self):
        """
        PASO 1: Genera el roadmap (grafo de waypoints)

        Proceso:
        1. Genera puntos aleatorios en espacios libres
        2. Conecta puntos cercanos si no hay obstáculos entre ellos
        """
        print(f"🗺️ Generando PRM con {self.num_samples} waypoints...")

        # PASO 1: Generar puntos aleatorios en espacios libres
        self.waypoints = []
        intentos = 0
        max_intentos = self.num_samples * 10

        while len(self.waypoints) < self.num_samples and intentos < max_intentos:
            x = random.randint(0, self.mapa.size - 1)
            y = random.randint(0, self.mapa.size - 1)

            # Solo agregar si NO es montaña
            if self.mapa.grid[x, y] != 'MONTAÑA':
                self.waypoints.append((x, y))

            intentos += 1

        print(f"   ✓ Generados {len(self.waypoints)} waypoints válidos")

        # PASO 2: Conectar puntos cercanos
        self.conexiones = {punto: [] for punto in self.waypoints}

        print(f"   → Conectando waypoints...")
        conexiones_hechas = 0

        for i, punto1 in enumerate(self.waypoints):
            for j, punto2 in enumerate(self.waypoints):
                if i >= j:  # Evitar duplicados
                    continue

                # Calcular distancia
                dist = self._distancia(punto1, punto2)

                # Si están cerca Y no hay obstáculos entre ellos
                if dist <= self.radio_conexion and self._camino_libre(punto1, punto2):
                    self.conexiones[punto1].append(punto2)
                    self.conexiones[punto2].append(punto1)
                    conexiones_hechas += 1

        print(f"   ✓ Creadas {conexiones_hechas} conexiones")

        return self.waypoints, self.conexiones

    def encontrar_camino(self, inicio, meta):
        """
        PASO 2: Encuentra camino usando el roadmap

        Proceso:
        1. Conecta inicio y meta al roadmap
        2. Usa A* sobre el roadmap (más rápido que grid completo)
        3. Retorna camino encontrado
        """
        if not self.waypoints:
            print("⚠️ Primero debes generar el roadmap!")
            return [], [], [], float('inf')

        print(f"🔍 Buscando camino de {inicio} a {meta}...")

        # Crear una copia de las conexiones para no modificar el roadmap original
        conexiones_temporales = {k: list(v) for k, v in self.conexiones.items()}

        # PASO 1: Conectar inicio y meta al roadmap
        print(f"   → Conectando inicio {inicio}...")
        inicio_conectado = self._conectar_punto_roadmap(inicio, conexiones_temporales)

        print(f"   → Conectando meta {meta}...")
        meta_conectada = self._conectar_punto_roadmap(meta, conexiones_temporales)

        if not inicio_conectado:
            print("❌ No se pudo conectar INICIO al roadmap")
            return [], [], [], float('inf')

        if not meta_conectada:
            print("❌ No se pudo conectar META al roadmap")
            return [], [], [], float('inf')


        # PASO 2: A* sobre el roadmap
        print(f"   → Ejecutando A* sobre roadmap...")
        camino_waypoints = self._a_estrella_roadmap(inicio, meta, conexiones_temporales)

        if not camino_waypoints:
            print("❌ No se encontró camino entre inicio y meta")
            return [], [], [], float('inf')

        # PASO 3: Calcular costo total
        costo_total = 0
        for i in range(len(camino_waypoints) - 1):
            costo_total += self._distancia(camino_waypoints[i], camino_waypoints[i + 1])

        print(f"✅ Camino encontrado: {len(camino_waypoints)} waypoints, costo {costo_total:.2f}")

        # Retornar en formato compatible con otros algoritmos
        visitados = self.waypoints  # Para visualizar todos los waypoints
        frontera = []

        return camino_waypoints, visitados, frontera, costo_total

    def _conectar_punto_roadmap(self, punto, conexiones):
        """
        Conecta un punto al roadmap buscando el waypoint más cercano accesible
        OPTIMIZADO: Solo revisa los K waypoints más cercanos
        """
        # Si el punto ya existe en el roadmap, ya está conectado
        if punto in conexiones:
            print(f"   ✓ Punto {punto} ya existe en roadmap")
            return True

        # Verificar que el punto no sea montaña
        x, y = punto
        if not (0 <= x < self.mapa.size and 0 <= y < self.mapa.size):
            print(f"   ❌ Punto {punto} fuera del mapa")
            return False
        if self.mapa.grid[x, y] == 'MONTAÑA':
            print(f"   ❌ Punto {punto} es montaña")
            return False

        # PASO 1: Calcular distancias a TODOS los waypoints (rápido)
        distancias = [(self._distancia(punto, w), w) for w in self.waypoints if w != punto]
        distancias.sort()  # Ordenar por distancia

        # PASO 2: Solo revisar los 20 MÁS CERCANOS (en vez de los 150)
        mejores_vecinos = []
        max_revisar = min(20, len(distancias))  # Máximo 20 o menos si hay pocos waypoints

        for i in range(max_revisar):
            dist, waypoint = distancias[i]

            # Si está dentro del radio Y el camino está libre
            if dist <= self.radio_conexion * 3:
                if self._camino_libre(punto, waypoint):
                    mejores_vecinos.append((dist, waypoint))
                    # Si ya encontramos 3 buenos, no buscar más
                    if len(mejores_vecinos) >= 3:
                        break

        # PASO 3: Si no encontramos nada, buscar el MÁS CERCANO sin importar el radio
        if not mejores_vecinos:
            print(f"   ⚠️ Punto {punto} lejos, buscando más cercanos...")
            for i in range(min(10, len(distancias))):
                dist, waypoint = distancias[i]
                if self._camino_libre(punto, waypoint):
                    mejores_vecinos.append((dist, waypoint))
                    break  # Con uno es suficiente

        # PASO 4: Conectar
        if mejores_vecinos:
            vecinos_seleccionados = [w for _, w in mejores_vecinos[:3]]

            # Agregar temporalmente al roadmap
            conexiones[punto] = vecinos_seleccionados
            for vecino in vecinos_seleccionados:
                if vecino not in conexiones:
                    conexiones[vecino] = []
                if punto not in conexiones[vecino]:  # Evitar duplicados
                    conexiones[vecino].append(punto)

            print(f"   ✓ Conectado {punto} a {len(vecinos_seleccionados)} waypoints")
            return True

        print(f"   ❌ No se pudo conectar {punto} al roadmap")
        return False

    def _a_estrella_roadmap(self, inicio, meta, conexiones):
        """A* simplificado sobre el roadmap"""
        frontera = []
        heappush(frontera, (0, inicio))

        vino_de = {inicio: None}
        costo_hasta_ahora = {inicio: 0}

        # Límite de iteraciones para evitar bucles infinitos
        max_iteraciones = len(conexiones) * 10
        iteracion = 0

        while frontera and iteracion < max_iteraciones:
            iteracion += 1
            _, actual = heappop(frontera)

            if actual == meta:
                break

            # Evitar revisitar nodos ya procesados con mejor costo
            if actual in costo_hasta_ahora and costo_hasta_ahora.get(actual, float('inf')) < costo_hasta_ahora.get(actual, 0):
                continue

            # Explorar vecinos en el roadmap
            for vecino in conexiones.get(actual, []):
                nuevo_costo = costo_hasta_ahora[actual] + self._distancia(actual, vecino)

                if vecino not in costo_hasta_ahora or nuevo_costo < costo_hasta_ahora[vecino]:
                    costo_hasta_ahora[vecino] = nuevo_costo
                    prioridad = nuevo_costo + self._distancia(vecino, meta)
                    heappush(frontera, (prioridad, vecino))
                    vino_de[vecino] = actual

        if iteracion >= max_iteraciones:
            print(f"   ⚠️ A* alcanzó límite de {max_iteraciones} iteraciones")

        # Reconstruir camino
        if meta not in vino_de:
            return []

        camino = []
        actual = meta
        visitados_reconstruccion = set()  # Evitar bucles en reconstrucción
        while actual is not None and actual not in visitados_reconstruccion:
            visitados_reconstruccion.add(actual)
            camino.append(actual)
            actual = vino_de.get(actual)

        camino.reverse()
        return camino

    def _distancia(self, p1, p2):
        """Distancia Manhattan (compatible con el grid)"""
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def _camino_libre(self, p1, p2):
        """
        Verifica si hay camino libre entre dos puntos (sin montañas)
        Usa muestreo simple (más rápido que Bresenham)
        """
        x0, y0 = p1
        x1, y1 = p2

        # Verificar límites
        if not (0 <= x0 < self.mapa.size and 0 <= y0 < self.mapa.size):
            return False
        if not (0 <= x1 < self.mapa.size and 0 <= y1 < self.mapa.size):
            return False

        # Verificar que inicio y fin no sean montañas
        if self.mapa.grid[x0, y0] == 'MONTAÑA' or self.mapa.grid[x1, y1] == 'MONTAÑA':
            return False

        # Calcular número de puntos a muestrear
        dist = abs(x1 - x0) + abs(y1 - y0)
        num_muestras = min(dist + 1, 30)  # Máximo 30 muestras

        # Muestrear puntos a lo largo de la línea
        for i in range(num_muestras):
            t = i / max(num_muestras - 1, 1)  # 0 a 1
            x = int(x0 + t * (x1 - x0))
            y = int(y0 + t * (y1 - y0))

            # Verificar límites
            if not (0 <= x < self.mapa.size and 0 <= y < self.mapa.size):
                return False

            # Verificar obstáculo
            if self.mapa.grid[x, y] == 'MONTAÑA':
                return False

        return True