import pygame.font

class Boton():
    def __init__(self, ai_game, msg):
        """Iniciar los atributos del botón"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        #Establecer las dimensiones y propiedades del botón
        self.width, self.height = 200,50
        self.color_boton = (0,255,0)
        self.color_texto = (255,255,255)
        self.font = pygame.font.SysFont(None, 48)

        #Construir el rectángulo y centrarlo
        self.rect = pygame.Rect(0,0,self.width, self.height)
        self.rect.center = self.screen_rect.center

        #Renderizar mensaje como imagen:
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Convertir mensaje a imagen y centrar el texto en el boton"""
        self.msg_imagen = self.font.render(msg,True, self.color_texto, self.color_boton)
        self.msg_imagen_rect = self.msg_imagen.get_rect()
        self.msg_imagen_rect.center = self.rect.center

    def draw_boton(self):
        """Dibujar botón en blanco y luego el mensaje"""
        self.screen.fill(self.color_boton, self.rect)
        self.screen.blit(self.msg_imagen, self.msg_imagen_rect)