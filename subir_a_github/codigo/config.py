"""Constantes xerais do xogo."""
import sys

# True cando o xogo corre no navegador (versión web feita con pygbag)
WEB = sys.platform == "emscripten"

# Resolución interna 1280x720 (16:9). Escálase con suavizado á pantalla da pizarra.
ANCHO, ALTO = 1280, 720
FPS = 60

TILE = 40
HUD_ALTO = 80
COLS, FILAS = 32, 16  # o mapa do Val Verde ocupa 1280x640 baixo o marcador


class C:
    """Paleta de cores (debuxo infantil, cores vivas pero suaves)."""
    NEGRO = (30, 28, 40)
    BLANCO = (255, 255, 255)
    TEXTO = (52, 50, 66)
    TEXTO_SOMBRA = None

    CAJA = (255, 252, 244)
    CAJA_BORDE = (60, 82, 140)
    CAJA_LINEA = (190, 210, 240)

    HUD = (40, 58, 110)
    HUD_BORDE = (120, 160, 230)

    BOTON = (64, 128, 220)
    BOTON_VERDE = (56, 172, 96)
    BOTON_ROJO = (220, 84, 72)
    BOTON_GRIS = (136, 146, 166)
    BOTON_LARANXA = (240, 146, 48)
    OK = (40, 150, 72)
    ERRO = (210, 60, 52)

    GOTA = (120, 180, 255)
    AMARILLO = (255, 222, 90)
    ROJO = (232, 72, 56)
    VERDE = (72, 184, 88)
    NARANJA = (248, 152, 40)
    GRIS = (160, 160, 168)
    AGUA_CLARA = (200, 230, 255)
