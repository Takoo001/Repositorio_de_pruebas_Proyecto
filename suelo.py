import pygame as pg
import nivel_settings as ns

class Suelo(pg.sprite.Sprite):
    def __init__(self, largo_suelos):
        super().__init__()

        self.largo_suelos = largo_suelos
        self.sprite_suelo = pg.image.load("assets/sprites_suelo/suelo_cesped_oscuro.png")
        self.lista_suelos = []

        for x in range(0, ns.ANCHO_NIVEL * largo_suelos, 64):
            self.lista_suelos.append(pg.Rect(x, ns.ALTO_NIVEL - 64, 64, 64))

    def dibujar_suelo(self, ventana, mundo_x, offset_y):
        for suelo in self.lista_suelos:
            ventana.blit(
                self.sprite_suelo,
                (suelo.x + mundo_x,
                 suelo.y + offset_y)
            )
