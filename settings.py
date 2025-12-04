import pygame

pygame.init()

# Ajustes de pantalla
pantalla_info = pygame.display.Info()
ANCHO = pantalla_info.current_w
ALTO = pantalla_info.current_h

# Usamos SCALED para que se vea bien en todo tipo de pantallas
PANTALLA = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN | pygame.SCALED)

# Colores
BLANCO = (255, 255, 255)
NARANJO = (255, 140, 0)

# La configuracion global
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

# REloj global
RELOJ = pygame.time.Clock()

