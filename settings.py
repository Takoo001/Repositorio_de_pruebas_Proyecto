import pygame
import os

pygame.init()

# --------------------------------------------------
# VENTANA
# --------------------------------------------------

os.environ["SDL_VIDEO_CENTERED"] = "1"

ANCHO_BASE = 1280
ALTO_BASE = 720

PANTALLA = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

ANCHO = ANCHO_BASE
ALTO = ALTO_BASE

# --------------------------------------------------
# COLORES
# --------------------------------------------------

BLANCO = (255, 255, 255)
NARANJO = (255, 140, 0)

# --------------------------------------------------
# VALORES GLOBALES
# --------------------------------------------------

BRILLO = 100
VOLUMEN = 40

# --------------------------------------------------
# LOGO (carga + menú)
# --------------------------------------------------

ESCALA_LOGO_INICIAL = 0.1
ESCALA_LOGO_FINAL = 0.6
VELOCIDAD_ESCALA_LOGO = 0.01

# --------------------------------------------------
# RUTAS BASE
# --------------------------------------------------

RUTA_ASSETS = "assets"
RUTA_IMAGES = os.path.join(RUTA_ASSETS, "images")
RUTA_MUSICA = os.path.join(RUTA_ASSETS, "musica")

# --------------------------------------------------
# RUTAS IMÁGENES
# --------------------------------------------------

# Logo
RUTA_LOGO = os.path.join(RUTA_IMAGES, "logo", "logo_juego.png")

# Fondos
RUTA_FONDO_MENU = os.path.join(RUTA_IMAGES, "fondos", "fondo_bosque.png")
RUTA_PANEL_MENU = os.path.join(RUTA_IMAGES, "fondos", "fondo_menu.png")
RUTA_FONDO_CARGA = os.path.join(RUTA_IMAGES, "fondos", "fondo_carga.png")
RUTA_FONDO_BRILLO = os.path.join(RUTA_IMAGES, "fondos", "fondo_brillo.png")
RUTA_FONDO_VOLUMEN = os.path.join(RUTA_IMAGES, "fondos", "fondo_volumen.png")
RUTA_FONDO_CARGANDO = os.path.join(RUTA_IMAGES, "fondos", "fondo_cargando.png")


# Imagenes de opciones menu
ESCALA_IMG_BRILLO = 0.3
ESCALA_IMG_VOLUMEN = 0.3


# Personajes
RUTA_SPRITE_LAUTARO = os.path.join(RUTA_IMAGES, "personajes", "pj.png")
RUTA_LAUTARO_BASE = os.path.join(RUTA_IMAGES, "personajes", "lautaro_base.png")
RUTA_LAUTARO_CORRIENDO = os.path.join(RUTA_IMAGES, "personajes", "lautaro_corriendo.png")

# Entorno
RUTA_SUELO = os.path.join(RUTA_IMAGES, "entorno", "suelo_cesped.png")

# Botones
RUTA_BOTON_JUGAR = os.path.join(RUTA_IMAGES, "botones", "boton_jugar.png")
RUTA_BOTON_OPCIONES = os.path.join(RUTA_IMAGES, "botones", "boton_opciones.png")
RUTA_BOTON_SALIR = os.path.join(RUTA_IMAGES, "botones", "boton_salir.png")
RUTA_BOTON_VOLVER = os.path.join(RUTA_IMAGES, "botones", "boton_volver.png")

# --------------------------------------------------
# MÚSICA
# --------------------------------------------------

RUTA_MUSICA_MENU = os.path.join(RUTA_MUSICA, "musica_menu.ogg")

# --------------------------------------------------
# FUENTES
# --------------------------------------------------

pygame.font.init()
FUENTE_GENERAL = pygame.font.Font(None, 60)
FUENTE_TITULO = pygame.font.Font(None, 120)

# --------------------------------------------------
# RELOJ GLOBAL
# --------------------------------------------------

RELOJ = pygame.time.Clock()
