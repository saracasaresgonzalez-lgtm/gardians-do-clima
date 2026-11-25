"""GARDIÁNS DO CLIMA — videoxogo educativo para 4º de Primaria (pizarra dixital táctil).

No ordenador:        python main.py          (en xanela: python main.py --xanela)
No navegador:        pygbag --build videojuego   (crea a versión web en build/web)
Requisitos:          pip install pygame-ce
"""
import asyncio
import os
import sys

# Escalado suavizado da imaxe á resolución da pantalla (debuxos sen píxeles)
os.environ.setdefault("SDL_RENDER_SCALE_QUALITY", "1")

import pygame  # noqa: E402

import arte  # noqa: E402
import datos  # noqa: E402
import escenas  # noqa: E402
import sonido  # noqa: E402
import texto  # noqa: E402
import ui  # noqa: E402
from config import ANCHO, ALTO, FPS, WEB  # noqa: E402
from entrada import Entrada  # noqa: E402
from pincel import fonte  # noqa: E402
from preguntas import Banco  # noqa: E402


class Juego:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.entrada = Entrada()
        self.arte = arte.Arte()
        self.fuentes = texto.Fuentes()
        self.sonidos = sonido.Sonidos()
        self.bancos = {k: Banco(v) for k, v in datos.POOLS.items()}
        self.partida = {}          # misión -> {"estrelas", "puntos"}
        self.activo = True
        self.escena = None
        escenas.ir_titulo(self)

    def ir_inicio(self):
        escenas.ir_titulo(self)

    def cambiar(self, escena):
        self.escena = escena

    def paso(self, dt, eventos):
        for e in eventos:
            if e.type == pygame.QUIT:
                self.activo = False
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_F11:
                ui.pantalla_completa()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE and not isinstance(self.escena, escenas.EscenaTitulo):
                escenas.ir_titulo(self)
                return
        self.entrada.procesar(eventos)
        self.escena.update(dt)
        self.escena.draw(self.pantalla)


def axustar_lenzo():
    """No navegador, pide á páxina que recalcule o tamaño do xogo (mantendo 16:9)."""
    if WEB:
        try:
            import platform
            platform.window.eval("window.dispatchEvent(new Event('resize'))")
        except Exception:
            pass


def pantalla_carga(pantalla):
    pantalla.fill((40, 58, 110))
    img = fonte(48).render("Cargando...", True, (255, 255, 255))
    pantalla.blit(img, (ANCHO // 2 - img.get_width() // 2, ALTO // 2 - img.get_height() // 2))
    pygame.display.flip()


async def main():
    pygame.mixer.pre_init(22050, -16, 1, 512)
    pygame.init()
    if WEB:
        opcions = 0   # no navegador a páxina xa escala a imaxe (con SCALED os toques chegan mal)
    else:
        opcions = pygame.SCALED
        if "--xanela" not in sys.argv:
            opcions |= pygame.FULLSCREEN
    pantalla = pygame.display.set_mode((ANCHO, ALTO), opcions)
    pygame.display.set_caption("Gardiáns do Clima")
    pantalla_carga(pantalla)
    axustar_lenzo()
    await asyncio.sleep(0)
    juego = Juego(pantalla)
    reloj = pygame.time.Clock()
    fotograma = 0
    while juego.activo:
        dt = min(reloj.tick(FPS) / 1000, 1 / 20)
        juego.paso(dt, pygame.event.get())
        pygame.display.flip()
        fotograma += 1
        if fotograma in (2, 60, 240):
            axustar_lenzo()
        await asyncio.sleep(0)   # necesario para que o navegador siga funcionando
    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
