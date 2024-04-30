import sys
import pygame
from settings import Config
from nave import Nave

class AlienInvasion():
    """Características del juego y comportamiento"""
    def __init__(self):
        #Iniciar el juego y crear los recursos
        pygame.init()
        #Configuración general de la screen
        self.config = Config()

        self.screen = pygame.display.set_mode((self.config.screen_width, self.config.screen_height))

        #Nombre de la ventana
        pygame.display.set_caption("Alien Invasion")

        self.nave = Nave(self)

    def run_game(self):
        """Se inicia el loop principal con un While"""
        while True:
            self._check_events()
            self.nave.update()
            self._update_screen()
            
    def _update_screen(self):
        #Aplicar color en cada iteración
        self.screen.fill(self.config.bg_color)
        self.nave.blitme()

        #Actualizar y hacer visible la pantalla
        pygame.display.flip()
    
    def _check_events(self):
        #Event loop para registrar eventos(acciones) del teclado y mouse
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type ==pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        #Mover la nave a la derecha:
                        self.nave.moving_right = True
                    elif event.key == pygame.K_LEFT:
                        self.nave.moving_left = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.nave.moving_right = False
                    elif event.key == pygame.K_LEFT:
                        self.nave.moving_left = False


if __name__ == '__main__':
    #Hacer una instancia con la clase y correr el juego con el metodo
    ai = AlienInvasion()
    ai.run_game()