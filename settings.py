import pygame
import os

pygame.init()

# Centrando la ventana
os.environ["SDL_VIDEO_CENTERED"] = "1"

# Resolucion base 
ANCHO_BASE = 1280
ALTO_BASE = 720

# Ventana fullscreen 
PANTALLA = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Resolucion "logica"
ANCHO = ANCHO_BASE
ALTO = ALTO_BASE

# Colores
BLANCO = (255, 255, 255)
NARANJO = (255, 140, 0)

# Valores globales
BRILLO = 100
VOLUMEN = 40

# Rutas
RUTA_LOGO = "assets/images/logo_juego.png"
RUTA_PJ_CAMINANDO = "assets/images/pj_caminando.png"
RUTA_FONDO_MENU = "assets/images/fondo_bosque.png"
RUTA_PANEL_MENU = "assets/images/fondo_menu.png"
RUTA_BOTON = "assets/images/boton_fondo.png"
RUTA_SPRITE_LAUTARO = "assets/images/pj.png"
RUTA_MUSICA_MENU = "assets/musica/musica_menu.ogg"

# Fuentes
pygame.font.init()
FUENTE_GENERAL = pygame.font.Font(None, 60)
FUENTE_TITULO = pygame.font.Font(None, 120)

# Reloj
RELOJ = pygame.time.Clock()


# Escalado, centrado y el input
def blit_escalado(surface_origen, ventana):
    vw, vh = ventana.get_size()
    sw, sh = surface_origen.get_size()

    escala = min(vw / sw, vh / sh)
    nuevo_w = int(sw * escala)
    nuevo_h = int(sh * escala)

    surface_escalada = pygame.transform.scale(surface_origen, (nuevo_w, nuevo_h))

    offset_x = (vw - nuevo_w) // 2
    offset_y = (vh - nuevo_h) // 2

    ventana.fill((0, 0, 0))
    ventana.blit(surface_escalada, (offset_x, offset_y))

    return escala, offset_x, offset_y


def mouse_logico(pos_mouse, escala, ox, oy):
    mx, my = pos_mouse
    mx = (mx - ox) / escala
    my = (my - oy) / escala
    return int(mx), int(my)
