import pygame as pg
import nivel_settings as ns
from settings import PANTALLA
from jugador import Jugador
from suelo import Suelo


def blit_estirado(superficie, pantalla):
    superficie_escalada = pg.transform.scale(
        superficie,
        pantalla.get_size()
    )
    pantalla.blit(superficie_escalada, (0, 0))


class Nivel1:
    def iniciar(self):
        pg.init()

        ventana = PANTALLA

        # Superficie del nivel 
        surface_juego = pg.Surface((ns.ANCHO_NIVEL, ns.ALTO_NIVEL))

        # Cargar jugador
        jugador = Jugador(100, 0)

        # Posicion inicial
        jugador.rect.bottom = ns.ALTO_NIVEL - ns.ALTO_SUELO
        jugador.hitbox.center = jugador.rect.center
        jugador.contacto_suelo = True
        jugador.velocidad_y = 0

        suelo = Suelo()
        reloj = pg.time.Clock()

        running = True
        while running:
            reloj.tick(60)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False

            # Fondo del nivel
            surface_juego.fill(ns.BACKGROUND)

            teclas = pg.key.get_pressed()
            jugador.movimiento(teclas)

            jugador.contacto_suelo = False

            for bloque in suelo.lista_suelos:
                if jugador.hitbox.colliderect(bloque):
                    jugador.rect.bottom = bloque.top + 15
                    jugador.hitbox.center = jugador.rect.center
                    jugador.velocidad_y = 0
                    jugador.contacto_suelo = True
                    break

            jugador.dibujar(surface_juego)
            suelo.dibujar_suelo(surface_juego)

            blit_estirado(surface_juego, ventana)

            pg.display.flip()

        pg.quit()
