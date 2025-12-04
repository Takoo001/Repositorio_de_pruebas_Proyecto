import pygame as pg
import nivel_settings as ns

from jugador import Jugador
from suelo import Suelo


class Nivel1:
    def iniciar(self):
        pg.init()

        # Pantalla completa 
        ventana = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        pg.display.set_caption("Nivel1")

        ANCHO_REAL, ALTO_REAL = ventana.get_size()

        # Superficie interna
        surface_juego = pg.Surface((ns.ANCHO_NIVEL, ns.ALTO_NIVEL))

        # Cargar al pj
        jugador = Jugador(100, 0)

        # Posicion inicial sobre el suelo
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

            # Logica de la superficie (Pasto)
            surface_juego.fill(ns.BACKGROUND)

            teclas = pg.key.get_pressed()
            jugador.movimiento(teclas)

            jugador.contacto_suelo = False

            teclas = pg.key.get_pressed()
            jugador.movimiento(teclas)

            for bloque in suelo.lista_suelos:
                if jugador.hitbox.colliderect(bloque):

                    jugador.rect.bottom = bloque.top + 15
                    jugador.hitbox.center = jugador.rect.center
                    jugador.velocidad_y = 0
                    jugador.contacto_suelo = True
                    break


            jugador.dibujar(surface_juego)

            # Dibujar piso
            suelo.dibujar_suelo(surface_juego)

            # Escalar a tamaño pantalla completa (Real) segun la pantalla
            juego_escalado = pg.transform.scale(surface_juego, (ANCHO_REAL, ALTO_REAL))
            ventana.blit(juego_escalado, (0, 0))

            pg.display.update()

        pg.quit()
