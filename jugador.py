import pygame as pg
from entidad import Entidad
from settings import SONIDO_ATAQUE, VOLUMEN_SFX

class Jugador(Entidad):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.frame = 0
        self.frame_ataque = 0
        
        # Cargando sonidos nuevos
        self.sonido_ataque = pg.mixer.Sound("assets/sonidos/ataque.wav")
        self.sonido_dano = pg.mixer.Sound("assets/sonidos/dano_jugador.ogg")

        # Sprites
        self.sprite_girando = pg.image.load("assets/images/personajes/giro_aire.png").convert_alpha()
        self.sprite_dash = pg.image.load("assets/images/personajes/dash.png").convert_alpha()
        self.sprite_salud = pg.image.load("assets/images/corazones/corazones_100.png").convert_alpha()

        # Sprites barra salud:
        self.sprites_corazones = [
            pg.image.load("assets/images/corazones/corazones_0.png").convert_alpha(),
            pg.image.load("assets/images/corazones/corazones_10.png").convert_alpha(),
            pg.image.load("assets/images/corazones/corazones_20.png").convert_alpha(),
            pg.image.load("assets/images/corazones/corazones_30.png").convert_alpha(),
            pg.image.load("assets/images/corazones/corazones_40.png").convert_alpha(),
            pg.image.load("assets/images/corazones/corazones_50.png").convert_alpha(),
            pg.image.load("assets/images/corazones/corazones_60.png").convert_alpha(),
            pg.image.load("assets/images/corazones/corazones_70.png").convert_alpha(),
            pg.image.load("assets/images/corazones/corazones_80.png").convert_alpha(),
            pg.image.load("assets/images/corazones/corazones_90.png").convert_alpha(),
            pg.image.load("assets/images/corazones/corazones_100.png").convert_alpha()
        ]

        # Recorte sprites por sus frames
        self.frames_corriendo = self.recortar_frames(self.sprite_corriendo, 12, 64, 64)
        self.frames_ataque = self.recortar_frames(self.sprite_ataque, 7, 64, 64)
        self.frames_girando = self.recortar_frames(self.sprite_girando, 4, 64, 64)
        self.frames_dasheando = self.recortar_frames(self.sprite_dash, 8, 64, 64)

        # Frames de Sprites Corriendo
        self.frame_milisegundos_corriendo = 50

        # Frames de Sprite Atacando
        self.frame_milisegundos_ataque = 10

        # Frames de Sprites Girando
        self.frame_girando = 0
        self.frame_tiempo_girando = 0
        self.frame_milisegundos_girando = 50

        # Frames Dasheando
        self.frame_dasheando = 0
        self.tiempo_de_inicio_dash = 0
        self.frame_milisegundos_dasheando = 10

        # Saber si se encuentra dasheando o no
        self.dasheando = False
        self.ultimo_dash = 0
        self.tiempo_de_inicio_dash = 0
        self.cooldown_dash = 1000
        self.duracion_dash = 200
        self.distancia_dash = 30

        self.tiempo_de_inicio = pg.time.get_ticks()

        if len(self.frames_ataque) > 0:
            self.imagen_ataque = self.frames_ataque[0]

    def movimiento(self, teclas):
        mov_x = 0
        mov_y = 0
        tiempo_actual = pg.time.get_ticks()

        if teclas[pg.K_a]:
            mov_x = -1
            self.direccion = "IZQUIERDA"
            self.flip = True

        if teclas[pg.K_d]:
            mov_x = 1
            self.direccion = "DERECHA"
            self.flip = False

        if teclas[pg.K_w] and not self.en_el_aire:
            self.velocidad_y = self.velocidad_salto
            self.en_el_aire = True

        if teclas[pg.K_LSHIFT] and tiempo_actual - self.ultimo_dash > self.cooldown_dash:
            if not self.dasheando:
                self.dasheando = True
                self.ultimo_dash = tiempo_actual
                self.tiempo_de_inicio_dash = tiempo_actual

        if self.dasheando:
            tiempo_dash = tiempo_actual - self.tiempo_de_inicio_dash
            porcentaje_dash = min(tiempo_dash / self.distancia_dash, 1)
            distancia_recorrida = self.distancia_dash * porcentaje_dash

            if self.direccion == "DERECHA":
                self.rect.x += distancia_recorrida
            if self.direccion == "IZQUIERDA":
                self.rect.x -= distancia_recorrida

            if tiempo_dash >= self.duracion_dash:
                self.dasheando = False

        if self.en_el_aire:
            self.velocidad_y += self.gravedad

        mov_y = self.velocidad_y

        # Sonido de ataque
        if teclas[pg.K_SPACE] and tiempo_actual - self.ultimo_ataque > self.cooldown:
            if not self.en_el_aire and not self.atacando:
                self.atacando = True
                self.ultimo_ataque = tiempo_actual
                self.tiempo_de_inicio_ataque = tiempo_actual

                self.sonido_ataque.set_volume(VOLUMEN_SFX)
                self.sonido_ataque.play()

        self.rect.x += mov_x * self.velocidad
        self.rect.y += mov_y
        self.hitbox.center = self.rect.center

        if not self.dasheando:
            if self.en_el_aire:
                self.animar_giro()
            else:
                if mov_x != 0:
                    self.animar_corriendo()
                else:
                    self.imagen = self.sprite_quieto
        else:
            self.animar_dash()

        if self.direccion == "DERECHA":
            self.ataque_hitbox = pg.Rect(self.rect.centerx + 15, self.rect.centery - 48, 64, 64)
        else:
            self.ataque_hitbox = pg.Rect(self.rect.centerx - 79, self.rect.centery - 48, 64, 64)

        if self.atacando:
            self.animar_ataque()

    # Sonido de daño 
    def recibir_dano(self, cantidad):
        self.vida -= cantidad
        self.sonido_dano.set_volume(VOLUMEN_SFX)
        self.sonido_dano.play()

    def dibujar_corazones(self, ventana):
        ventana.blit(self.sprite_salud, (0, 0))
        self.sprite_salud = self.sprites_corazones[min(self.vida // 10, 10)]

    def animar_corriendo(self):
        tiempo_actual = pg.time.get_ticks()

        if tiempo_actual - self.tiempo_de_inicio > self.frame_milisegundos_corriendo:
            self.frame = (self.frame + 1) % len(self.frames_corriendo)
            self.imagen = self.frames_corriendo[self.frame]
            self.tiempo_de_inicio = tiempo_actual

    def animar_ataque(self):
        tiempo_actual = pg.time.get_ticks()

        if tiempo_actual - self.tiempo_de_inicio_ataque > self.frame_milisegundos_ataque:
            self.frame_ataque += 1
            self.tiempo_de_inicio_ataque = tiempo_actual

            if self.frame_ataque >= len(self.frames_ataque):
                self.frame_ataque = 0
                self.atacando = False
            else:
                self.imagen = self.frames_ataque[self.frame_ataque]

    def animar_giro(self):
        tiempo_actual = pg.time.get_ticks()

        if tiempo_actual - self.tiempo_de_inicio > self.frame_milisegundos_girando:
            self.frame_girando = (self.frame_girando + 1) % len(self.frames_girando)
            self.imagen = self.frames_girando[self.frame_girando]
            self.tiempo_de_inicio = tiempo_actual

    def animar_dash(self):
        tiempo_actual = pg.time.get_ticks()

        if tiempo_actual - self.tiempo_de_inicio > self.frame_milisegundos_dasheando:
            self.frame_dasheando = (self.frame_dasheando + 1) % len(self.frames_dasheando)
            self.imagen = self.frames_dasheando[self.frame_dasheando]
            self.tiempo_de_inicio = tiempo_actual
