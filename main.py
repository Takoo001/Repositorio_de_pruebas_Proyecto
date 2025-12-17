import pygame
import sys
import time
import os

from settings import *
from menu import menu
from nivel1 import Nivel1

SUPERFICIE_CARGA = pygame.Surface((ANCHO, ALTO))

logo = pygame.image.load(RUTA_LOGO).convert_alpha()

fondo_carga = pygame.image.load(RUTA_FONDO_CARGA).convert()
fondo_carga = pygame.transform.scale(fondo_carga, (ANCHO, ALTO))


sprite_cargando = pygame.image.load(RUTA_FONDO_CARGANDO).convert_alpha()

CARGANDO_FRAMES = 4
indice_frame = 0
contador_frame = 0
VEL_ANIM_CARGA = 12  

ancho_frame = sprite_cargando.get_width() // CARGANDO_FRAMES
alto_frame = sprite_cargando.get_height()

frames_cargando = []
for i in range(CARGANDO_FRAMES):
    frame = sprite_cargando.subsurface(
        pygame.Rect(i * ancho_frame, 0, ancho_frame, alto_frame)
    )
    frames_cargando.append(frame)


def blit_estirado(superficie, pantalla):
    superficie_escalada = pygame.transform.scale(superficie, pantalla.get_size())
    pantalla.blit(superficie_escalada, (0, 0))


def animacion_inicio():
    global indice_frame, contador_frame

    escala = ESCALA_LOGO_INICIAL
    x_logo = ANCHO // 2
    y_logo = ALTO // 2
    y_logo_final = int(ALTO * 0.16)

    while escala < ESCALA_LOGO_FINAL or y_logo > y_logo_final:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SUPERFICIE_CARGA.blit(fondo_carga, (0, 0))

        # Escalado logo
        if escala < ESCALA_LOGO_FINAL:
            escala += VELOCIDAD_ESCALA_LOGO

        logo_escalado = pygame.transform.scale(
            logo,
            (
                int(logo.get_width() * escala),
                int(logo.get_height() * escala)
            )
        )
        rect_logo = logo_escalado.get_rect(center=(x_logo, y_logo))
        SUPERFICIE_CARGA.blit(logo_escalado, rect_logo)

        if escala >= ESCALA_LOGO_FINAL and y_logo > y_logo_final:
            y_logo -= 10

        # Animacion de lcargando
        contador_frame += 1
        if contador_frame >= VEL_ANIM_CARGA:
            contador_frame = 0
            indice_frame = (indice_frame + 1) % CARGANDO_FRAMES

        frame = frames_cargando[indice_frame]
        rect = frame.get_rect(center=(ANCHO // 2, int(ALTO * 0.85)))
        SUPERFICIE_CARGA.blit(frame, rect)

        blit_estirado(SUPERFICIE_CARGA, PANTALLA)
        pygame.display.flip()
        RELOJ.tick(60)

    time.sleep(0.8)


# Ejecucion
if __name__ == "__main__":
    animacion_inicio()
    pygame.event.clear()

    accion = menu()

    if accion == "jugar":
        pygame.mixer.music.stop()
        nivel = Nivel1(PANTALLA)
        nivel.iniciar()
