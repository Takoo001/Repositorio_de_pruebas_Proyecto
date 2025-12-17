import pygame
import sys
import time

from settings import *
from menu import menu
from nivel1 import Nivel1

# Carga
SUPERFICIE_CARGA = pygame.Surface((ANCHO, ALTO))

# Cargar imagenes
logo = pygame.image.load(RUTA_LOGO).convert_alpha()


fondo_carga = pygame.image.load(RUTA_FONDO_CARGA).convert()
fondo_carga = pygame.transform.scale(fondo_carga, (ANCHO, ALTO))

# Sprite animado cargando
cargando_sprite = pygame.image.load(RUTA_FONDO_CARGANDO).convert_alpha()

CARGANDO_FRAMES = 4
frame_actual = 0
contador_anim = 0
VELOCIDAD_ANIM = 10

ancho_frame = cargando_sprite.get_width() // CARGANDO_FRAMES
alto_frame = cargando_sprite.get_height()

frames_cargando = []
for i in range(CARGANDO_FRAMES):
    frame = cargando_sprite.subsurface(
        pygame.Rect(i * ancho_frame, 0, ancho_frame, alto_frame)
    )
    frames_cargando.append(frame)
fuente_carga = pygame.font.Font(None, 70)


def blit_estirado(superficie, pantalla):
    superficie_escalada = pygame.transform.scale(
        superficie,
        pantalla.get_size()
    )
    pantalla.blit(superficie_escalada, (0, 0))

def animacion_inicio():
    global frame_actual, contador_anim

    escala = ESCALA_LOGO_INICIAL

    x_logo = ANCHO // 2
    y_logo = ALTO // 2
    y_logo_final = ALTO * 0.16

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

        # --- Animación cargando ---
        contador_anim += 1
        if contador_anim >= VELOCIDAD_ANIM:
            contador_anim = 0
            frame_actual = (frame_actual + 1) % CARGANDO_FRAMES

        frame = frames_cargando[frame_actual]
        rect_cargando = frame.get_rect(
            center=(ANCHO // 2, int(ALTO * 0.85))
        )
        SUPERFICIE_CARGA.blit(frame, rect_cargando)

        blit_estirado(SUPERFICIE_CARGA, PANTALLA)
        pygame.display.flip()
        RELOJ.tick(60)

    time.sleep(0.8)



if __name__ == "__main__":
    animacion_inicio()
    pygame.event.clear()

    accion = menu()

    if accion == "jugar":
        pygame.mixer.music.stop()

        nivel = Nivel1()
        nivel.iniciar()