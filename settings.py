#-------------------------------------------------------------------------------
# Name:        módulo1
# Purpose:
#
# Author:      prilo
#
# Created:     10/03/2022
# Copyright:   (c) prilo 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pygame
class Settings:
    """esta clase guarda toda la confir+guración del juego"""

    def __init__(self):
        """Iniciamos la configuración del juego"""

        #Configuramos la pantalla
        self.w = 1920
        self.h = 1080
        self.bg_color=(230,230,230)
        self.fondo=pygame.image.load("images/fondonuevo.jpg")
        self.fondo_inicial=pygame.image.load("images/fondoinicial.jpg")

        #configuramos la nave
        self.ship_limit=1

        #configuración fondo movil
        self.FPS = 60 #velocidad a la que queremos que se mueva la pantalla

        #Configuramos las balas
        self.bullet_width=3
        self.bullet_height=15
        self.bullet_color=(255, 0, 0)
        self.bullet_allowed=15

        #Configuramos los aliens
        self.alien_number=10
        self.fleet_drop_speed=20

        #Configuramos el incremento en los puntos por aliens a medida que avanzamos pantallas
        self.score_scale=1.5

        #Configuramos la velocidad a la que acelera el juego
        self.speedup_scale=5

        #configuracion del movimiento del panel del top5
        self.velocidad_panel=2

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Inicializa las configuraciones que van cambiando durante el juego"""
        self.ship_speed=3
        self.alien_speed=2.0
        self.bullet_speed=5.0
        self.fleet_direction=1 # 1  dcha, -1 izda
        self.alien_points=50
        self.alien_number=10

    def increase_speed(self):
        """incrementa la configuracion de velocidad"""
        self.ship_speed *= self.speedup_scale/3
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= (self.speedup_scale)/4
        self.alien_number += 3
        self.alien_points = int(self.alien_points*self.score_scale)








