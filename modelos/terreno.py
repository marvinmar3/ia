# diccionario de terrenos ; tipos y sus costes

TIPOS_TERRENO = {
    'LLANURA': {'costo':1, 'color':(144,238,144), 'nombre': 'Llanura'},
    'BOSQUE': {'costo': 2, 'color': (34,139,34), 'nombre': 'Bosque'},
    'PANTANO': {'costo':3, 'color': (139,115,85), 'nombre': 'Pantano'},
    'AGUA':{'costo': 5, 'color': (64,164,223), 'nombre': 'Agua'},
    'MONTAÑA':{'costo': float('inf'), 'color':(128,128,128), 'nombre': 'Montaña'} #terreno intransitable
}