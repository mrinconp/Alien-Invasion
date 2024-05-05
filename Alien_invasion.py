import sys
import pygame
import random
from settings import Config
from nave import Nave
from bullet import Bala
from alien import Alien
from star import Star

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

        #Nave
        self.nave = Nave(self)

        #Balas
        self.balas = pygame.sprite.Group()

        #Aliens
        self.aliens = pygame.sprite.Group()
        self._crear_manada()

        #Estrellas
        self.stars = pygame.sprite.Group()
        self._create_stars()

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
        #Dibujar estrellas
        self.stars.draw(self.screen)
        #Dibujar nave
        self.nave.blitme()
        #Dibujar balas
        for bala in self.balas.sprites():
            bala.draw_bala()
        #Dibujar aliens
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
        #Alien de referencia para medidas, no para incluir en la manada
        alien = Alien(self)
        
        alien_width, alien_height = alien.rect.size 
        espacio_disponible_x = self.config.screen_width - (2*alien_width)
        numero_aliens_x = espacio_disponible_x // (2*alien_width)

        #Determinar el número de filas
        nave_height = self.nave.rect.height
        espacio_disponible_y = (self.config.screen_height - 
                                (3*alien_height) - nave_height)
        numero_filas = espacio_disponible_y // (2*alien_height)
    
        #Crear manada
        for row_number in range(numero_filas):
            for alien_number in range(numero_aliens_x):
                #Crear un alien y posicionarlo
                self._create_alien(alien_number, row_number)
        

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        #Coordenadas del rectángulo donde se va a posicionar el alien
        alien.rect.x = alien_width + 2*alien_width*alien_number
        alien.rect.y = alien_height + 2*alien_height*row_number
        self.aliens.add(alien)


    def _create_stars(self):
        """Crear estrellas de forma aleatoria"""
        x_values = random.sample(range(self.config.screen_width), self.config.cantidad_estrellas)
        y_values = random.sample(range(self.config.screen_height), self.config.cantidad_estrellas)

        for i in range(self.config.cantidad_estrellas):
            x = x_values[i]
            y = y_values[i]
            self._create_star(x, y)

    def _create_star(self, x, y):
        star = Star(self)

        star.rect.x = x
        star.rect.y = y
        self.stars.add(star)

if __name__ == '__main__':
    #Hacer una instancia con la clase y correr el juego con el metodo
    ai = AlienInvasion()
    ai.run_game()