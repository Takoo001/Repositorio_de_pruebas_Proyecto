import pygame as pg

class Entidad(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        self.vida = 100
        self.dano = 20
        self.velocidad = 5
        self.vivo = True

        self.tick_dano_recibido = False

        self.velocidad_y = 0
        self.gravedad = 0.5
        self.velocidad_salto = -15
        self.en_el_aire = True

        self.atacando = False
        self.tick_ataque = False
        self.direccion = "DERECHA"

        self.cooldown = 500
        self.ultimo_ataque = 0

        self.flip = False
        self.sprite_quieto = pg.image.load("assets/images/personajes/lautaro_quieto.png").convert_alpha()
        self.sprite_corriendo = pg.image.load("assets/images/personajes/lautaro_corriendo.png").convert_alpha()
        self.imagen = self.sprite_quieto
        self.sprite_ataque = pg.image.load("assets/images/personajes/ataque_prueba.png").convert_alpha()
        self.imagen_ataque = pg.image.load("assets/images/personajes/ataque_prueba.png").convert_alpha()

        self.frames_corriendo = self.recortar_frames(self.sprite_corriendo, 12, 64, 64)
        self.frames_ataque = self.recortar_frames(self.sprite_ataque, 7, 64, 64)

        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x, self.y, 64, 64)
        self.hitbox = pg.Rect(self.x, self.y, 25, 35)
        self.ataque_hitbox = pg.Rect(self.rect.centerx + 15, self.rect.centery - 48, 64, 64)

        self.frame_corriendo = 0
        self.frame_milisegundos_corriendo = 100

        self.frame_ataque = 0
        self.frame_milisegundos_ataque = 10

        self.tiempo_de_inicio = pg.time.get_ticks()

    def recortar_frames(self, sprite, numero_frames, ancho, alto):
        frames = []
        for i in range(numero_frames):
            frame = sprite.subsurface(i * ancho, 0, ancho, alto)
            frames.append(frame)
        return frames

    def movimiento(self):
        pass

    def animar_corriendo(self):
        tiempo_actual = pg.time.get_ticks()
        if tiempo_actual - self.tiempo_de_inicio > self.frame_milisegundos_corriendo:
            self.frame_corriendo = (self.frame_corriendo + 1) % len(self.frames_corriendo)
            self.imagen = self.frames_corriendo[self.frame_corriendo]
            self.tiempo_de_inicio = tiempo_actual

    def animar_ataque(self):
        tiempo_actual = pg.time.get_ticks()
        if tiempo_actual - self.tiempo_de_inicio > self.frame_milisegundos_ataque:
            self.frame_ataque += 1
            if self.frame_ataque >= len(self.frames_ataque):
                self.atacando = False
                self.frame_ataque = 0
                self.tick_ataque = False
            if self.frame_ataque < len(self.frames_ataque):
                self.imagen_ataque = self.frames_ataque[self.frame_ataque]
            self.tiempo_de_inicio = tiempo_actual

    def dibujar(self, ventana, mundo_x, offset_y=0):
        if self.atacando:
            ataque = pg.transform.flip(self.imagen_ataque, self.flip, False)
            ventana.blit(
                ataque,
                (self.ataque_hitbox.x + mundo_x,
                 self.ataque_hitbox.y + offset_y)
            )

        imagen = pg.transform.flip(self.imagen, self.flip, False)
        ventana.blit(
            imagen,
            (self.rect.x + mundo_x,
             self.rect.y + offset_y)
        )

    def muerto(self):
        self.hitbox = pg.Rect(0, 0, 0, 0)
        self.rect = pg.Rect(0, 0, 0, 0)
        self.ataque_hitbox = pg.Rect(0, 0, 0, 0)

    def restablecer_posicion(self, y):
        self.rect.y = y
        self.hitbox.center = self.rect.center
        self.velocidad_y = 0
        self.en_el_aire = False
