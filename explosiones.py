#-------------------------------------------------------------------------------
# Name:        módulo1
# Purpose:
#
# Author:      prilo
#
# Created:     22/03/2022
# Copyright:   (c) prilo 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pygame
from pygame.sprite import Sprite

"""class Explosion(Sprite):

    def __init__(self,posx,posy):
        super().__init__()
        self.explosion_list=[]
        for i in range(1,13):
            file=f"images/explosion{i}.PNG"
            img=pygame.image.load(file)
            #img_scale=pygame.transform.scale(img,(70,70))
            self.explosion_list.append(img)
        self.frame=0
        self.image=self.explosion_list[self.frame]
        self.rect=self.image.get_rect()
        self.rect.center=[posx,posy]

        self.counter=0


    def update(self):
        explosion_speed= 3
        self.counter+=1

        if self.counter >= explosion_speed and self.frame < len(self.explosion_list)-1:
            self.counter=0
            self.frame += 1
            self.image=self.explosion_list[self.frame]

        if self.counter >= explosion_speed and self.frame >= len(self.explosion_list)-1:
            self.kill()"""



class Explosion(Sprite):

    def __init__(self,posx,posy):
        super().__init__()
        self.explosion_list=[]
        for i in range(1,13):
            file=f"images/explosion{i}.PNG"
            img=pygame.image.load(file)
            #img_scale=pygame.transform.scale(img,(70,70))
            self.explosion_list.append(img)
        self.frame=0
        self.image=self.explosion_list[self.frame]
        self.rect=self.image.get_rect()
        self.center=[posx,posy]
        self.rect.center=self.center
        self.last_update=pygame.time.get_ticks()
        self.frame_rate=50

    def update(self):

        now=pygame.time.get_ticks()
        if now - self.last_update >self.frame_rate:
            self.last_update=now
            self.frame += 1
            if self.frame == len(self.explosion_list)-1:
                self.kill()
            else:
                self.center=self.rect.center
                self.image=self.explosion_list[self.frame]
                self.rect=self.image.get_rect()
                self.rect.center=self.center
