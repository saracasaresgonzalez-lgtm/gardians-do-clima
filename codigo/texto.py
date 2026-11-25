"""Textos suavizados, caixas redondeadas e bocadillos."""
import pygame

from config import C
from pincel import fonte

_cache = {}


class Fuentes:
    def __init__(self):
        self.p = fonte(22)   # textos pequenos
        self.m = fonte(27)   # diálogos e botóns
        self.g = fonte(40)   # rótulos
        self.t = fonte(72)   # títulos


def render(f, txt, cor):
    clave = (id(f), txt, cor)
    img = _cache.get(clave)
    if img is None:
        if len(_cache) > 1500:
            _cache.clear()
        img = _cache[clave] = f.render(txt, True, cor)
    return img


def texto(surf, f, txt, pos, color=C.TEXTO, sombra=None, centro=False):
    img = render(f, txt, color)
    x, y = pos
    if centro:
        x -= img.get_width() // 2
    if sombra:
        surf.blit(render(f, txt, sombra), (x + 2, y + 2))
    surf.blit(img, (x, y))
    return img.get_width()


def envolver(f, txt, ancho):
    lineas = []
    for par in txt.split("\n"):
        actual = ""
        for palabra in par.split(" "):
            prueba = (actual + " " + palabra).strip()
            if f.size(prueba)[0] <= ancho or not actual:
                actual = prueba
            else:
                lineas.append(actual)
                actual = palabra
        lineas.append(actual)
    return lineas


def parrafo(surf, f, txt, rect, color=C.TEXTO, sombra=None, centrado=False, max_lineas=None, interlineado=1.0):
    r = pygame.Rect(rect)
    lineas = envolver(f, txt, r.w)
    if max_lineas:
        lineas = lineas[:max_lineas]
    lh = int(f.get_linesize() * interlineado)
    y = r.y if not centrado else r.centery - len(lineas) * lh // 2
    for i, l in enumerate(lineas):
        x = r.centerx - f.size(l)[0] // 2 if centrado else r.x
        texto(surf, f, l, (x, y + i * lh), color, sombra)
    return len(lineas) * lh


def titulo(surf, f, txt, centro, color=(255, 226, 90), borde=(40, 52, 110), grosor=4):
    """Texto grande con bordo groso."""
    img = render(f, txt, color)
    b = render(f, txt, borde)
    x = centro[0] - img.get_width() // 2
    y = centro[1] - img.get_height() // 2
    for dx in range(-grosor, grosor + 1, 2):
        for dy in range(-grosor, grosor + 1, 2):
            if dx * dx + dy * dy <= grosor * grosor:
                surf.blit(b, (x + dx, y + dy))
    surf.blit(b, (x + 1, y + grosor + 1))
    surf.blit(img, (x, y))


_sombras = {}


def caja(surf, rect, fondo=C.CAJA, borde=C.CAJA_BORDE, interior=None, radio=16, sombra=True, g=4):
    r = pygame.Rect(rect)
    if sombra:
        clave = (r.w, r.h, radio)
        sm = _sombras.get(clave)
        if sm is None:
            sm = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
            pygame.draw.rect(sm, (0, 0, 0, 60), (0, 0, r.w, r.h), border_radius=radio)
            _sombras[clave] = sm
        surf.blit(sm, (r.x, r.y + 6))
    pygame.draw.rect(surf, borde, r, border_radius=radio)
    pygame.draw.rect(surf, fondo, r.inflate(-2 * g, -2 * g), border_radius=max(0, radio - g))
    if interior:
        pygame.draw.rect(surf, interior, r.inflate(-2 * g - 8, -2 * g - 8), 2, border_radius=max(0, radio - g - 2))


def triangulo(surf, x, y, color, direccion="abajo", t=14):
    if direccion == "abajo":
        pts = [(x, y), (x + t, y), (x + t // 2, y + int(t * 0.7))]
    else:
        pts = [(x, y), (x + int(t * 0.7), y + t // 2), (x, y + t)]
    pygame.draw.polygon(surf, color, pts)


def bocadillo(surf, f, txt, ancla):
    """Bocadillo de cómic; a punta sinala a 'ancla'."""
    lineas = envolver(f, txt, 300)
    lh = f.get_linesize()
    w = max(f.size(l)[0] for l in lineas) + 28
    h = len(lineas) * lh + 18
    x = min(max(8, ancla[0] - w // 2), surf.get_width() - w - 8)
    y = ancla[1] + 22
    pygame.draw.polygon(surf, C.CAJA_BORDE, [(ancla[0] - 10, y + 2), (ancla[0] + 10, y + 2), ancla])
    pygame.draw.rect(surf, C.CAJA_BORDE, (x, y, w, h), border_radius=14)
    pygame.draw.rect(surf, C.CAJA, (x + 3, y + 3, w - 6, h - 6), border_radius=12)
    pygame.draw.polygon(surf, C.CAJA, [(ancla[0] - 7, y + 4), (ancla[0] + 7, y + 4), (ancla[0], y - 10)])
    for i, l in enumerate(lineas):
        texto(surf, f, l, (x + 14, y + 9 + i * lh), (112, 40, 136))
