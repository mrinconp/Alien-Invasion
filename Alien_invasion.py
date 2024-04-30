import sys
import pygame
from settings import Config

class AlienInvasion():
    """Características del juego y comportamiento"""
    def __init__(self):
        #Iniciar el juego y crear los recursos
        pygame.init()
        #Configuración general de la pantalla
        self.config = Config()

        self.pantalla = pygame.display.set_mode(self.config.altura_pantalla, self.config.ancho_pantalla)

        #Nombre de la ventana
        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        """Se inicia el loop principal con un While"""
        while True:
            #Event loop para registrar eventos(acciones) del teclado y mouse
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sys.exit()
            
            #Aplicar color en cada iteración
            self.pantalla.fill(self.config.bg_color)

            #Actualizar y hacer visible la pantalla
            pygame.display.flip()

if __name__ == '__main__':
    #Hacer una instancia con la clase y correr el juego con el metodo
    ai = AlienInvasion()
    ai.run_game()