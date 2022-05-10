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
from random import randrange





class Alien(Sprite):
    """clase que representa un solo alien en la flota"""

    def __init__(self,ai_game):
        """constructor que inicializa el alien y los meteoritos en una posición inicial aleatoria y actualiza su movimiento"""

        super().__init__()
        BLANCO = (255, 255, 255)
        NEGRO = (0, 0, 0)
        self.screen= ai_game.screen
        self.settings=ai_game.settings
        #Carga la imagen del alien
        self.image_random=randrange(3)
        if self.image_random==0:
            self.image = pygame.transform.scale(pygame.image.load("images/meteorito.png").convert(),(100,100))
            self.radius=50
        if self.image_random==1:
            self.image = pygame.transform.scale(pygame.image.load("images/alien.png").convert(),(60,60))
            self.radius=30
        if self.image_random==2:
            self.image = pygame.transform.scale(pygame.image.load("images/meteorito.png").convert(),(50,50))
            self.radius=25

        self.image.set_colorkey(NEGRO)
        self.rect=self.image.get_rect()

        self.rect.x=randrange(self.settings.w-self.rect.width)
        self.rect.y=-self.rect.width
        self.velocidad_y = randrange(1,10)


        #guarda la posicon horizontal exacta del alien

        self.x=float(self.rect.x)

    def update(self):
        """mueve el alien a la derecha"""
        self.rect.y+=self.velocidad_y
        if self.rect.top > self.settings.h:

            self.rect.x=randrange(self.settings.w-self.rect.width)
            self.rect.y = -self.rect.width
            self.velocidad = randrange(1, 10)