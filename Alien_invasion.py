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

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        
        #Aunque el código corre con FULLSCREEN, es bueno guardar como atributos la altura y ancho de la pantalla en caso de ser necesario
        self.config.screen_width = self.screen.get_rect().width
        self.config.screen_height = self.screen.get_rect().height

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
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.nave.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.nave.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.nave.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.nave.moving_left = False


if __name__ == '__main__':
    #Hacer una instancia con la clase y correr el juego con el metodo
    ai = AlienInvasion()
    ai.run_game()