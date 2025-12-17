import pygame as pg
import nivel_settings as ns
from entidad import Entidad
import random as rd

class Enemigo(Entidad):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.vida = 50
        self.dano = 5
        self.velocidad = rd.randint(1, 2)

        self.cooldown = 1000
        self.ultimo_ataque = 0

        self.hitbox = pg.Rect(self.x, self.y, 64, 64)
        self.ataque_hitbox = pg.Rect(self.rect.centerx, self.rect.centery, 64, 64)

        self.frame_milisegundos = 100
        self.frame_milisegundos_ataque = 10

        self.tiempo_de_inicio = pg.time.get_ticks()

        if len(self.frames_ataque) > 0:
            self.imagen_ataque = self.frames_ataque[0]

    def movimiento(self, jugador):
        tiempo_actual = pg.time.get_ticks()

        if self.hitbox.centerx > jugador.hitbox.centerx + 60:
            self.rect.x -= self.velocidad
            self.direccion = "IZQUIERDA"
            self.flip = True

        elif self.hitbox.centerx < jugador.hitbox.centerx - 60:
            self.rect.x += self.velocidad
            self.direccion = "DERECHA"
            self.flip = False

        self.hitbox.center = self.rect.center

        if self.direccion == "DERECHA":
            self.ataque_hitbox = pg.Rect(self.rect.centerx + 15, self.rect.centery - 32, 64, 64)
        else:
            self.ataque_hitbox = pg.Rect(self.rect.centerx - 79, self.rect.centery - 32, 64, 64)

        # 🔥 DAÑO AL JUGADOR (ESTO ES LO QUE FALTABA)
        if self.ataque_hitbox.colliderect(jugador.hitbox):
            if tiempo_actual - self.ultimo_ataque > self.cooldown:
                jugador.vida -= self.dano
                self.ultimo_ataque = tiempo_actual
                self.atacando = True

        if self.atacando:
            self.animar_ataque()


class EnemigoPequeno(Enemigo):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.sprite_quieto = pg.image.load(
            "assets/images/sprites_enemigos/enemigo_prueba.png"
        ).convert_alpha()

        self.imagen = self.sprite_quieto
