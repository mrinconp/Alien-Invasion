import pygame.font

class Scoreboard():
    """Una clase para registrar la puntuación"""

    def __init__(self, ai_game):
        """Inicializar los atributos de la tabla"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.config = ai_game.config
        self.stats = ai_game.stats

        #Configuración de la fuente
        self.text_color = (250,250,250)
        self.font = pygame.font.SysFont(None, 48)

        #Preparar la imagen de puntuación inicial
        self.prep_score()

    def prep_score(self):
        """Renderizar la puntuación a imagen"""
        score_str = str(self.stats.puntuacion)
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.config.bg_color)

        # Mostrar la puntuación en la esquina derecha superior de la pantalla
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def mostrar_puntuacion(self):
        """Dibujar la puntuación en la pantalla"""
        self.screen.blit(self.score_image, self.score_rect)
