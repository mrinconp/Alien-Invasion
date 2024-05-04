import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Una clase para configurar los aliens"""

    def __init__(self, ai_game):
        """Crear el alien y posicionarlo"""
        super().__init__()

        self.screen = ai_game.screen

        #Cargar la imagen de la nave y su rectangulo
        self.raw = pygame.image.load('recursos/alien1.bmp')
        self.image = pygame.transform.scale_by(self.raw, 0.15)
        self.rect = self.image.get_rect()

        #Iniciar cada alien arriba a la izquierda de la pantalla
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Guardar la posición inicial exacta
        self.x = float(self.rect.x)
        