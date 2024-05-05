import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Una clase para configurar los aliens"""

    def __init__(self, ai_game):
        """Crear el alien y posicionarlo"""
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.config

        #Cargar la imagen de la nave y su rectangulo
        self.raw = pygame.image.load('recursos/alien1.bmp')
        self.image = pygame.transform.scale_by(self.raw, 0.1)
        self.rect = self.image.get_rect()

        #Iniciar cada alien arriba a la izquierda de la pantalla
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Guardar la posición inicial exacta
        self.x = float(self.rect.x)

    def update(self):
        """Mover el alien a la derecha o izquierda"""
        self.x += (self.settings.alien_speed *
                        self.settings.manada_direction)
        self.rect.x = self.x

    def check_bordes(self):
        """True si un alien toca un borde de la pantalla"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True