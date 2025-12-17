import pygame
import sys
from settings import *

SUPERFICIE_MENU = pygame.Surface((ANCHO, ALTO))
MOUSE_POS = (0, 0)

# Sin bordes negros
def blit_estirado(superficie, pantalla):
    superficie_escalada = pygame.transform.scale(
        superficie,
        pantalla.get_size()
    )
    pantalla.blit(superficie_escalada, (0, 0))


# Mouse para la pantalla estirada
def mouse_logico_estirado():
    mx, my = pygame.mouse.get_pos()
    pw, ph = PANTALLA.get_size()
    return int(mx * ANCHO / pw), int(my * ALTO / ph)


# Crgando los recursos
fondo_menu = pygame.transform.scale(
    pygame.image.load(RUTA_FONDO_MENU),
    (ANCHO, ALTO)
)

panel_menu = pygame.image.load(RUTA_PANEL_MENU)
panel_opciones = pygame.image.load(RUTA_PANEL_MENU)

img_brillo_original = pygame.image.load(RUTA_FONDO_BRILLO).convert_alpha()
img_volumen_original = pygame.image.load(RUTA_FONDO_VOLUMEN).convert_alpha()

img_brillo = pygame.transform.scale(
    img_brillo_original,
    (
        int(img_brillo_original.get_width() * ESCALA_IMG_BRILLO),
        int(img_brillo_original.get_height() * ESCALA_IMG_BRILLO)
    )
)

img_volumen = pygame.transform.scale(
    img_volumen_original,
    (
        int(img_volumen_original.get_width() * ESCALA_IMG_VOLUMEN),
        int(img_volumen_original.get_height() * ESCALA_IMG_VOLUMEN)
    )
)


# Escala si hace falta (ajusta valores si quieres)
img_brillo = pygame.transform.scale(img_brillo, (140, 40))
img_volumen = pygame.transform.scale(img_volumen, (140, 40))


sprite_lautaro = pygame.transform.scale(
    pygame.image.load(RUTA_SPRITE_LAUTARO),
    (900, 900)
)

logo_juego = pygame.image.load(RUTA_LOGO).convert_alpha()

pygame.mixer.init()
pygame.mixer.music.load(RUTA_MUSICA_MENU)
pygame.mixer.music.set_volume(VOLUMEN / 100)
pygame.mixer.music.play(-1)

# Boton
class Boton:
    def __init__(self, x, y, ruta_img, funcion, scale=1.0):
        self.x = int(x)
        self.y = int(y)
        self.funcion = funcion
        self.scale = scale

        self.img_original = pygame.image.load(ruta_img).convert_alpha()

        w = int(self.img_original.get_width() * self.scale)
        h = int(self.img_original.get_height() * self.scale)

        self.img_normal = pygame.transform.scale(self.img_original, (w, h))
        self.img_hover = pygame.transform.scale(
            self.img_original,
            (int(w * 0.95), int(h * 0.95))
        )

        self.img = self.img_normal
        self.rect = self.img.get_rect(center=(self.x, self.y))
        self.hovered = False

    def dibujar(self, superficie):
        global MOUSE_POS

        if self.rect.collidepoint(MOUSE_POS):
            if not self.hovered:
                self.img = self.img_hover
                self.rect = self.img.get_rect(center=(self.x, self.y))
                self.hovered = True
        else:
            if self.hovered:
                self.img = self.img_normal
                self.rect = self.img.get_rect(center=(self.x, self.y))
                self.hovered = False

        superficie.blit(self.img, self.rect)

    def click(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(MOUSE_POS):
                return self.funcion()


# Sliders
class Slider:
    def __init__(self, x, y, valor):
        self.x = int(x)
        self.y = int(y)
        self.valor = valor
        self.ancho = 185
        self.altura = 6
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.altura)

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, (200, 200, 200), self.rect)

        porcentaje = self.valor / 100
        relleno_ancho = int(self.ancho * porcentaje)
        pygame.draw.rect(
            superficie,
            (255, 140, 0),
            (self.x, self.y, relleno_ancho, self.altura)
        )

        cx = self.x + relleno_ancho
        cy = self.y + self.altura // 2
        pygame.draw.circle(superficie, (255, 255, 255), (cx, cy), 10)

    def mover(self):
        global MOUSE_POS
        if pygame.mouse.get_pressed()[0]:
            mx, my = MOUSE_POS

            # Margen vertical
            if self.x - 10 <= mx <= self.x + self.ancho + 10 and abs(my - self.y) < 20:
                nuevo = (mx - self.x) / self.ancho
                nuevo = max(0, min(1, nuevo))
                self.valor = int(nuevo * 100)

# Funciones
def iniciar_juego():
    global ACCION_MENU
    ACCION_MENU = "jugar"


def abrir_opciones():
    opciones_menu()


def salir():
    pygame.quit()
    sys.exit()


