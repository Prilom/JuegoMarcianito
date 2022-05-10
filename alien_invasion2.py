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

import sys
import pygame
from time import sleep  #con esta libreria podremos poner en pausa momentaneamente la pantalla cuando una nave sea alcanzada

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from gamestats import GameStats
from botton import Button
from scoreboard import Scoreboard
from initial_bg import Initial_bg
from explosiones import Explosion
from top5 import ScoreStore

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
HC74225 = (199, 66, 37)
H61CD35 = (97, 205, 53)

class AlienInvasion:
    """Clase general para gestionar los recursos y el comportamiento del juego"""

    def __init__(self):
        #iniciamos el juego y creamos recursos

        pygame.init()
        pygame.mixer.init()

        #Cargamos los sonidos del juego
        self.bg_sound= pygame.mixer.Sound("sounds/battleship.ogg")
        self.laser_sound=pygame.mixer.Sound("sounds/laser.wav")
        self.explosion=pygame.mixer.Sound("sounds/explosion.wav")
        self.level_change=pygame.mixer.Sound("sounds/cambionivel.wav")
        self.bg_sound.play()
        self.bg_sound.set_volume(0.1)

        #Creamos las instancias de las clases creadas en otros modulos
        self.settings=Settings()
        self.w,self.h=self.settings.w,self.settings.h

        #configuraciones de la pantalla
        self.screen =pygame.display.set_mode((self.w,self.h))
        self.FPS = self.settings.FPS
        self.RELOJ = pygame.time.Clock() #metodo que llama al reloj de pygame
        self.settings.screen_width=self.screen.get_rect().width
        self.settings.screen_height=self.screen.get_rect().height
        self.y=0
        self.x=0
        pygame.display.set_caption("Invasión Alien")
        self.top5=ScoreStore()
        self.stats=GameStats(self)#creamos una instancia para iniciar las estadísticas
        self.sb=Scoreboard(self)
        self.top5=ScoreStore()

        self.ship=Ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()

        self._create_fleet()

        self.play_button=Button(self,"Play")
        self.initial_bg=Initial_bg(self)

        #Creamos los sprites


        self.explosion_group=pygame.sprite.Group()



        self.game_over=False

    def run_game(self):
        """inicia el bucle principal para el juego"""

        while True:
            #busca eventos del teclado y del ratón
            self._check_events()
            #dentro de este if metemos solo las ejecuciones que se realicen mientras el juego esté activo
            if self.stats.game_active:
                self.ship.update() # metodo de la clase Ship que actualiza la posicion de la nave
                self._update_bullets() #metodo que actualiza las balas
                self._update_aliens()
                self._update_explosions()
                self._moving_backgroud()#metodo que actualiza el fondo movil
            self._update_screen()






    def _check_events(self):
        """Responde a las pulsaciones de las teclas del teclado y raton"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _moving_backgroud(self):
        """en este método generamos el movimiento del fondo, como queremos que se mueva de arriba a bajo, creamos una variable llamada y_relativa que es la division entera de la posicion del fondo en ese momento entre el alto del fondo\
        luego con el método blit posicionamos el fondo en el eje y restando la y_relativa - el alto del fondo. para que el movimiento sea fluido, añadimos un condicional en el que si la y_relativa es menor que la altura de la pantalla posicione\
        el fondo en la y_relativa"""

        y_relativa=self.y%self.screen.get_rect().height
        self.screen.blit(self.settings.fondo,(self.x,y_relativa-self.screen.get_rect().height))
        if y_relativa < self.h:
            self.screen.blit(self.settings.fondo,(self.x,y_relativa))
        self.y+=1
        self.RELOJ.tick(self.FPS)





    def _check_keydown_events(self,event):

        """Responde a las pulsaciones de las teclas"""

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullets()
            self.laser_sound.play()
            self.laser_sound.set_volume(1.0)

    def _check_keyup_events(self,event):
        """Responde a las liberaciones de las teclas"""

        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=False
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _check_play_button(self, mouse_pos):
        """inicia el juego nuevo cuando el juegador hace click en play"""
        button_clicked= self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active=True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            #nos desacemos de los aliens y las balas que quedan
            self.aliens.empty()
            self.bullets.empty()
            #Creamos una nueva flota y nave
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)


    def _fire_bullets(self):
        """Crea una nueva bala y la añade al grupo de balas"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        self.bullets.update()
        #creamos un bucle para desacernos de las balas que desaparecen en la parte superior de la pantalla
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)
        self._check_collision_bullets_aliens()

    def _check_collision_bullets_aliens(self):
        """este método comprueba si existe colision entre aliens y balas y en caso de True los destruye"""
        collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        #en base al numero de colisiones vamos sumando las puntuaciones
        #self.stats.alien_number_level=self.stats.alien_number
        if collisions:

            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points* len(aliens)
                self.stats.alien_number -= len(aliens)
                for alien in aliens:
                    x=alien.rect.centerx
                    y=alien.rect.centery
                    explosion=Explosion(x,y)
                    self.explosion_group.add(explosion)

            self.explosion.play()
            self.sb.prep_score()
            self.sb.check_high_score()
            self.sb.prep_aliens()
        #ahora comprabamos si la flota se ha destruido por completo, si True borramos las balas existentes y creamos otra flota
        if not self.aliens:
            self.level_change.play()
            self.bullets.empty()
            self.settings.increase_speed()
            self.stats.alien_number=self.settings.alien_number
            self._create_fleet()
            self.sb.prep_aliens()
            self.stats.level += 1 #cuando acabamos con la flota incrementamos en una unidad el nivek¡l
            self.sb.prep_level()

    def _update_explosions(self):

        self.explosion_group.update()
        self.explosion_group.draw(self.screen)

    def _create_fleet(self):
        """creamos una flota de aliens"""
        #creamos un alien y definimos las variables que contienen su ancho y alto
        self.alien_number=self.settings.alien_number
        for i in range(self.alien_number):
            alien= Alien(self)
            self.aliens.add(alien)


    def _create_alien(self, alien_number, row_number):

        alien=Alien(self)
        alien_width=alien.rect.width
        alien_height=alien.rect.height
        alien.x=alien_width + 2*alien_width*alien_number
        alien.y=alien_height + 2*alien_height*row_number
        alien.rect.x=alien.x
        alien.rect.y=alien.y
        self.aliens.add(alien)




    def _update_screen(self):

        if self.stats.game_active:

            #redibuja pa pantalla en cada paso por el bucle
            self.ship.blitme()

            #Creamos un bucle para dibujar las balas
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()

            self.explosion_group.draw(self.screen)

            self.aliens.draw(self.screen)
            self.sb.show_score()

        #Dibuja el boton si el juego está inactivo
        if not self.stats.game_active and self.game_over:
            self._game_over()
            self.sb.check_tp_5_values()
            self.sb.prep_top5_scores()


            self.play_button.draw_button()
        elif not self.stats.game_active and not self.game_over:
            self.initial_bg.blitme()
            self.play_button.draw_button()

        #hacemos visible la ultima pantalla dibuajda
        pygame.display.flip()

    def _update_aliens(self):
        """Actualiza las posiciones de la flota"""
        #self._check_fleet_edges()
        self.aliens.update()
        #comprobamos si existe colision entre nave y aliens
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        #Buscamos aliens llegando al fondo de la pantalla
        #self._check_aliens_bottom()



    def _ship_hit(self):
        """Responde a las colisiones de las naves con los aliens"""

        x=self.ship.rect.centerx
        y=self.ship.rect.centery
        explosion=Explosion(x,y)
        self.explosion_group.add(explosion)
        self.explosion.play()
        if self.stats.ship_left > 0:

            self.stats.ship_left -= 1

            #Nos desacemos de los aliens y balas restantes
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            #Creamos flota y nave nueva
            self.stats.alien_number=self.settings.alien_number
            self.sb.prep_aliens()
            self._create_fleet()
            self.ship.center_ship()
        else:
            self.stats.game_active=False
            self.game_over=True

            pygame.mouse.set_visible(True)

        sleep(0.5)

    def _game_over(self):
        screen_rect=self.screen.get_rect()
        game_over_image=pygame.image.load("images/gameoverphrase.png")
        rect=game_over_image.get_rect()
        center_x=(screen_rect.width//2) - (rect.width//2)
        center_y=(screen_rect.height//2) - (rect.height//2)
        self.screen.blit(game_over_image,[center_x,center_y])
        sleep(1)




    def _check_aliens_bottom(self):
        """COn este metodo comprobaremos si la flota llega al final de la pantalla"""
        screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break


    def _check_fleet_edges(self):
        """Responde en caso de que algun alien haya llegado al borde de la pantalla"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """baja los aliens un numero de posiciones indicada en settings(fleet_drop_speed) y modifica su dirección"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1



if __name__ == "__main__":
    ai=AlienInvasion()
    ai.run_game()
