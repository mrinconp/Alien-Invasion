import pygame
from pygame.sprite import Sprite

class Bala(Sprite):
    """Una clase para las balas que dispara la nave"""
    def __init__(self, ai_game, shooter:str):
        """Crear un objeto 'bala' y posicionarlo"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.config
        self.color = self.settings.bala_color
        self.shooter = shooter

        match self.shooter:
            case "nave":
                self.rect = pygame.Rect(0,0, self.settings.bala_width, self.settings.bala_height)
                self.rect.midtop = ai_game.nave.rect.midtop
            case "jefe":
                self.rect = pygame.Rect(0,0, self.settings.bala_jefe_width, self.settings.bala_jefe_height)
                self.rect.midtop = ai_game.jefe.rect.midbottom

        #Guardar la posición como un decimal
        self.y = float(self.rect.y)
        #self.x = float(self.rect.x)

    def update(self):
        match self.shooter:
            case "nave":
                #Mover la bala hacia arriba
                self.y -= self.settings.bala_speed
            case "jefe":
                #Mover la bala en diagonal
                self.y += self.settings.bala_jefe_speed
                #self.x += self.settings.bala_jefe_speed

        #Actualizar posición
        self.rect.y = self.y
        #self.rect.y = self.x
    
    def draw_bala(self):
        #Dibujar la bala en la pantalla
        pygame.draw.rect(self.screen, self.color, self.rect)

        