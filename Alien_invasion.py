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
from jefe import Jefe

class AlienInvasion:
    """Clase principal para gestionar los recursos y el comportamiento del juego."""

    def __init__(self):
        pygame.mixer.pre_init(buffer=4096)
        pygame.init()
        self.config = Config()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.nave = Nave(self, 0.15)
        self.balas = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.balas_jefe = pygame.sprite.Group()
        self.last_shot_time = 0
        self.boton_play = Boton(self, "Jugar")

        self._make_sonidos()
        self._crear_flota()
        self._create_stars()

    def run_game(self):
        """Iniciar el bucle principal del juego."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.nave.update()
                self._update_balas(self.balas, "nave")
                self._update_aliens()
                if self.stats.nivel == self.config.nivel_jefe:
                    self.aliens.empty()
                    self.jefe.update()
                    self._update_balas(self.balas_jefe, "jefe")
                    self._check_jefe_shoot()
            self._update_screen()

    def _make_sonidos(self):
        """Inicializar y configurar los sonidos del juego."""
        self.bala_sound = pygame.mixer.Sound('recursos/laser_sound.wav')
        self.nave_hit_sound = pygame.mixer.Sound('recursos/nave_hit.wav')
        self.level_up_sound = pygame.mixer.Sound('recursos/level_up.wav')
        self.victory_sound = pygame.mixer.Sound('recursos/victory.wav')
        pygame.mixer.music.load('recursos/bg_music.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        self._set_volumenes()

    def _set_volumenes(self):
        """Establecer el volumen de los sonidos del juego."""
        self.bala_sound.set_volume(self.config.volumen_balas)
        self.nave_hit_sound.set_volume(self.config.volumen_vidas)
        self.level_up_sound.set_volume(self.config.volumen_level_up)

    def _update_screen(self):
        """Actualizar las imágenes en la pantalla y cambiar a la nueva pantalla."""
        self.screen.fill(self.config.bg_color)
        self.stars.draw(self.screen)
        self.nave.blitme()
        for bala in self.balas.sprites():
            bala.draw_bala()
        if self.stats.nivel == self.config.nivel_jefe:
            self.jefe.draw_jefe()
            for bala in self.balas_jefe.sprites():
                bala.draw_bala()
        else:
            self.aliens.draw(self.screen)
        self.sb.mostrar_puntuacion()
        if not self.stats.game_active:
            self.boton_play.draw_boton()
        pygame.display.flip()

    def _check_events(self):
        """Responder a las pulsaciones de teclas y eventos del ratón."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.save_mayor_puntuacion()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_boton_play(mouse_pos)

    def _check_boton_play(self, mouse_pos):
        """Iniciar un nuevo juego cuando el jugador hace clic en Play."""
        boton_clicked = self.boton_play.rect.collidepoint(mouse_pos)
        if boton_clicked and not self.stats.game_active:
            self._start_game()
            self.config.reset_config()
            self.sb.prep_images()

    def _start_game(self):
        """Reiniciar la configuración del juego y empezar un nuevo juego."""
        self.stats.reset_stats()
        self.stats.game_active = True

        self.aliens.empty()
        self.balas.empty()
        self.balas_jefe.empty()

        self._crear_flota()
        self.nave.centrar_nave()

        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.nave.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.nave.moving_left = True
        elif event.key == pygame.K_q:
            self.stats.save_mayor_puntuacion()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._disparar_bala("nave")
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()
            self.config.reset_config()
            self.sb.prep_images()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.nave.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.nave.moving_left = False

    def _disparar_bala(self, shooter: str):
        if shooter == "nave":
            if len(self.balas) < self.config.balas_max:
                nueva_bala = Bala(self, shooter)
                self.balas.add(nueva_bala)
                pygame.mixer.find_channel(True).play(self.bala_sound)
        elif shooter == "jefe":
            nueva_bala = Bala(self, shooter)
            self.balas_jefe.add(nueva_bala)

    def _update_balas(self, grupo_balas, shooter: str):
        """Actualizar la posición de las balas y eliminar las antiguas."""
        grupo_balas.update()
        for bala in grupo_balas.copy():
            if bala.rect.bottom <= 0 or bala.rect.top >= self.config.screen_height:
                grupo_balas.remove(bala)
        if shooter == "nave":
            self._check_colisiones_bala_alien()
        elif shooter == "jefe":
            self._check_colisiones_jefe_nave()
            self._check_colisiones_bala_jefe()

    def _check_colisiones_bala_alien(self):
        """Responder a las colisiones entre balas y aliens."""
        collisions = pygame.sprite.groupcollide(self.balas, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.puntuacion += self.config.alien_points * len(aliens)
            self.sb.prep_puntuacion()
            self.sb.check_mayor_puntuacion()

        if not self.aliens and self.stats.nivel != self.config.nivel_jefe:
            self._start_nuevo_nivel()

    def _check_colisiones_jefe_nave(self):
        """Comprobar las colisiones entre las balas del jefe y la nave."""
        for bala in self.balas_jefe.sprites():
            if bala.rect.colliderect(self.nave.rect):
                self._nave_hit()
                self.balas_jefe.remove(bala)

    def _check_colisiones_bala_jefe(self):
        """Comprobar las colisiones entre las balas de la nave y el jefe y reducir la salud del jefe."""
        for bala in self.balas.copy():
            if bala.rect.colliderect(self.jefe.rect):
                self._boss_hit()
                self.balas.remove(bala)

    def _start_nuevo_nivel(self):
        """Iniciar un nuevo nivel."""
        pygame.mixer.find_channel(True).play(self.level_up_sound)
        self.balas.empty()

        if self.stats.nivel + 1 == self.config.nivel_jefe:
            self.jefe = Jefe(self)
        else:
            self._crear_flota()

        self.config.aumentar_velocidad()
        self.stats.nivel += 1
        self.sb.prep_nivel()

    def _update_aliens(self):
        """Actualizar la posición de los aliens."""
        self._check_manada_bordes()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.nave, self.aliens):
            self._nave_hit()
        self._check_aliens_bottom()

    def _crear_flota(self):
        """Crear una flota completa de aliens."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        espacio_disponible_x = self.config.screen_width - (2 * alien_width)
        numero_aliens_x = espacio_disponible_x // (2 * alien_width)

        nave_height = self.nave.rect.height
        espacio_disponible_y = (self.config.screen_height - (3 * alien_height) - nave_height)
        numero_filas = espacio_disponible_y // (2 * alien_height)

        for row_number in range(numero_filas):
            for alien_number in range(numero_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = 10 + alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _create_stars(self):
        """Crear estrellas posicionadas aleatoriamente en el fondo."""
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
        """Comprobar si algún alien ha alcanzado los bordes de la pantalla y cambiar la dirección."""
        for alien in self.aliens.sprites():
            if alien.check_bordes():
                self._cambiar_direccion()
                break

    def _cambiar_direccion(self):
        """Bajar la flota y cambiar su dirección."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.config.manada_drop_speed
        self.config.manada_direction *= -1

    def _nave_hit(self):
        """Responder al impacto de la nave por un alien."""
        if self.stats.nave_left > 0:
            pygame.mixer.find_channel(True).play(self.nave_hit_sound)
            self.stats.nave_left -= 1
            self.sb.prep_naves()
            self.aliens.empty()
            self.balas.empty()
            self.balas_jefe.empty()
            self._crear_flota()
            self.nave.centrar_nave()
            sleep(0.5)
        else:
            pygame.mixer.find_channel(True).play(self.nave_hit_sound)
            self._end_game()

    def _boss_hit(self):
        """Reducir la salud del jefe y comprobar si ha sido derrotado."""
        if self.jefe.salud <= 0:
            self.stats.puntuacion += 500000
            self.sb.prep_puntuacion()
            self.sb.check_mayor_puntuacion()
            pygame.mixer.music.stop()
            pygame.mixer.find_channel(True).play(self.victory_sound)
            self._end_game()
        else:
            self.jefe.salud -= self.config.balas_daño

    def _check_jefe_shoot(self):
        """Comprobar si el jefe debe disparar una bala."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > 500:
            self._disparar_bala("jefe")
            self.last_shot_time = current_time

    def _check_aliens_bottom(self):
        """Comprobar si algún alien ha alcanzado la parte inferior de la pantalla."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._nave_hit()
                break

    def _end_game(self):
        """Terminar el juego y mostrar el cursor del ratón."""
        self.stats.game_active = False
        pygame.mouse.set_visible(True)

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
