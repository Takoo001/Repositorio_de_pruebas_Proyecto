import pygame as pg
import nivel_settings as ns

from jugador import Jugador
from enemigo import EnemigoPequeno
from suelo import Suelo


class Nivel1:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()
        self.running = True

    def iniciar(self):

        jugador = Jugador(0, ns.ALTO_NIVEL - 64 - 49)
        enemigos_pequenos = []

        largo_mapa = 6
        suelo = Suelo(largo_mapa)

        fondo_ancho = 640 * largo_mapa

        fondo_alto = self.pantalla.get_height()
        fondo = pg.Surface((fondo_ancho, fondo_alto))

        camara_x = 0

        offset_y = self.pantalla.get_height() - ns.ALTO_NIVEL


        for i in range(400, fondo_ancho, 400):
            enemigo = EnemigoPequeno(i, ns.ALTO_NIVEL - 64 - 64)
            enemigos_pequenos.append(enemigo)

        sprite_fondo = pg.image.load(
            "assets/images/fondos/ia_4.png"
        ).convert()

        sprite_fondo = pg.transform.scale(
            sprite_fondo,
            (640, fondo_alto)
        )

        for i in range(fondo_ancho // 640):
            fondo.blit(sprite_fondo, (i * 640, 0))


        while self.running:
            self.reloj.tick(60)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            teclas = pg.key.get_pressed()

            camara_x = -jugador.rect.x + 300
            camara_x = max(camara_x, -(fondo_ancho - ns.ANCHO_NIVEL))
            camara_x = min(camara_x, 0)

            jugador.rect.x = max(0, min(jugador.rect.x, fondo_ancho - 64 - 300))

            self.pantalla.fill(ns.BACKGROUND)

            self.pantalla.blit(fondo, (camara_x, 0))

            jugador.movimiento(teclas)
            jugador.dibujar(self.pantalla, camara_x, offset_y)
            jugador.dibujar_corazones(self.pantalla)

            for enemigo in enemigos_pequenos[:]:
                if enemigo.vivo:
                    enemigo.dibujar(self.pantalla, camara_x, offset_y)
                    enemigo.movimiento(jugador)

                    if jugador.atacando and not jugador.tick_ataque:
                        if jugador.ataque_hitbox.colliderect(enemigo.hitbox):
                            enemigo.vida -= jugador.dano
                            enemigo.tick_dano_recibido = True

                            if enemigo.vida <= 0:
                                enemigo.vivo = False
                                jugador.vida = min(jugador.vida + 20, 100)

                            jugador.tick_ataque = True
                else:
                    enemigo.muerto()
                    enemigos_pequenos.remove(enemigo)

            suelo.dibujar_suelo(self.pantalla, camara_x, offset_y)

            for tile in suelo.lista_suelos:
                if jugador.hitbox.colliderect(tile):
                    jugador.restablecer_posicion(ns.ALTO_NIVEL - 64 - 49)

            pg.display.flip()
