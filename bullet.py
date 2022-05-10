#-------------------------------------------------------------------------------
# Name:        módulo1
# Purpose:
#
# Author:      prilo
#
# Created:     16/03/2022
# Copyright:   (c) prilo 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Clase creada para gestionar las balas que lanza la nave"""

    def __init__(self,ai_game):
        """crea un objeto para la bala en la posicion actual de la nave"""
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.color=self.settings.bullet_color

        #Creamos un rectangulo para la bala en (0,0) y luego establece la posicion correcta
        self.rect=pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midtop=ai_game.ship.rect.midtop
        self.laser=ai_game.laser_sound


        self.y= float(self.rect.y)

    def update(self):
        """mueve la bala hacia arriba por la pantalla"""

        #Actualizamos la posicion decimal de la bala
        self.y -= self.settings.bullet_speed

        #actualiza la posición del rectangulo

        self.rect.y= self.y


    def draw_bullet(self):
        """ Dibuja la bala en pantalla"""

        pygame.draw.rect(self.screen, self.color, self.rect)
