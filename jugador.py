import pygame as pg
import nivel_settings as ns

class Jugador(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Estadisticas del personake
        self.estadisticas = {
            "Vida": 100,
            "Daño": 20
        }

        self.velocidad = 3
        self.velocidad_y = 0
        self.gravedad = 1
        self.contacto_suelo = False

        # Sprites principales
        self.flip = False
        self.quieto = pg.image.load("assets/images/personajes/Lautaro_base64.png").convert_alpha()
        self.corriendo = pg.image.load("assets/images/personajes/lautaro_corriendo.png").convert_alpha()

        # Dimensiones reales del sprite
        self.ancho = self.quieto.get_width()
        self.altura = self.quieto.get_height()

        # Sprite 
        self.imagen = self.quieto
        
        # Posición y hitbox
        self.rect = pg.Rect(x, y, self.ancho, self.altura)
        self.hitbox = pg.Rect(self.rect.x, self.rect.y, self.ancho * 0.6, self.altura * 0.7)
        self.hitbox.center = self.rect.center
        
        # Animacion
        self.frame = 0
        self.frames_corriendo = []
        self.frame_milisegundos = 50
        self.tiempo_de_inicio = pg.time.get_ticks()

        # Cortar los frames para animar correr
        for i in range(12):
            frame = self.corriendo.subsurface(i * 64, 0, 64, 64)
            self.frames_corriendo.append(frame)

    def dibujar(self, ventana):
        imagen_flip = pg.transform.flip(self.imagen, self.flip, False)
        ventana.blit(imagen_flip, self.rect.topleft)

    def movimiento(self, teclas):

        # Movimiento horizontal
        mov_x = 0
        if teclas[pg.K_a]:
            mov_x = -1
            self.flip = True
        if teclas[pg.K_d]:
            mov_x = 1
            self.flip = False

        # Salto
        if teclas[pg.K_SPACE] and self.contacto_suelo:
            self.velocidad_y = -15
            self.contacto_suelo = False

        # Movimiento horizontal
        self.rect.x += mov_x * self.velocidad

        # Gravedad
        if not self.contacto_suelo:
            self.velocidad_y += self.gravedad
            if self.velocidad_y > 20:
                self.velocidad_y = 20

        # Movimiento vertical
        self.rect.y += int(self.velocidad_y)

        # Hitbox
        self.hitbox.center = self.rect.center

        # Animacion
        if mov_x != 0:
            self.animar_caminando()
        else:
            if self.contacto_suelo:
                self.imagen = self.quieto
    
    def animar_caminando(self):
        tiempo_actual = pg.time.get_ticks()
        
        if tiempo_actual - self.tiempo_de_inicio > self.frame_milisegundos:
            self.frame = (self.frame + 1) % len(self.frames_corriendo)
            self.imagen = self.frames_corriendo[self.frame]
            self.tiempo_de_inicio = tiempo_actual

    def obtener_posicion(self):
        return (self.hitbox.x, self.hitbox.y)
    
    def restablecer_posicion(self, y):
        self.rect.y = y
        self.hitbox.center = self.rect.center
        self.velocidad_y = 0
