# diccionario de terrenos ; tipos y sus costes
import pygame
import os

class TIPOS_TERRENO:
    #definicion de terrenos con textura
    @staticmethod
    def cargar_texturas(tam_celda):

        texturas = {}

        #rutas de las texturas
        rutas = {
            'LLANURA': 'assets/terrenos/llanura.png',
            'BOSQUE':'assets/terrenos/bosque.png',
            'PANTANO': 'assets/terrenos/pantano.png',
            'AGUA': 'assets/terrenos/agua.png',
            'MONTAÑA': 'assets/terrenos/montana.png'
        }

        #cargar y escalar cada textura
        for tipo, ruta in rutas.items():
            if os.path.exists(ruta):
                img = pygame.image.load(ruta).convert()
                img= pygame.transform.scale(img, (tam_celda, tam_celda))
                texturas[tipo] = img
            else:
                #fallback: usar colores si no existe la textura
                print(f"Textura no encontrada: {ruta}, usando color por defecto")
                texturas[tipo] = None
        return texturas


    COLORES = {
        'LLANURA': (144, 238, 144),
        'BOSQUE': (34, 139, 34),
        'PANTANO': (139, 115, 85),
        'AGUA': (64, 164, 223),
        'MONTAÑA': (128, 128, 128)
    }

    INFO = {
        'LLANURA': {'costo': 1, 'nombre': 'Llanura'},
        'BOSQUE': {'costo': 2, 'nombre': 'Bosque'},
        'PANTANO': {'costo': 3, 'nombre': 'Pantano'},
        'AGUA': {'costo': 5, 'nombre': 'Agua'},
        'MONTAÑA': {'costo': float('inf'), 'nombre': 'Montaña'}
    }