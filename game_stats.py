class GameStats():
    """Registrar estadísticas del juego"""

    def __init__(self, ai_game):
        """Iniciar estadísticas"""
        self.config = ai_game.config
        self.reset_stats()
        #Iniciar el juego en un estado Activo
        self.game_active = False

    def reset_stats(self):
        """Iniciar estadísticas que pueden cambiar durante el juego"""
        self.nave_left = self.config.nave_limit