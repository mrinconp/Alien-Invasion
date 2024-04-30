import pygame

class Nave():
    """Una clase para configurar la nave"""

    def __init__(self, ai_game):
        """Crear la nave y posicionarla"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect() #rectangulo de la pantalla

        #Cargar la imagen de la nave y su rectangulo
        self.raw = pygame.image.load('recursos/Spaceship.bmp')
        self.image = pygame.transform.scale_by(self.raw, 0.1)
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Dibujar la nave en su posición"""
        self.screen.blit(self.image, self.rect)