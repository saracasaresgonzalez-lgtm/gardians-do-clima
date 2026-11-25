"""Pincel: debuxo vectorial con contornos e suavizado (estilo ilustración infantil).

Debúxase a un tamaño 3 veces maior e despois redúcese con suavizado: así os
bordos quedan lisos (sen píxeles). Todas as coordenadas van en "unidades do
debuxo" (o tamaño final da imaxe).
"""
import math
import os

import pygame

CONT = (52, 46, 70)   # cor de contorno por defecto
_fontes = {}
# Fonte incluída co xogo (Nunito, licenza SIL OFL): vese igual no ordenador e no navegador
FONTE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fontes", "Nunito-ExtraBold.ttf")


def mestura(a, b, t):
    return tuple(int(x + (y - x) * t) for x, y in zip(a, b))


def escurecer(c, f=0.75):
    return tuple(int(v * f) for v in c[:3])


def aclarar(c, f=0.35):
    return tuple(int(v + (255 - v) * f) for v in c[:3])


def fonte(tam, negra=True):
    clave = (tam, negra)
    if clave not in _fontes:
        if os.path.exists(FONTE):
            _fontes[clave] = pygame.font.Font(FONTE, tam)
        else:
            _fontes[clave] = pygame.font.Font(None, int(tam * 1.3))
    return _fontes[clave]


class Pincel:
    def __init__(self, w, h, ss=3, fondo=None):
        self.w, self.h, self.k = w, h, ss
        self.s = pygame.Surface((int(w * ss), int(h * ss)), pygame.SRCALPHA)
        if fondo:
            self.s.fill(fondo)

    # ---------------------------------------------------------- conversión
    def P(self, x, y):
        return (round(x * self.k), round(y * self.k))

    def R(self, v):
        return max(1, round(v * self.k))

    def _re(self, cx, cy, rx, ry):
        k = self.k
        return pygame.Rect(round((cx - rx) * k), round((cy - ry) * k), max(1, round(2 * rx * k)), max(1, round(2 * ry * k)))

    # ---------------------------------------------------------- formas
    def circulo(self, x, y, r, cor, borde=CONT, g=2.5):
        if borde:
            pygame.draw.circle(self.s, borde, self.P(x, y), self.R(r + g))
        if cor:
            pygame.draw.circle(self.s, cor, self.P(x, y), self.R(r))

    def aro(self, x, y, r, cor, g=2.5):
        pygame.draw.circle(self.s, cor, self.P(x, y), self.R(r + g / 2), self.R(g))

    def elipse(self, cx, cy, rx, ry, cor, borde=CONT, g=2.5):
        if borde:
            pygame.draw.ellipse(self.s, borde, self._re(cx, cy, rx + g, ry + g))
        if cor:
            pygame.draw.ellipse(self.s, cor, self._re(cx, cy, rx, ry))

    def rect(self, x, y, w, h, cor, radio=0, borde=CONT, g=2.5):
        k = self.k
        if borde:
            pygame.draw.rect(self.s, borde, pygame.Rect(round((x - g) * k), round((y - g) * k),
                                                        round((w + 2 * g) * k), round((h + 2 * g) * k)),
                             border_radius=round((radio + g) * k) if radio else 0)
        if cor:
            pygame.draw.rect(self.s, cor, pygame.Rect(round(x * k), round(y * k), round(w * k), round(h * k)),
                             border_radius=round(radio * k) if radio else 0)

    def poli(self, pts, cor, borde=CONT, g=2.5):
        P = [self.P(x, y) for x, y in pts]
        if borde:
            w = self.R(2 * g)
            for i in range(len(P)):
                a, b = P[i], P[(i + 1) % len(P)]
                pygame.draw.line(self.s, borde, a, b, w)
                pygame.draw.circle(self.s, borde, a, w // 2)
        if cor:
            pygame.draw.polygon(self.s, cor, P)

    def linha(self, pts, cor, g=2.5, pechar=False):
        P = [self.P(x, y) for x, y in pts]
        w = self.R(g)
        n = len(P) if pechar else len(P) - 1
        for i in range(n):
            pygame.draw.line(self.s, cor, P[i], P[(i + 1) % len(P)], w)
        for q in P:
            pygame.draw.circle(self.s, cor, q, max(1, w // 2))

    def linha_contorno(self, pts, cor, g=4, borde=CONT, gb=2):
        if borde:
            self.linha(pts, borde, g + 2 * gb)
        self.linha(pts, cor, g)

    def arco(self, cx, cy, r, a0, a1, cor, g=2.5, n=28, borde=None):
        pts = [(cx + math.cos(a0 + (a1 - a0) * i / n) * r, cy + math.sin(a0 + (a1 - a0) * i / n) * r) for i in range(n + 1)]
        if borde:
            self.linha(pts, borde, g + 3)
        self.linha(pts, cor, g)

    def degradado(self, x, y, w, h, c1, c2):
        k = self.k
        y0, y1 = round(y * k), round((y + h) * k)
        for yy in range(y0, y1):
            t = (yy - y0) / max(1, y1 - y0 - 1)
            pygame.draw.line(self.s, mestura(c1, c2, t), (round(x * k), yy), (round((x + w) * k) - 1, yy))

    def sombra(self, cx, cy, rx, ry, alfa=70):
        capa = pygame.Surface(self.s.get_size(), pygame.SRCALPHA)
        pygame.draw.ellipse(capa, (0, 0, 0, alfa), self._re(cx, cy, rx, ry))
        self.s.blit(capa, (0, 0))

    def texto(self, txt, x, y, tam, cor, centro=True, borde=None):
        f = fonte(round(tam * self.k))
        img = f.render(txt, True, cor)
        px, py = self.P(x, y)
        if centro:
            px -= img.get_width() // 2
            py -= img.get_height() // 2
        if borde:
            b = f.render(txt, True, borde)
            g = self.R(1.5)
            for dx in (-g, 0, g):
                for dy in (-g, 0, g):
                    if dx or dy:
                        self.s.blit(b, (px + dx, py + dy))
        self.s.blit(img, (px, py))

    def pegar(self, surf, x, y, w, h):
        img = pygame.transform.smoothscale(surf, (self.R(w), self.R(h)))
        self.s.blit(img, self.P(x, y))

    def imaxe(self, w=None, h=None):
        return pygame.transform.smoothscale(self.s, (w or self.w, h or self.h))
