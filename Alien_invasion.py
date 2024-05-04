import sys
import pygame
from settings import Config
from nave import Nave
from bullet import Bala
from alien import Alien

class AlienInvasion():
    """Características del juego y comportamiento"""
    def __init__(self):
        #Iniciar el juego y crear los recursos
        pygame.init()
        #Configuración general de la screen
        self.config = Config()

        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        
        #Aunque el código corre con FULLSCREEN, es bueno guardar como atributos la altura y ancho de la pantalla en caso de ser necesario
        #self.config.screen_width = self.screen.get_rect().width
        #self.config.screen_height = self.screen.get_rect().height

        self.screen = pygame.display.set_mode((1200,800))
        #Nombre de la ventana
        pygame.display.set_caption("Alien Invasion")

        self.nave = Nave(self)

        self.balas = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()

        self._crear_manada()

    def run_game(self):
        """Se inicia el loop principal con un While"""
        while True:
            self._check_events()
            self.nave.update()
            self._update_balas()
            self._update_screen()
             
    def _update_screen(self):
        #Aplicar color en cada iteración
        self.screen.fill(self.config.bg_color)
        self.nave.blitme()

        for bala in self.balas.sprites():
            bala.draw_bala()
        
        self.aliens.draw(self.screen)

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
        elif event.key == pygame.K_SPACE:
            self._disparar_bala()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.nave.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.nave.moving_left = False


    def _disparar_bala(self):
        if len(self.balas) < self.config.balas_max:
            nueva_bala = Bala(self)
            self.balas.add(nueva_bala)  

    def _update_balas(self):
        """Actualizar posición de las balas y eliminar las que salen de la pantalla"""
        #Actualizar posición
        self.balas.update()
        #Quitar balas que salen de la pantalla
        for bala in self.balas.copy():
            if bala.rect.bottom <= 0:
                self.balas.remove(bala)

    def _crear_manada(self):
        """Manada de aliens"""
        #Hacer un alien
        alien = Alien(self)
        self.aliens.add(alien)

if __name__ == '__main__':
    #Hacer una instancia con la clase y correr el juego con el metodo
    ai = AlienInvasion()
    ai.run_game()