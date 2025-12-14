import ctypes
import pygame
import sys
from settings import *

ctypes.windll.user32.SetProcessDPIAware()


# Cargar recursos
fondo_menu = pygame.transform.scale(
    pygame.image.load(RUTA_FONDO_MENU),
    (ANCHO, ALTO)
)

panel_menu = pygame.image.load(RUTA_PANEL_MENU)
panel_opciones = pygame.image.load(RUTA_PANEL_MENU)

boton_base = pygame.image.load(RUTA_BOTON)

sprite_lautaro = pygame.transform.scale(
    pygame.image.load(RUTA_SPRITE_LAUTARO),
    (900, 900)
)

logo_juego = pygame.image.load(RUTA_LOGO).convert_alpha()

pygame.mixer.init()
pygame.mixer.music.load(RUTA_MUSICA_MENU)
pygame.mixer.music.set_volume(VOLUMEN / 100)
pygame.mixer.music.play(-1)

# BOTONES
class Boton:
    def __init__(self, x, y, texto, funcion, fuente, color_texto=(255, 255, 255)):
        self.x = x
        self.y = y
        self.funcion = funcion
        self.texto = texto
        self.fuente = fuente
        self.color_texto = color_texto

        self.tamano_normal = (200, 60)
        self.tamano_zoom = (180, 60)

        self.img_base = pygame.transform.scale(boton_base, self.tamano_normal)
        self.img = self.img_base
        self.rect = self.img.get_rect(center=(self.x, self.y))

        self.hovered = False


    def dibujar(self, pantalla):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            if not self.hovered:
                self.img = pygame.transform.scale(self.img_base, self.tamano_zoom)
                self.rect = self.img.get_rect(center=(self.x, self.y))
                self.hovered = True
        else:
            if self.hovered:
                self.img = pygame.transform.scale(self.img_base, self.tamano_normal)
                self.rect = self.img.get_rect(center=(self.x, self.y))
                self.hovered = False

        pantalla.blit(self.img, self.rect)

        texto_render = self.fuente.render(
            self.texto,
            True,
            (255, 165, 0) if self.hovered else self.color_texto
        )
        texto_rect = texto_render.get_rect(center=self.rect.center)
        pantalla.blit(texto_render, texto_rect)

    def click(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(evento.pos):
                return self.funcion()


# Sliders
class Slider:
    def __init__(self, x, y, valor):
        self.x = x
        self.y = y
        self.valor = valor
        self.ancho = 300
        self.altura = 6
        self.rect = pygame.Rect(x, y, self.ancho, self.altura)

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, (200, 200, 200), self.rect)
        per = self.valor / 100
        pygame.draw.rect(pantalla, (255, 140, 0), (self.x, self.y, self.ancho * per, self.altura))
        circulo_x = self.x + int(self.ancho * per)
        pygame.draw.circle(pantalla, (255, 255, 255), (circulo_x, self.y + 3), 10)

    def mover(self):
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            if self.rect.collidepoint(mx, my) or abs(my - self.y) < 20:
                nuevo = (mx - self.x) / self.ancho
                nuevo = max(0, min(1, nuevo))
                self.valor = int(nuevo * 100)



def iniciar_juego():
    global ACCION_MENU
    ACCION_MENU = "jugar"


def abrir_opciones():
    opciones_menu()


def salir():
    pygame.quit()
    sys.exit()


fuente_botones = pygame.font.Font(None, 35)

# Controlar ubicacion de los botones
botones = [
    Boton(ANCHO * 0.15, ALTO * 0.38, "JUGAR", iniciar_juego, fuente_botones),
    Boton(ANCHO * 0.15, ALTO * 0.48, "OPCIONES", abrir_opciones, fuente_botones),
    Boton(ANCHO * 0.15, ALTO * 0.58, "SALIR", salir, fuente_botones),
]


# Menu de opciones 
def opciones_menu():
    global BRILLO, VOLUMEN

    panel = pygame.transform.scale(panel_opciones, (int(ANCHO * 0.42), int(ALTO * 0.55)))
    rect_panel = panel.get_rect(center=(ANCHO * 0.50, ALTO * 0.50))

    slider_brillo = Slider(ANCHO * 0.44, ALTO * 0.44, BRILLO)
    slider_volumen = Slider(ANCHO * 0.44, ALTO * 0.53, VOLUMEN)

    boton_volver = Boton(ANCHO * 0.50, ALTO * 0.74, "VOLVER", lambda: "volver", fuente_botones)

    reloj = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                resultado = boton_volver.click(evento)
                if resultado == "volver":
                    BRILLO = slider_brillo.valor
                    VOLUMEN = slider_volumen.valor
                    return

        slider_brillo.mover()
        slider_volumen.mover()

        pygame.mixer.music.set_volume(slider_volumen.valor / 100)

        PANTALLA.blit(fondo_menu, (0,0))
        PANTALLA.blit(panel, rect_panel)

        texto_b = fuente_botones.render("Brillo", True, (255, 255, 255))
        PANTALLA.blit(texto_b, (ANCHO * 0.32, ALTO * 0.43))


        texto_v = fuente_botones.render("Volumen", True, (255, 255, 255))
        PANTALLA.blit(texto_v, (ANCHO * 0.32, ALTO * 0.52))


        slider_brillo.dibujar(PANTALLA)
        slider_volumen.dibujar(PANTALLA)
        boton_volver.dibujar(PANTALLA)

        oscuridad = 255 - int(slider_brillo.valor * 2.55)
        if oscuridad > 0:
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(oscuridad)
            overlay.fill((0, 0, 0))
            PANTALLA.blit(overlay, (0, 0))

        pygame.display.flip()
        reloj.tick(60)



# Menu principal
def menu():
    panel_escalado = pygame.transform.scale(panel_menu, (300, 300))
    rect_panel = panel_escalado.get_rect(center=(ANCHO * 0.15, ALTO * 0.48))

    reloj = pygame.time.Clock()
    
    pygame.event.clear()
    pygame.time.delay(200)

    global ACCION_MENU
    ACCION_MENU = None

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for b in botones:
                    b.click(evento) 

        if ACCION_MENU == "jugar":
            return "jugar"

        PANTALLA.blit(fondo_menu, (0,0))

        rect_logo = logo_juego.get_rect(center=(ANCHO // 2, int(ALTO * 0.13)))
        PANTALLA.blit(logo_juego, rect_logo)

        PANTALLA.blit(panel_escalado, rect_panel)

        for b in botones:
            b.dibujar(PANTALLA)

        PANTALLA.blit(sprite_lautaro, sprite_lautaro.get_rect(center=(ANCHO * 0.65, ALTO * 0.55)))

        oscuridad = 255 - int(BRILLO * 2.55)
        if oscuridad > 0:
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(oscuridad)
            overlay.fill((0, 0, 0))
            PANTALLA.blit(overlay, (0, 0))

        pygame.display.flip()
        reloj.tick(60)
