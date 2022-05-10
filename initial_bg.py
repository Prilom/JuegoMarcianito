#-------------------------------------------------------------------------------
# Name:        módulo1
# Purpose:
#
# Author:      prilo
#
# Created:     21/03/2022
# Copyright:   (c) prilo 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pygame

class Initial_bg:

    def __init__(self,ai_game):

        self.screen= ai_game.screen
        self.settings=ai_game.settings
        self.screen_rect=self.screen.get_rect()
        self.fondo=self.settings.fondo_inicial
        self.rect=self.fondo.get_rect()
        self.center()
        """elf.rect.x = self.x"""

        """self.fondo.x=(self.screen_rect.width-self.fondo_rect.width)//2

        self.fondo.y=(self.screen_rect.height-self.fondo_rect.height)//2"""
    def blitme(self):
        self.screen.blit(self.fondo,self.rect)

    def center(self):
        self.rect.center=self.screen_rect.center
        self.x=float(self.rect.x)

