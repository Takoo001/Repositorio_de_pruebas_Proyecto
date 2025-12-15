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
pj_caminando = pygame.image.load(RUTA_PJ_CAMINANDO).convert_alpha()

fuente_carga = pygame.font.Font(None, 70)


def blit_estirado(superficie, pantalla):
    superficie_escalada = pygame.transform.scale(
        superficie,
        pantalla.get_size()
    )
    pantalla.blit(superficie_escalada, (0, 0))


def animacion_inicio():
    escala = 0.1
    escala_final = 1.0

    # Ubicacion "logica" de logo
    x_logo = ANCHO // 2
    y_logo = ALTO // 2
    y_logo_final = ALTO * 0.16

    puntos = 0
    tiempo_puntos = 0

    while escala < escala_final or y_logo > y_logo_final:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SUPERFICIE_CARGA.fill((0, 0, 0))

        if escala < escala_final:
            escala += 0.02

        logo_escalado = pygame.transform.scale(
            logo,
            (int(logo.get_width() * escala), int(logo.get_height() * escala))
        )
        rect_logo = logo_escalado.get_rect(center=(x_logo, y_logo))
        SUPERFICIE_CARGA.blit(logo_escalado, rect_logo)

        if escala >= escala_final and y_logo > y_logo_final:
            y_logo -= 10

        tiempo_puntos += 1
        if tiempo_puntos > 30:
            puntos = (puntos + 1) % 4
            tiempo_puntos = 0

        texto = "Cargando" + "." * puntos
        render_carga = fuente_carga.render(texto, True, BLANCO)
        SUPERFICIE_CARGA.blit(render_carga, (ANCHO * 0.70, ALTO * 0.85))

        pj_escalado = pygame.transform.scale(pj_caminando, (120, 120))
        SUPERFICIE_CARGA.blit(pj_escalado, (ANCHO * 0.15, ALTO * 0.78))

        # Estirando la pantalla
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
