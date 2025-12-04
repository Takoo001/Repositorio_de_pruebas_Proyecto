import pygame
import ctypes
import os

# Para evitar problemas con el escalado
ctypes.windll.user32.SetProcessDPIAware()

pygame.init()

# Centrando la ventana
os.environ["SDL_VIDEO_CENTERED"] = "1"

# Resolucion base 
ANCHO_BASE = 1280
ALTO_BASE = 720

# Ventana en pantalla completa escalada
PANTALLA = pygame.display.set_mode(
    (ANCHO_BASE, ALTO_BASE),
    pygame.FULLSCREEN | pygame.SCALED
)

# Ajustando pantalla a la que tenga el usuario
info = pygame.display.Info()
ANCHO = info.current_w
ALTO = info.current_h

# Colores
BLANCO = (255, 255, 255)
NARANJO = (255, 140, 0)

# Colores globales
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

# Reloj global
RELOJ = pygame.time.Clock()
