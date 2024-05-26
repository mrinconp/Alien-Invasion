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
        self.prep_puntuacion()
        self.prep_mayor_puntuacion()
        self.prep_nivel()

    def prep_puntuacion(self):
        """Renderizar la puntuación a imagen"""
        rounded_puntuacion = round(self.stats.puntuacion, -1)
        puntuacion_str = "{:,}".format(rounded_puntuacion)
        self.puntuacion_image = self.font.render(puntuacion_str, True,
                                            self.text_color, self.config.bg_color)

        # Mostrar la puntuación en la esquina derecha superior de la pantalla
        self.puntuacion_rect = self.puntuacion_image.get_rect()
        self.puntuacion_rect.right = self.screen_rect.right - 20
        self.puntuacion_rect.top = 20

    def mostrar_puntuacion(self):
        """Dibujar la puntuación en la pantalla"""
        self.screen.blit(self.puntuacion_image, self.puntuacion_rect)
        self.screen.blit(self.mayor_puntuacion_image, self.mayor_puntuacion_rect) 
        self.screen.blit(self.nivel_image, self.nivel_rect)

    def prep_mayor_puntuacion(self):
        """Renderizar la mayor puntuación a imagen"""
        mayor_puntuacion = round(self.stats.mayor_puntuacion, -1)
        mayor_puntuacion_str = "{:,}".format(mayor_puntuacion)
        self.mayor_puntuacion_image = self.font.render(mayor_puntuacion_str, True,
                                            self.text_color, self.config.bg_color)
        
        # Centrar la mayor puntuacion en la parte superior de la pantalla
        self.mayor_puntuacion_rect = self.mayor_puntuacion_image.get_rect()
        self.mayor_puntuacion_rect.centerx = self.screen_rect.centerx
        self.mayor_puntuacion_rect.top = self.puntuacion_rect.top

    def check_mayor_puntuacion(self):
        """Revisar si hay una nueva mayor puntuacion"""
        if self.stats.puntuacion > self.stats.mayor_puntuacion:
            self.stats.mayor_puntuacion = self.stats.puntuacion
            self.prep_mayor_puntuacion()

    def prep_nivel(self):
        """Renderizar nivel a imagen"""
        nivel_str = str(self.stats.nivel)
        self.nivel_image = self.font.render(nivel_str, True,
                                            self.text_color, self.config.bg_color)
        
        #Posicionar nivel
        self.nivel_rect = self.nivel_image.get_rect()
        self.nivel_rect.right = self.puntuacion_rect.right
        self.nivel_rect.top = self.puntuacion_rect.bottom + 10


