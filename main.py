"""
EL RESCATE DEL EXPLORADOR PERDIDO
Punto de entrada principal del juego
"""

from modelos.mapa_juego import MapaJuego
from ui.visualizador import Visualizador


def main():
    """Función principal que inicia el juego"""
    print("=" * 70)
    print("EL RESCATE DEL EXPLORADOR PERDIDO")
    print("=" * 70)
    print("\nInstrucciones:")
    print("1. Click en el mapa para colocar la Unidad de Rescate (verde)")
    print("2. Click nuevamente para colocar la Baliza (roja)")
    print("3. Usa los botones del panel para ejecutar algoritmos")
    print("\nAlgoritmos disponibles:")
    print("- A*: Encuentra el camino con menor coste total")
    print("- Greedy: Rápido pero no siempre óptimo")
    print("- BFS: Menor número de pasos")
    print("- MST (Prim/Kruskal): Árbol de expansión mínima")
    print("- Detección de Ciclos: Identifica regiones con rutas redundantes")
    print("- Generación Perlin Noise: Terreno realista")
    print("- Generación Cellular Automata: Cuevas orgánicas")
    print("=" * 70)

    # Crear mapa y visualizador
    mapa = MapaJuego()
    visualizador = Visualizador(mapa)

    # Iniciar el juego
    visualizador.run()