class Config():
    """Establecer las configuraciones del juego"""
    
    def __init__(self):
        """Inicializar las configuraciones constantes del juego"""
        #Configuraciones de pantalla:
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0,0,0)

        #Config nave
        self.nave_limit = 3

        #Config alien
        self.manada_drop_speed = 150
        
        #Config balas
        self.bala_width = 1000
        self.bala_height = 15
        self.bala_color = (60,60,60)
        self.balas_max = 3

        #Config estrellas
        self.cantidad_estrellas = 200

        #Tasa de aumento de velocidad
        self.aumento_vel_escala = 1.1
        #Tasa de aumento puntuación
        self.puntuacion_escala = 1.5

        self.iniciar_config_dinamicas()

    def iniciar_config_dinamicas(self):
        """Inicializar las configuraciones que cambian a lo largo del juego"""
        self.nave_speed = 1.5
        self.bala_speed = 3.0
        self.alien_speed = 1.0

        #Direccion manada (1 derecha, -1 izquierda)
        self.manada_direction = 1

        #Puntaje
        self.alien_points = 50

    def aumentar_velocidad(self):
        """Aumentar la velocidad del juego y de la puntuación"""
        self.nave_speed *= self.aumento_vel_escala
        self.bala_speed *= self.aumento_vel_escala
        self.alien_speed *= self.aumento_vel_escala

        self.alien_points = int(self.alien_points * self.puntuacion_escala)