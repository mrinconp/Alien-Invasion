import sys
import pygame

class AlienInvasion():
    """Características del juego y comportamiento"""
    def __init__(self):
        #Iniciar el juego y crear los recursos
        pygame.init()
        #Tamaño de la ventana
        self.screen = pygame.display.set_mode((1200, 800))
        #Nombre de la ventana
        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        """Se inicia el loop principal con un While"""
        while True:
            #Event loop para registrar eventos(acciones) del teclado y mouse
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            #Actualizar y hacer visible la pantalla
            pygame.display.flip()

if __name__ == '__main__':
    #Hacer una instancia con la clase y correr el juego con el metodo
    ai = AlienInvasion()
    ai.run_game()