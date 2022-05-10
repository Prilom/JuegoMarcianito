#-------------------------------------------------------------------------------
# Name:        módulo2
# Purpose:
#
# Author:      prilo
#
# Created:     18/03/2022
# Copyright:   (c) prilo 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class GameStats:
    """Con esta clase seguiremos las estadísticas del juego"""

    def __init__(self,ai_game):
        """constructor de  la estadísitica"""
        self.settings=ai_game.settings
        self.reset_stats()
        self.game_active=False # Bandera que permite la ejecucion del juego en base a las vidas
        #la puntuacion mas alta debería mantenerse y no resetearse, por eso la iniciamos en el constructor de la clase
        self.high_score=0


    def reset_stats(self):
        """inicializa las estadísticas"""

        self.ship_left= self.settings.ship_limit
        self.score=0
        self.level=1
        self.alien_number=10
