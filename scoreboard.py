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

import pygame.font
from pygame.sprite import Group

from ship import Ship
import re


class Scoreboard:
    """clase que gestionará la información sobre las puntuaciones"""

    def __init__(self,ai_game):
        """inicializa los atributos de la puntuación"""
        self.screen=ai_game.screen
        self.ai_game=ai_game
        self.screen_rect=self.screen.get_rect()
        self.settings=ai_game.settings
        self.stats=ai_game.stats
        self.top5=ai_game.top5

        #Configuramos la fuente y el tamaño para la puntuación
        self.text_color=(30,30,30)
        self.font=pygame.font.SysFont(None,58)

        #Preparamos la imagen de puntuación inicial
        self.prep_score()
        self.prep_high_score() #Puntuacion máxima
        self.prep_aliens()
        self.prep_level()#devuelve el nivel en el que estamos
        self.prep_ships()#Creamos las naves que representan las vidas

    def prep_score(self):
        """Con este método convertimos las puntuaciones en una imagen renderizada"""
        rounded_score=round(self.stats.score,-1)
        score_str="Puntos:{:,}".format(rounded_score)
        self.score_imagen = self.font.render(score_str,self.text_color,self.settings.bg_color)

        #Muestra la puntuación en la parte superior derecha de la pantalla
        self.score_rect=self.score_imagen.get_rect()
        self.score_rect.right=self.screen_rect.right -20
        self.score_rect.top=20

    def prep_high_score(self):
        """Convierte la puntuacion máxima en una imagen renderizada"""
        high_score=round(self.stats.high_score, -1)
        high_score_str = "Máx Puntuación: {:,}".format(high_score)
        self.high_score_image=self.font.render(high_score_str,self.text_color,self.settings.bg_color)

        #Centramos la puntuacion maxima en el centro de la pantalla superior
        self.high_score_rect=self.high_score_image.get_rect()
        self.high_score_rect.centerx=self.screen_rect.centerx+200
        self.high_score_rect.top=20

    def prep_level(self):
        """Convertimos el nivel en el que estamos en una imagen para mostrarlo en pantalla"""
        level_str="Level: {}".format(str(self.stats.level))
        self.level_image=self.font.render(level_str,self.text_color, self.settings.bg_color)
        self.level_rect=self.level_image.get_rect()
        self.level_rect.right=self.score_rect.right
        self.level_rect.top=self.score_rect.top + 50

    def prep_top5_scores(self):
        """Muestra en la pantalla GameOver las 5 mejores puntuaciones"""
        scores=self.save_values_int
        screen="Mejores puntuaciones:"
        screen_image=self.font.render(screen,self.text_color,self.settings.bg_color)
        screen_image_rect=screen_image.get_rect()
        screen_image_rect.centerx=self.screen_rect.centerx
        screen_image_rect.top=680
        self.screen.blit(screen_image,screen_image_rect)
        n=0
        initial=740
        for i in scores:
            if n<5:
                n+=1
                screen=f"{n}. {i}"
                screen_image=self.font.render(screen,self.text_color,self.settings.bg_color)
                screen_image_rect=screen_image.get_rect()
                screen_image_rect.centerx=self.screen_rect.centerx
                screen_image_rect.top=initial
                initial += 60
                self.screen.blit(screen_image,screen_image_rect)

    """def update_top5(self):
        mueve las 5 mejores puntuaciones de iza a dcha
        rect=self.screen_top5_image_rect
        rect_x=rect.x

        if rect_x<=200:
            rect_x=self.screen_rect.center+300

        else:
            rect_x -= self.settings.velocidad_panel"""

    def show_top5(self):

        self.screen.blit(self.screen_top5_image,self.screen_top5_image_rect)

    def prep_aliens(self):
        """devuelve en pantalla los aliens que quedan en el nivel en el que estamos"""
        alien_number_str=f"Enemigos vivos: {str(self.stats.alien_number)}"
        self.alien_number_image=self.font.render(alien_number_str,self.text_color,self.settings.bg_color)

        #posicionamos el nº de aliens en la pantalla
        self.alien_number_image_rect=self.alien_number_image.get_rect()
        self.alien_number_image_rect.x=self.screen_rect.centerx-500
        self.alien_number_image_rect.y=10

    def prep_ships(self):
        """Muestra cuantas naves/vidas quedan"""
        self.ships=Group()
        for ship_number in range(self.stats.ship_left):
            ship=Ship(self.ai_game)

            ship.rect.x=10 + ship_number * ship.rect.width
            ship.rect.y= 10
            self.ships.add(ship)

    def show_score(self):
        """dibuja la puntuación en la pantalla"""
        self.screen.blit(self.score_imagen, self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.screen.blit(self.alien_number_image,self.alien_number_image_rect)

        self.ships.draw(self.screen)

    def check_high_score(self):
        """comprueba si la puntuacion actual es mayor que la maxima"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def check_tp_5_values(self):
        self.top5.read_file()
        self.lines=self.top5.lines
        high_score=round(self.stats.high_score, -1)
        self.save_values_int=[]
        character="\n"
        values = [int(values) for values in re.findall(r'-?\d+\.?\d*', self.lines)]

        for value in values:
            self.save_values_int.append(int(value))
        self.save_values_int.append(high_score)

        self.save_values_int.sort(reverse=True)

        new_top5=f"{str(self.save_values_int[0])}\n{str(self.save_values_int[1])}\n{str(self.save_values_int[2])}\n{str(self.save_values_int[3])}\n{str(self.save_values_int[4])}"
        self.top5.top_5_score_anadir(new_top5)