fuente_botones = pygame.font.Font(None, 35)

botones = [
    Boton(
        ANCHO * 0.15,
        ALTO * 0.38,
        RUTA_BOTON_JUGAR,
        iniciar_juego,
        scale=0.55
    ),
    Boton(
        ANCHO * 0.15,
        ALTO * 0.48,
        RUTA_BOTON_OPCIONES,
        abrir_opciones,
        scale=0.55
    ),
    Boton(
        ANCHO * 0.15,
        ALTO * 0.58,
        RUTA_BOTON_SALIR,
        salir,
        scale=0.55
    ),
]


# Opciones
def opciones_menu():
    global BRILLO, VOLUMEN, MOUSE_POS

    panel = pygame.transform.scale(
        panel_opciones,
        (int(ANCHO * 0.42), int(ALTO * 0.55))
    )
    rect_panel = panel.get_rect(center=(ANCHO * 0.50, ALTO * 0.50))

    slider_brillo = Slider(ANCHO * 0.49, ALTO * 0.44, BRILLO)
    slider_volumen = Slider(ANCHO * 0.49, ALTO * 0.53, VOLUMEN)

    boton_volver = Boton(
    ANCHO * 0.50,
    ALTO * 0.74,
    RUTA_BOTON_VOLVER,
    lambda: "volver",
    scale=0.75
    )


    reloj = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if boton_volver.click(evento) == "volver":
                    BRILLO = slider_brillo.valor
                    VOLUMEN = slider_volumen.valor
                    return

        # Movimiento sliders
        slider_brillo.mover()
        slider_volumen.mover()
        pygame.mixer.music.set_volume(slider_volumen.valor / 100)

        # Dibujado
        SUPERFICIE_MENU.blit(fondo_menu, (0, 0))
        SUPERFICIE_MENU.blit(panel, rect_panel)

        # Imagen brillo
        SUPERFICIE_MENU.blit(
            img_brillo,
            img_brillo.get_rect(
            midright=(ANCHO * 0.48, ALTO * 0.44)
        )
    )

        # Imagen volumen
        SUPERFICIE_MENU.blit(
        img_volumen,
        img_volumen.get_rect(
        midright=(ANCHO * 0.48, ALTO * 0.53)
        )
    )

        # Sliders
        slider_brillo.dibujar(SUPERFICIE_MENU)
        slider_volumen.dibujar(SUPERFICIE_MENU)

        # Boton volver
        boton_volver.dibujar(SUPERFICIE_MENU)

        # Brillo pantalla
        oscuridad = 255 - int(slider_brillo.valor * 2.55)
        if oscuridad > 0:
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(oscuridad)
            overlay.fill((0, 0, 0))
            SUPERFICIE_MENU.blit(overlay, (0, 0))

        # Render final
        blit_estirado(SUPERFICIE_MENU, PANTALLA)
        MOUSE_POS = mouse_logico_estirado()

        pygame.display.flip()
        reloj.tick(60)



# Menu
def menu():
    global ACCION_MENU, MOUSE_POS
    ACCION_MENU = None

    panel_escalado = pygame.transform.scale(panel_menu, (300, 300))
    rect_panel = panel_escalado.get_rect(center=(ANCHO * 0.15, ALTO * 0.48))

    logo_menu = pygame.transform.scale(
        logo_juego,
        (
            int(logo_juego.get_width() * ESCALA_LOGO_FINAL),
            int(logo_juego.get_height() * ESCALA_LOGO_FINAL)
        )
    )
    rect_logo_menu = logo_menu.get_rect(
        center=(ANCHO // 2, int(ALTO * 0.13))
    )

    reloj = pygame.time.Clock()
    pygame.event.clear()
    pygame.time.delay(200)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for b in botones:
                    b.click(evento)

        if ACCION_MENU == "jugar":
            return "jugar"

        SUPERFICIE_MENU.blit(fondo_menu, (0, 0))

        # Logo
        SUPERFICIE_MENU.blit(logo_menu, rect_logo_menu)

        # Panel
        SUPERFICIE_MENU.blit(panel_escalado, rect_panel)

        # Botones
        for b in botones:
            b.dibujar(SUPERFICIE_MENU)

        # Sprite decorativo
        SUPERFICIE_MENU.blit(
            sprite_lautaro,
            sprite_lautaro.get_rect(center=(ANCHO * 0.65, ALTO * 0.55))
        )

        # Brillo
        oscuridad = 255 - int(BRILLO * 2.55)
        if oscuridad > 0:
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(oscuridad)
            overlay.fill((0, 0, 0))
            SUPERFICIE_MENU.blit(overlay, (0, 0))

        blit_estirado(SUPERFICIE_MENU, PANTALLA)
        MOUSE_POS = mouse_logico_estirado()

        pygame.display.flip()
        reloj.tick(60)