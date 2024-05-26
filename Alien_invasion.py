import sys
from time import sleep

import pygame
import random
from settings import Config
from nave import Nave
from bullet import Bala
from alien import Alien
from star import Star
from game_stats import GameStats
from boton import Boton
from tablapuntos import Scoreboard

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

        #Estadísticas y puntuación
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

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

        #Boton Jugar
        self.boton_play = Boton(self, "Jugar")


    def run_game(self):
        """Se inicia el loop principal con un While"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.nave.update()
                self._update_balas()
                self._update_aliens()

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
        #Dibujar la puntuación
        self.sb.mostrar_puntuacion()
        #Dibujar botón si el juego está inactivo
        if not self.stats.game_active:
            self.boton_play.draw_boton()

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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_boton_play(mouse_pos)

    def _check_boton_play(self, mouse_pos):
        """Empezar el juego cuando se da click a Jugar"""
        boton_clicked = self.boton_play.rect.collidepoint(mouse_pos)
        if boton_clicked and not self.stats.game_active:
            self._start_game()
            #Reiniciar las configuraciones
            self.config.iniciar_config_dinamicas()
            self.sb.prep_score()
            
    def _start_game(self):
        #Reiniciar stats
        self.stats.reset_stats()
        self.stats.game_active = True

        #Eliminar aliens y balas
        self.aliens.empty()
        self.balas.empty()

        #Crear nueva manada y centrar la nave
        self._crear_manada()
        self.nave.centrar_nave()

        #Esconder mouse
        pygame.mouse.set_visible(False)


    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.nave.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.nave.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._disparar_bala()
        elif event.key == pygame.K_p:
            self._start_game()

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

        self._check_colisiones_bala_alien()
        
    def _check_colisiones_bala_alien(self):
        #Revisar colisiones y borrar alien dado el caso
            #Los dos argumentos True borran los elementos que colisionan
        collisions = pygame.sprite.groupcollide(
            self.balas, self.aliens, True, True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.puntuacion += self.config.alien_points * len(aliens)
            self.sb.prep_score()

        if not self.aliens:
            #Eliminar balas existentes y crear nueva manada de aliens
            self.balas.empty()
            self._crear_manada()
            self.config.aumentar_velocidad()

    def _update_aliens(self):
        self._check_manada_bordes()
        self.aliens.update()

        #Revisar colisión alien-nave
        if pygame.sprite.spritecollideany(self.nave, self.aliens):
            self._nave_hit()

        #Revisar aliens llegando al final de la pantalla
        self._check_aliens_bottom()

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
        alien.x = alien_width + 2*alien_width*alien_number
        alien.rect.x = alien.x
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

    def _check_manada_bordes(self):
        for alien in self.aliens.sprites():
            if alien.check_bordes():
                self._cambiar_direccion()
                break

    def _cambiar_direccion(self):
        """Bajar la manada y cambiar la direccion"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.config.manada_drop_speed
        self.config.manada_direction *= -1

    def _nave_hit(self):
        """Respuesta a colisiones alien-nave"""
        if self.stats.nave_left > 0:
            #Restar naves restantes:
            self.stats.nave_left -= 1

            #Eliminar aliens y balas
            self.aliens.empty()
            self.balas.empty()

            #Crear nueva manada y centrar la nave
            self._crear_manada()
            self.nave.centrar_nave()

            #Pausa
            sleep(0.5)
            
        else:
            self.stats.game_active = False
            #Mouse visible de nuevo
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Revisar si algún alien llega al final de la pantalla"""
        screen_rect = self.screen.get_rect()

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Hacer lo mismo que cuando hay colisión alien-nave:
                self._nave_hit()
                break

if __name__ == '__main__':
    #Hacer una instancia con la clase y correr el juego con el metodo
    ai = AlienInvasion()
    ai.run_game()