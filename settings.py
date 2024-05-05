class Config():
    """Establecer las configuraciones del juego"""
    
    def __init__(self):
        """Inicializar las configuraciones del juego"""
        #Configuraciones de pantalla:
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0,0,0)

        #Config nave
        self.nave_speed = 1.5

        #Config alien
        self.alien_speed = 1.0
        self.manada_drop_speed = 10
        #Direccion(1 derecha, -1 izquierda)
        self.manada_direction = 1

        #Config balas
        self.bala_speed = 1.5
        self.bala_width = 3
        self.bala_height = 15
        self.bala_color = (60,60,60)
        self.balas_max = 3

        #Config estrellas
        self.cantidad_estrellas = 200