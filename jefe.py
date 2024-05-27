import pygame

class Jefe():
    def __init__(self, ai_game):
        """Crear el Jefe y posicionarlo"""

        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.config = ai_game.config

        #Cargar la imagen de la nave y su rectangulo
        self.raw = pygame.image.load('recursos/jefe.bmp')
        self.image = pygame.transform.scale_by(self.raw, 0.7)
        self.rect = self.image.get_rect()

        #Posicionar jefe
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery - 100

        #Guardar la posición inicial exacta
        self.x = float(self.rect.x)

        #Salud
        self.salud = 10000

    def draw_jefe(self):
        """Dibujar el jefe en su posición y su vida"""
        self.screen.blit(self.image, self.rect)
        self._salud_rect()
        pygame.draw.rect(self.screen, self.color_salud, self.salud_rect)

    def update(self):
        """Mover el Jefe a la derecha o izquierda"""
        if self._check_bordes():
            self.config.direccion_jefe *= -1
        self.x += (self.config.jefe_speed * self.config.direccion_jefe)
        self.rect.x = self.x

    def _check_bordes(self):
        """True si se toca un borde de la pantalla"""
        if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
            return True
    
    def _salud_rect(self):
        """Atributos rectángulo salud"""
        self.salud_rect = pygame.Rect(0,0, self.salud//10, 30)
        self.salud_rect.centerx = self.screen_rect.centerx
        self.salud_rect.top = 100
        self.color_salud = (255,0,0)
