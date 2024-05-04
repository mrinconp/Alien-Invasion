import pygame

class Nave():
    """Una clase para configurar la nave"""

    def __init__(self, ai_game):
        """Crear la nave y posicionarla"""
        self.screen = ai_game.screen
        self.settings = ai_game.config
        self.screen_rect = ai_game.screen.get_rect() #rectangulo de la pantalla

        #Cargar la imagen de la nave y su rectangulo
        self.raw = pygame.image.load('recursos/nave1.bmp')
        self.image = pygame.transform.scale_by(self.raw, 0.15)
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        #Flag de movimiento
        self.moving_right = False
        self.moving_left = False

    def update(self):
        #Actualizar la posicion de la nave basado en la bandera de movimiento

        #Revisar si está activa la bandera de movimiento y que el extremo derecho del rectángulo de la nave no sea mayor que el de la pantalla
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.nave_speed
        
        #Revisar si está activa la bandera de movimiento y que el extremo izquierdo del rectángulo de la nave sea mayor a 0 
        #(recordar que las coordenadas tienen origen en el extremo sup izq de la pantalla)
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.nave_speed

        self.rect.x = self.x

    def blitme(self):
        """Dibujar la nave en su posición"""
        self.screen.blit(self.image, self.rect)