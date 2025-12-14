#clase para botones interactivos
import pygame
from proyect_ia_m.ui.colores import COLORES

class Boton:

    def __init__(self, x,y,ancho, alto, texto, accion):
        self.rect = pygame.Rect(x,y,ancho,alto)
        self.texto = texto
        self.accion = accion
        self.esta_sobre = False

    def dibujar(self, pantalla, fuente):
        color = COLORES['BOTON_HOVER'] if self.esta_sobre else COLORES['BOTON']
        pygame.draw.rect(pantalla, color, self.rect)
        pygame.draw.rect(pantalla, COLORES['TEXTO'], self.rect, 2)

        texto_surf = fuente.render(self.texto, True, COLORES['TEXTO'])
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        pantalla.blit(texto_surf, texto_rect)

    def manejar_evento(self,evento):
        if evento.type == pygame.MOUSEMOTION:
            self.esta_sobre = self.rect.collidepoint(evento.pos) #indica que el mouse esta sobre el boton
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if self.esta_sobre:
                self.accion()
                return True
        return False