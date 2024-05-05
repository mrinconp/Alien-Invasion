import pygame
from pygame.sprite import Sprite


class Star(Sprite):
    """Una clase para configurar las estrellas"""

    def __init__(self, ai_game):
        """Crear estrella y posicionarla"""
        super().__init__()

        self.screen = ai_game.screen

        #Cargar la imagen de la nave y su rectangulo
        self.raw = pygame.image.load('recursos/star1.bmp')
        self.image = pygame.transform.scale_by(self.raw, 0.01)
        self.rect = self.image.get_rect()

        #Iniciar cada estrella arriba a la izquierda de la pantalla
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        