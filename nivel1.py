import pygame as pg
import nivel_settings as ns
import time
from menu import opciones_pausa  

from jugador import Jugador
from enemigo import EnemigoPequeno
from suelo import Suelo


class Nivel1:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()
        self.running = True

        # estado game over
        self.game_over = False
        self.tiempo_game_over = 0
        self.escala_game_over = 0.2

        # imagen game over
        self.game_over_img = pg.image.load(
            "assets/images/fondos/game_over.png"
        ).convert_alpha()

    def iniciar(self):

        jugador = Jugador(0, ns.ALTO_NIVEL - 64 - 49)
        enemigos_pequenos = []

        largo_mapa = 20
        suelo = Suelo(largo_mapa)

        fondo_ancho = 640 * largo_mapa
        fondo_alto = self.pantalla.get_height()
        fondo = pg.Surface((fondo_ancho, fondo_alto))

        camara_x = 0
        offset_y = self.pantalla.get_height() - ns.ALTO_NIVEL

        for i in range(400, fondo_ancho, 800):
            enemigos_pequenos.append(
                EnemigoPequeno(i, ns.ALTO_NIVEL - 64 - 64)
            )

        sprite_fondo = pg.image.load(
            "assets/sprites_fondo/fondo_bosque_2.png"
        ).convert()

        sprite_fondo = pg.transform.scale(
            sprite_fondo,
            (640, fondo_alto)
        )

        for i in range(fondo_ancho // 640):
            fondo.blit(sprite_fondo, (i * 640, 0))

        # loop principal
        while self.running:
            self.reloj.tick(60)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    return

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        fondo_congelado = self.pantalla.copy() # 👈 SOLO ABRE OPCIONES
                        accion = opciones_pausa(fondo_congelado, self.reloj)
                        
                        if accion == "salir":
                            self.running = False
                            return
                        
            if self.game_over:
                self.animar_game_over()
                continue

            teclas = pg.key.get_pressed()

            camara_x = -jugador.rect.x + 600
            camara_x = max(camara_x, -(fondo_ancho - ns.ANCHO_NIVEL))
            camara_x = min(camara_x, 0)

            jugador.rect.x = max(
                0, min(jugador.rect.x, fondo_ancho - 64 - 1280)
            )

            self.pantalla.fill(ns.BACKGROUND)
            self.pantalla.blit(fondo, (camara_x, 0))

            jugador.movimiento(teclas)
            jugador.dibujar(self.pantalla, camara_x, offset_y)
            jugador.dibujar_corazones(self.pantalla)

            # enemigos
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
                    jugador.restablecer_posicion(
                        ns.ALTO_NIVEL - 64 - 49
                    )

            if jugador.vida <= 0:
                self.game_over = True
                self.tiempo_game_over = pg.time.get_ticks()
                self.escala_game_over = 0.2

            pg.display.flip()

        pg.quit()

    def animar_game_over(self):
        tiempo_actual = pg.time.get_ticks()

        self.pantalla.fill((0, 0, 0))

        if self.escala_game_over < 1.0:
            self.escala_game_over += 0.02

        w = int(self.game_over_img.get_width() * self.escala_game_over)
        h = int(self.game_over_img.get_height() * self.escala_game_over)

        img = pg.transform.scale(self.game_over_img, (w, h))
        rect = img.get_rect(
            center=(
                self.pantalla.get_width() // 2,
                self.pantalla.get_height() // 2
            )
        )

        self.pantalla.blit(img, rect)
        pg.display.flip()

        if tiempo_actual - self.tiempo_game_over > 3000:
            self.running = False
