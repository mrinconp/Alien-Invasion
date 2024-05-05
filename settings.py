class Config():
    """Establecer las configuraciones del juego"""
    
    def __init__(self):
        """Inicializar las configuraciones del juego"""
        #Configuraciones de pantalla:
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0,0,0)

        #Velocidad nave
        self.nave_speed = 1.5

        #Config balas
        self.bala_speed = 1.0
        self.bala_width = 3
        self.bala_height = 15
        self.bala_color = (60,60,60)
        self.balas_max = 3

        #Config estrellas
        self.cantidad_estrellas = 200