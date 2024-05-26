class GameStats():
    """Registrar estadísticas del juego"""

    def __init__(self, ai_game):
        """Iniciar estadísticas"""
        self.config = ai_game.config
        self.reset_stats()
        #Iniciar el juego en un estado inactivo
        self.game_active = False
        #Mayor puntuacion
        file = open('save/mayor_puntuacion.txt',"r")
        self.mayor_puntuacion= int(file.read())

    def reset_stats(self):
        """Iniciar estadísticas que pueden cambiar durante el juego"""
        self.nave_left = self.config.nave_limit
        self.puntuacion = 0
        self.nivel = 1

    def save_mayor_puntuacion(self):
        """Guardar la mayor puntuacion una vez se supera la anterior"""
        if self.puntuacion >= self.mayor_puntuacion:
            file = open('save/mayor_puntuacion.txt',"w")
            nueva_puntuacion = str(self.puntuacion)
            file.write(nueva_puntuacion)
            file.close()