import pygame as pg
import nivel_settings as ns

class Suelo(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Cargar sprite del suelo
        self.sprite_suelo = pg.image.load("assets/images/suelo_cesped.png").convert_alpha()

        self.lista_suelos = []

        # Crear suelo usando ALTO_SUELO del settings
        for x in range(0, ns.ANCHO_NIVEL, 64):
            self.lista_suelos.append(
                pg.Rect(x, ns.ALTO_NIVEL - ns.ALTO_SUELO, 64, ns.ALTO_SUELO)
            )

    def dibujar_suelo(self, ventana):
        for suelo in self.lista_suelos:
            ventana.blit(self.sprite_suelo, suelo.topleft)
