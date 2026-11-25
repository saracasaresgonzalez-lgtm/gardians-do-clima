"""Todas as ilustracións do xogo, debuxadas por código en estilo infantil
(formas suaves con contorno). Créanse a demanda e gárdanse en caché.

Uso:  j.arte.imaxe("carballo", 160, 160)
"""
import math
import random

import pygame

from pincel import Pincel, CONT, escurecer, aclarar, mestura

DEBUXOS = {}


def debuxo(nome, w, h):
    def rexistrar(f):
        DEBUXOS[nome] = (f, w, h)
        return f
    return rexistrar


class Arte:
    def __init__(self):
        self.base = {}
        self.escaladas = {}

    def existe(self, nome):
        return nome in DEBUXOS or nome in _MAPAS

    def base_de(self, nome):
        if nome not in self.base:
            if nome in DEBUXOS:
                f, w, h = DEBUXOS[nome]
                self.base[nome] = f()
            else:
                import mapas
                self.base[nome] = getattr(mapas, _MAPAS[nome])(*_TAM_MAPAS[nome])[0]
        return self.base[nome]

    def imaxe(self, nome, w=None, h=None):
        """Devolve a imaxe (escalada con suavizado se se pide un tamaño)."""
        if nome not in DEBUXOS and nome not in _MAPAS and ("ic_" + nome) in DEBUXOS:
            nome = "ic_" + nome
        base = self.base_de(nome)
        if w is None:
            return base
        if h is None:
            h = round(base.get_height() * w / base.get_width())
        clave = (nome, w, h)
        if clave not in self.escaladas:
            self.escaladas[clave] = pygame.transform.smoothscale(base, (w, h))
        return self.escaladas[clave]

    def encaixar(self, nome, w, h):
        """Escala mantendo a proporción para caber en w x h."""
        base = self.base_de(nome if self.existe(nome) else "ic_" + nome)
        f = min(w / base.get_width(), h / base.get_height())
        return self.imaxe(nome, max(1, round(base.get_width() * f)), max(1, round(base.get_height() * f)))


_MAPAS = {"mapa_espana": "mapa_espana", "mapa_galicia": "mapa_galicia", "globo": "globo_zonas"}
_TAM_MAPAS = {"mapa_espana": (600, 460), "mapa_galicia": (420, 420), "globo": (300, 300)}

# ================================================================ axudas comúns

BRANCO = (255, 255, 255)
NUBE_B = (252, 253, 255)
NUBE_G = (214, 222, 236)
NUBE_E = (130, 140, 168)
BORDE_NUBE = (92, 112, 156)
AZUL_PINGA = (66, 140, 236)
SOL = (255, 212, 64)
SOL_B = (232, 140, 40)
VERDE_C = (112, 196, 92)
VERDE_E = (52, 140, 72)
TRONCO = (138, 92, 56)


def nube(p, cx, cy, e, cor=NUBE_B, borde=BORDE_NUBE, g=2.5):
    """Nube de debuxo animado. e = escala (1 ≈ 60 px de ancho)."""
    circ = [(-18, 4, 13), (-4, -6, 17), (14, -2, 14), (24, 7, 10), (2, 8, 13), (-24, 9, 8)]
    for dx, dy, r in circ:
        p.circulo(cx + dx * e, cy + dy * e, r * e, None, borde=borde, g=g)
    for dx, dy, r in circ:
        p.circulo(cx + dx * e, cy + dy * e, r * e, cor, borde=None)
    p.elipse(cx - 6 * e, cy - 9 * e, 6 * e, 3.5 * e, aclarar(cor, 0.6), borde=None)


def sol(p, cx, cy, r, cara=False):
    for k in range(10):
        a = k * math.pi / 5
        p.linha_contorno([(cx + math.cos(a) * (r + 6), cy + math.sin(a) * (r + 6)),
                          (cx + math.cos(a) * (r + 16), cy + math.sin(a) * (r + 16))], SOL, g=r * 0.28, borde=SOL_B, gb=1.5)
    p.circulo(cx, cy, r, SOL, borde=SOL_B, g=2.5)
    p.circulo(cx - r * 0.35, cy - r * 0.35, r * 0.3, (255, 236, 150), borde=None)
    if cara:
        p.circulo(cx - r * 0.3, cy - r * 0.1, r * 0.1, (90, 60, 30), borde=None)
        p.circulo(cx + r * 0.3, cy - r * 0.1, r * 0.1, (90, 60, 30), borde=None)
        p.arco(cx, cy + r * 0.1, r * 0.35, 0.2 * math.pi, 0.8 * math.pi, (90, 60, 30), g=r * 0.08)


def pinga(p, x, y, e=1, cor=AZUL_PINGA, borde=(40, 90, 170)):
    pts = [(x, y - 9 * e), (x + 5.5 * e, y), (x + 5 * e, y + 4 * e), (x, y + 7 * e), (x - 5 * e, y + 4 * e), (x - 5.5 * e, y)]
    p.poli(pts, cor, borde=borde, g=1.5)
    p.circulo(x - 2 * e, y + 1 * e, 1.3 * e, (200, 230, 255), borde=None)


def folerpa(p, x, y, e=1, cor=BRANCO, borde=(90, 140, 220)):
    brazos = []
    for k in range(3):
        a = k * math.pi / 3
        brazos.append([(x - math.cos(a) * 7 * e, y - math.sin(a) * 7 * e), (x + math.cos(a) * 7 * e, y + math.sin(a) * 7 * e)])
    for b in brazos:
        p.linha(b, borde, g=4 * e)
    for b in brazos:
        p.linha(b, cor, g=2 * e)


def lostrego(p, x, y, e=1):
    pts = [(0, 0), (14, 0), (8, 14), (18, 14), (-2, 40), (4, 20), (-6, 20)]
    p.poli([(x + a * e, y + b * e) for a, b in pts], (255, 226, 60), borde=(200, 120, 20), g=2)


def ceo(p, c1=(132, 196, 250), c2=(214, 238, 255)):
    p.degradado(0, 0, p.w, p.h, c1, c2)


def chan(p, y, cor=(118, 196, 96), ondas=(0, -8, 4, -6, 2), borde=None):
    n = len(ondas)
    pts = [(p.w * i / (n - 1), y + ondas[i]) for i in range(n)]
    pts += [(p.w + 5, p.h + 5), (-5, p.h + 5)]
    p.poli(pts, cor, borde=borde or escurecer(cor, 0.7), g=2)


def outeiro(p, x, y, rx, ry, cor):
    p.elipse(x, y, rx, ry, cor, borde=escurecer(cor, 0.75), g=2)


def montana(p, x, base, w, h, cor=(150, 140, 130), neve=True):
    pico = (x, base - h)
    p.poli([(x - w / 2, base), pico, (x + w / 2, base)], cor, borde=escurecer(cor, 0.6), g=2.5)
    p.poli([pico, (x + w / 2, base), (x + w * 0.05, base)], escurecer(cor, 0.85), borde=None)
    if neve:
        t = 0.32
        a = (x - w / 2 * t, base - h * (1 - t))
        b = (x + w / 2 * t, base - h * (1 - t))
        p.poli([pico, b, (x + w * 0.08, base - h * (1 - t) + 8), (x - w * 0.04, base - h * (1 - t) + 2),
                (x - w * 0.1, base - h * (1 - t) + 9), a], (250, 252, 255), borde=(170, 190, 220), g=1.5)


# ---------------------------------------------------------------- árbores laterais (para paisaxes e tarxetas)

def arbore_carballo(p, x, base, e=1, cor=(76, 164, 76)):
    p.poli([(x - 6 * e, base), (x - 4 * e, base - 40 * e), (x + 4 * e, base - 40 * e), (x + 7 * e, base)], TRONCO, g=2)
    copa = [(-20, -52, 18), (0, -64, 22), (20, -52, 18), (-10, -42, 16), (12, -40, 16), (0, -48, 18)]
    for dx, dy, r in copa:
        p.circulo(x + dx * e, base + dy * e, r * e, None, borde=escurecer(cor, 0.55), g=2.5)
    for dx, dy, r in copa:
        p.circulo(x + dx * e, base + dy * e, r * e, cor, borde=None)
    p.circulo(x - 8 * e, base - 66 * e, 8 * e, aclarar(cor, 0.3), borde=None)
    p.circulo(x + 14 * e, base - 44 * e, 7 * e, escurecer(cor, 0.85), borde=None)


def arbore_faia(p, x, base, e=1, cor=(120, 182, 70)):
    p.poli([(x - 5 * e, base), (x - 3 * e, base - 50 * e), (x + 3 * e, base - 50 * e), (x + 5 * e, base)], (150, 144, 134), g=2)
    p.elipse(x, base - 74 * e, 22 * e, 38 * e, cor, borde=escurecer(cor, 0.55), g=2.5)
    p.elipse(x - 7 * e, base - 86 * e, 8 * e, 14 * e, aclarar(cor, 0.3), borde=None)
    p.elipse(x + 8 * e, base - 62 * e, 8 * e, 12 * e, escurecer(cor, 0.85), borde=None)


def arbore_pineiro(p, x, base, e=1, cor=(46, 120, 72)):
    p.linha_contorno([(x, base), (x - 3 * e, base - 30 * e), (x + 4 * e, base - 56 * e)], (150, 96, 60), g=6 * e, gb=2)
    for dx, dy, rx, ry in ((-14, -60, 22, 9), (14, -62, 24, 9), (2, -70, 22, 9)):
        p.elipse(x + dx * e, base + dy * e, rx * e, ry * e, cor, borde=escurecer(cor, 0.55), g=2.5)
    p.elipse(x - 4 * e, base - 73 * e, 10 * e, 4 * e, aclarar(cor, 0.25), borde=None)


def arbore_acineira(p, x, base, e=1, cor=(74, 110, 64)):
    p.poli([(x - 6 * e, base), (x - 4 * e, base - 24 * e), (x + 4 * e, base - 24 * e), (x + 6 * e, base)], TRONCO, g=2)
    for dx, dy, r in ((-14, -34, 14), (12, -34, 14), (0, -44, 17), (0, -30, 15)):
        p.circulo(x + dx * e, base + dy * e, r * e, None, borde=escurecer(cor, 0.55), g=2.5)
    for dx, dy, r in ((-14, -34, 14), (12, -34, 14), (0, -44, 17), (0, -30, 15)):
        p.circulo(x + dx * e, base + dy * e, r * e, cor, borde=None)
    for dx, dy in ((-8, -46), (8, -38), (-14, -30), (4, -28)):
        p.circulo(x + dx * e, base + dy * e, 2.2 * e, aclarar(cor, 0.3), borde=None)


def arbore_drago(p, x, base, e=1):
    tr = (176, 160, 140)
    p.poli([(x - 9 * e, base), (x - 6 * e, base - 34 * e), (x + 6 * e, base - 34 * e), (x + 9 * e, base)], tr, g=2)
    ramas = [(-26, -58), (-10, -64), (8, -66), (26, -58)]
    for dx, dy in ramas:
        p.linha_contorno([(x, base - 32 * e), (x + dx * 0.6 * e, base + (dy + 16) * e), (x + dx * e, base + dy * e)], tr, g=6 * e, gb=2)
    for dx, dy in ramas:
        for k in range(7):
            a = -math.pi / 2 + (k - 3) * 0.32
            p.linha_contorno([(x + dx * e, base + dy * e), (x + (dx + math.cos(a) * 14) * e, base + (dy + math.sin(a) * 12) * e)],
                             (86, 150, 86), g=3 * e, borde=(40, 90, 50), gb=1)


def arbore_palmeira(p, x, base, e=1):
    pts = [(x + math.sin(t / 10) * 6 * e, base - t * e) for t in range(0, 92, 8)]
    p.linha_contorno(pts, (176, 130, 80), g=8 * e, gb=2)
    for t in range(6, 88, 10):
        q = (x + math.sin(t / 10) * 6 * e, base - t * e)
        p.linha([(q[0] - 4 * e, q[1]), (q[0] + 4 * e, q[1])], (130, 90, 56), g=1.5)
    top = pts[-1]
    for k in range(7):
        a = math.pi + k * math.pi / 6
        fin = (top[0] + math.cos(a) * 34 * e, top[1] + math.sin(a) * 18 * e + 14 * e * abs(math.cos(a)))
        medio = (top[0] + math.cos(a) * 18 * e, top[1] + math.sin(a) * 14 * e - 4 * e)
        p.linha_contorno([top, medio, fin], (70, 160, 80), g=6 * e, borde=(36, 96, 52), gb=1.5)


def arbore_conifera(p, x, base, e=1, neve=False):
    p.rect(x - 3 * e, base - 10 * e, 6 * e, 10 * e, TRONCO, g=1.5)
    for k, (w, y) in enumerate(((22, -10), (17, -26), (12, -40))):
        p.poli([(x - w * e, base + y * e), (x, base + (y - 22) * e), (x + w * e, base + y * e)], (46, 128, 84),
               borde=(26, 80, 50), g=2)
        if neve:
            p.poli([(x - w * 0.5 * e, base + (y - 11) * e), (x, base + (y - 22) * e), (x + w * 0.5 * e, base + (y - 11) * e)],
                   (250, 252, 255), borde=None)


def matogueira(p, x, base, e=1, cor=(110, 150, 70), flores=(220, 120, 200)):
    for dx, dy, r in ((-10, -8, 9), (8, -8, 9), (0, -14, 10)):
        p.circulo(x + dx * e, base + dy * e, r * e, None, borde=escurecer(cor, 0.55), g=2)
    for dx, dy, r in ((-10, -8, 9), (8, -8, 9), (0, -14, 10)):
        p.circulo(x + dx * e, base + dy * e, r * e, cor, borde=None)
    if flores:
        for dx, dy in ((-8, -12), (4, -18), (10, -8), (-2, -6)):
            p.circulo(x + dx * e, base + dy * e, 2 * e, flores, borde=None)


def casa_lateral(p, x, base, e=1, teito=(210, 82, 64)):
    p.rect(x - 22 * e, base - 30 * e, 44 * e, 30 * e, (248, 238, 214), g=2)
    p.poli([(x - 28 * e, base - 28 * e), (x, base - 50 * e), (x + 28 * e, base - 28 * e)], teito, g=2)
    p.rect(x - 5 * e, base - 16 * e, 10 * e, 16 * e, (150, 96, 56), g=1.5)
    p.rect(x + 9 * e, base - 22 * e, 8 * e, 8 * e, (150, 200, 240), g=1.5)


# ================================================================ PERSONAXES

def _nubi(cor, borde):
    p = Pincel(140, 100)
    circ = [(36, 60, 24), (62, 40, 30), (96, 40, 26), (114, 62, 21), (72, 66, 27), (46, 72, 18), (98, 72, 19)]
    for x, y, r in circ:
        p.circulo(x, y, r, None, borde=borde, g=3.5)
    for x, y, r in circ:
        p.circulo(x, y, r, cor, borde=None)
    p.elipse(52, 34, 10, 6, aclarar(cor, 0.7), borde=None)
    p.elipse(60, 60, 6, 8, (44, 44, 64), borde=None)
    p.elipse(88, 60, 6, 8, (44, 44, 64), borde=None)
    p.circulo(58, 57, 2.4, BRANCO, borde=None)
    p.circulo(86, 57, 2.4, BRANCO, borde=None)
    p.elipse(47, 72, 7, 4, (255, 166, 188), borde=None)
    p.elipse(101, 72, 7, 4, (255, 166, 188), borde=None)
    p.arco(74, 67, 8, 0.15 * math.pi, 0.85 * math.pi, (44, 44, 64), g=2.8)
    return p.imaxe()


@debuxo("nubi", 140, 100)
def d_nubi():
    return _nubi(NUBE_B, BORDE_NUBE)


@debuxo("nubi_gris", 140, 100)
def d_nubi_gris():
    return _nubi((196, 206, 224), (78, 92, 130))


@debuxo("retrato_nubi", 200, 200)
def d_retrato_nubi():
    p = Pincel(200, 200)
    p.pegar(_nubi(NUBE_B, BORDE_NUBE), 10, 40, 180, 129)
    return p.imaxe()


@debuxo("retrato_brisa", 200, 200)
def d_brisa():
    p = Pincel(200, 200)
    pelo = (72, 152, 226)
    p.poli([(28, 204), (38, 162), (70, 142), (130, 142), (162, 162), (172, 204)], (250, 250, 253))
    p.poli([(84, 143), (116, 143), (100, 176)], (250, 200, 80), g=2)
    p.linha([(84, 143), (96, 196)], (196, 204, 222), g=3)
    p.linha([(116, 143), (104, 196)], (196, 204, 222), g=3)
    p.rect(48, 168, 22, 6, (90, 160, 230), radio=2, g=1.5)
    p.rect(88, 120, 24, 26, (250, 206, 172), g=2)
    p.circulo(100, 92, 56, pelo)
    p.circulo(100, 30, 22, pelo)
    p.elipse(100, 98, 40, 44, (255, 218, 188))
    p.poli([(58, 92), (62, 64), (80, 50), (100, 46), (122, 50), (140, 64), (142, 92), (128, 74), (110, 80),
            (96, 68), (80, 80), (68, 74)], pelo, g=2)
    p.linha([(78, 58), (98, 52)], aclarar(pelo, 0.45), g=4)
    p.elipse(84, 102, 5, 6.5, (44, 44, 64), borde=None)
    p.elipse(116, 102, 5, 6.5, (44, 44, 64), borde=None)
    p.circulo(82.5, 99.5, 1.8, BRANCO, borde=None)
    p.circulo(114.5, 99.5, 1.8, BRANCO, borde=None)
    p.aro(84, 102, 13, (210, 64, 84), g=3.5)
    p.aro(116, 102, 13, (210, 64, 84), g=3.5)
    p.linha([(97, 101), (103, 101)], (210, 64, 84), g=3.5)
    p.elipse(72, 122, 7, 4, (255, 172, 172), borde=None)
    p.elipse(128, 122, 7, 4, (255, 172, 172), borde=None)
    p.arco(100, 112, 3, 0.1 * math.pi, 0.9 * math.pi, (214, 150, 130), g=2.2)
    p.arco(100, 118, 11, 0.2 * math.pi, 0.8 * math.pi, (160, 60, 70), g=3)
    return p.imaxe()


@debuxo("retrato_baron", 200, 200)
def d_baron():
    p = Pincel(200, 200)
    capa = (118, 52, 150)
    p.poli([(22, 204), (34, 160), (70, 140), (130, 140), (166, 160), (178, 204)], capa)
    p.poli([(64, 148), (46, 112), (84, 136)], aclarar(capa, 0.2), g=2)
    p.poli([(136, 148), (154, 112), (116, 136)], aclarar(capa, 0.2), g=2)
    p.poli([(88, 142), (112, 142), (100, 170)], (246, 246, 240), g=2)
    p.circulo(100, 180, 4.5, (240, 200, 70), g=1.5)
    p.circulo(100, 194, 4.5, (240, 200, 70), g=1.5)
    p.rect(88, 122, 24, 24, (232, 218, 205), g=2)
    p.elipse(58, 102, 7, 11, (232, 218, 205))
    p.elipse(142, 102, 7, 11, (232, 218, 205))
    p.elipse(100, 100, 40, 44, (238, 226, 212))
    p.linha_contorno([(70, 80), (92, 90)], (60, 46, 44), g=7, borde=None)
    p.linha_contorno([(130, 80), (108, 90)], (60, 46, 44), g=7, borde=None)
    p.elipse(84, 98, 4.5, 5.5, (30, 30, 40), borde=None)
    p.elipse(116, 98, 4.5, 5.5, (30, 30, 40), borde=None)
    p.aro(116, 98, 11, (232, 190, 60), g=3.5)
    p.linha([(126, 104), (136, 122), (132, 142)], (232, 190, 60), g=2)
    p.elipse(100, 112, 6, 8, (224, 198, 182), borde=(150, 120, 110), g=1.5)
    bigote = (78, 56, 44)
    p.poli([(100, 124), (86, 118), (70, 122), (60, 116), (60, 126), (74, 133), (92, 131)], bigote, g=2)
    p.poli([(100, 124), (114, 118), (130, 122), (140, 116), (140, 126), (126, 133), (108, 131)], bigote, g=2)
    p.circulo(60, 112, 4.5, bigote, g=2)
    p.circulo(140, 112, 4.5, bigote, g=2)
    p.arco(106, 134, 8, 0.15 * math.pi, 0.7 * math.pi, (130, 50, 56), g=2.8)
    p.rect(66, 8, 68, 58, (44, 38, 56), radio=4)
    p.rect(66, 50, 68, 12, (156, 64, 186), borde=None)
    p.elipse(100, 66, 58, 9, (44, 38, 56))
    p.rect(74, 14, 7, 32, (84, 76, 100), radio=3, borde=None)
    return p.imaxe()


@debuxo("retrato_tubito", 200, 200)
def d_tubito():
    p = Pincel(200, 200)
    met = (180, 190, 208)
    p.rect(56, 150, 88, 54, (150, 160, 182), radio=16)
    p.circulo(100, 174, 8, (250, 204, 70), g=2)
    p.rect(90, 132, 20, 20, (112, 120, 142), g=2)
    for x in (26, 150):
        p.rect(x, 50, 24, 52, (112, 120, 142), radio=6)
        p.elipse(x + 12, 50, 14, 6, (64, 68, 86), g=2)
    for x, y, r in ((34, 32, 9), (46, 18, 7), (166, 30, 10), (154, 14, 7)):
        p.circulo(x, y, r, (206, 206, 214), borde=(130, 130, 146), g=2)
    p.rect(42, 60, 116, 80, met, radio=28)
    p.rect(58, 76, 84, 42, (36, 46, 78), radio=18, g=2)
    for x in (82, 118):
        p.circulo(x, 97, 12, (100, 232, 250), borde=None)
        p.circulo(x + 2, 95, 5, (20, 30, 54), borde=None)
        p.circulo(x - 3, 91, 2.2, BRANCO, borde=None)
    p.rect(88, 124, 24, 7, (240, 84, 84), radio=3, g=1.5)
    p.circulo(52, 100, 3.5, (120, 128, 150), g=1.5)
    p.circulo(148, 100, 3.5, (120, 128, 150), g=1.5)
    p.rect(58, 66, 44, 6, (226, 232, 244), radio=3, borde=None)
    return p.imaxe()


@debuxo("globo", 150, 184)
def d_globo():
    p = Pincel(150, 184)
    p.linha([(44, 104), (56, 146)], (96, 72, 52), g=2.5)
    p.linha([(106, 104), (94, 146)], (96, 72, 52), g=2.5)
    roxo = (132, 70, 184)
    p.elipse(75, 64, 60, 60, roxo, g=3)
    p.elipse(75, 64, 36, 60, (152, 96, 204), borde=None)
    p.elipse(75, 64, 13, 60, roxo, borde=None)
    p.elipse(48, 34, 10, 17, (204, 176, 234), borde=None)
    nube(p, 76, 66, 0.55, (226, 222, 236), borde=(90, 80, 104), g=2)
    p.poli([(52, 116), (98, 116), (90, 128), (60, 128)], (100, 50, 140), g=2)
    # Barón (sombreiro e cara)
    p.elipse(64, 148, 10, 9, (238, 226, 212), g=2)
    p.rect(54, 124, 20, 16, (44, 38, 56), radio=2, g=2)
    p.elipse(64, 140, 15, 3.5, (44, 38, 56), g=2)
    p.linha([(57, 153), (71, 153)], (78, 56, 44), g=3)
    # Tubiño
    p.rect(80, 136, 24, 20, (180, 190, 208), radio=7, g=2)
    p.rect(84, 141, 16, 8, (36, 46, 78), radio=3, borde=None)
    p.circulo(88, 145, 2, (100, 232, 250), borde=None)
    p.circulo(96, 145, 2, (100, 232, 250), borde=None)
    # cesta
    p.rect(44, 150, 62, 28, (184, 128, 70), radio=5, g=2.5)
    for y in (158, 166):
        p.linha([(46, y), (104, y)], (140, 92, 50), g=2)
    for x in range(52, 104, 10):
        p.linha([(x, 152), (x, 176)], (150, 100, 56), g=1.5)
    return p.imaxe()


# ================================================================ MAPA DO VAL (vista desde arriba)

def _arbore_top(cor):
    p = Pincel(56, 64)
    p.sombra(28, 56, 20, 6, 70)
    p.rect(24, 40, 8, 16, (130, 86, 50), radio=3, g=2)
    copa = [(18, 32, 14), (38, 30, 14), (28, 18, 15), (28, 36, 15)]
    for x, y, r in copa:
        p.circulo(x, y, r, None, borde=escurecer(cor, 0.5), g=2.5)
    for x, y, r in copa:
        p.circulo(x, y, r, cor, borde=None)
    p.circulo(34, 38, 9, escurecer(cor, 0.86), borde=None)
    p.circulo(22, 20, 6, aclarar(cor, 0.3), borde=None)
    p.circulo(28, 13, 3, aclarar(cor, 0.5), borde=None)
    return p.imaxe()


@debuxo("arbore0", 56, 64)
def d_arb0():
    return _arbore_top((72, 166, 82))


@debuxo("arbore1", 56, 64)
def d_arb1():
    return _arbore_top((96, 180, 70))


@debuxo("arbore2", 56, 64)
def d_arb2():
    return _arbore_top((58, 150, 100))


@debuxo("mato", 44, 38)
def d_mato():
    p = Pincel(44, 38)
    p.sombra(22, 33, 18, 4, 60)
    cor = (218, 184, 96)
    cl = [(13, 24, 10), (30, 23, 11), (22, 15, 10)]
    for x, y, r in cl:
        p.circulo(x, y, r, None, borde=(130, 96, 50), g=2.2)
    for x, y, r in cl:
        p.circulo(x, y, r, cor, borde=None)
    for x, y in ((16, 12), (26, 18), (10, 22)):
        p.circulo(x, y, 2.5, (240, 214, 150), borde=None)
    for a, b in (((20, 6), (18, 1)), ((28, 10), (33, 5))):
        p.linha([a, b], (140, 100, 56), g=1.8)
    return p.imaxe()


@debuxo("queimado", 48, 36)
def d_queimado():
    p = Pincel(48, 36)
    p.elipse(24, 24, 20, 10, (92, 80, 70), borde=None)
    p.rect(19, 12, 10, 14, (52, 42, 38), radio=2, g=1.5)
    for x, y in ((8, 22), (40, 26), (32, 30), (12, 30), (36, 18)):
        p.circulo(x, y, 1.8, (170, 160, 156), borde=None)
    p.circulo(24, 14, 1.8, (240, 120, 50), borde=None)
    return p.imaxe()


def _lume(punta):
    p = Pincel(44, 56)
    tx, ty = punta
    p.poli([(22, 54), (6, 44), (5, 30), (12, 20), (16, 26), (tx, ty), (30, 18), (38, 28), (39, 42)], (238, 84, 40),
           borde=(170, 50, 30), g=2)
    p.poli([(22, 52), (11, 44), (11, 34), (17, 28), (21, 34), (tx + 2, ty + 14), (31, 32), (33, 44)], (250, 156, 40),
           borde=None)
    p.poli([(22, 50), (16, 44), (17, 38), (22, 40), (25, 34), (28, 42), (28, 46)], (255, 232, 110), borde=None)
    return p.imaxe()


@debuxo("lume0", 44, 56)
def d_l0():
    return _lume((20, 4))


@debuxo("lume1", 44, 56)
def d_l1():
    return _lume((27, 6))


@debuxo("lume2", 44, 56)
def d_l2():
    return _lume((17, 8))


@debuxo("casa", 62, 62)
def d_casa():
    p = Pincel(62, 62)
    p.sombra(32, 54, 26, 6, 60)
    p.rect(10, 26, 42, 28, (248, 238, 214), g=2.5)
    p.rect(40, 6, 7, 14, (150, 90, 70), g=2)
    p.poli([(4, 30), (31, 6), (58, 30)], (214, 84, 66), g=2.5)
    p.linha([(31, 9), (31, 28)], (180, 64, 52), g=1.5)
    p.rect(26, 38, 10, 16, (150, 96, 56), radio=2, g=2)
    p.rect(13, 34, 9, 9, (150, 204, 244), g=1.5)
    p.rect(40, 34, 9, 9, (150, 204, 244), g=1.5)
    return p.imaxe()


# ================================================================ SÍMBOLOS DO TEMPO (96x96)

def _ic_nube(p, cor=NUBE_B, borde=BORDE_NUBE, y=46, e=1.25):
    nube(p, 48, y, e, cor, borde, g=3)


@debuxo("ic_soleado", 96, 96)
def ic_soleado():
    p = Pincel(96, 96)
    sol(p, 48, 48, 20, cara=True)
    return p.imaxe()


@debuxo("ic_sol_nubes", 96, 96)
def ic_sol_nubes():
    p = Pincel(96, 96)
    sol(p, 36, 34, 15)
    nube(p, 56, 58, 1.0, NUBE_B, BORDE_NUBE, g=3)
    return p.imaxe()


@debuxo("ic_nubrado", 96, 96)
def ic_nubrado():
    p = Pincel(96, 96)
    nube(p, 38, 38, 0.9, NUBE_G, BORDE_NUBE, g=3)
    nube(p, 56, 58, 1.05, NUBE_B, BORDE_NUBE, g=3)
    return p.imaxe()


@debuxo("ic_chuvia", 96, 96)
def ic_chuvia():
    p = Pincel(96, 96)
    for x, y in ((30, 72), (50, 80), (70, 72)):
        pinga(p, x, y, 1.2)
    _ic_nube(p, NUBE_G, y=38)
    return p.imaxe()


@debuxo("ic_neve", 96, 96)
def ic_neve():
    p = Pincel(96, 96)
    for x, y in ((28, 74), (50, 82), (72, 74)):
        folerpa(p, x, y, 1.3)
    _ic_nube(p, NUBE_G, y=38)
    return p.imaxe()


@debuxo("ic_sarabia", 96, 96)
def ic_sarabia():
    p = Pincel(96, 96)
    for x, y in ((28, 72), (48, 82), (68, 74), (38, 88)):
        p.circulo(x, y, 6, (250, 252, 255), borde=(120, 136, 170), g=2.5)
    _ic_nube(p, NUBE_E, borde=(70, 76, 100), y=38)
    return p.imaxe()


@debuxo("ic_treboada", 96, 96)
def ic_treboada():
    p = Pincel(96, 96)
    lostrego(p, 42, 50, 1.0)
    _ic_nube(p, NUBE_E, borde=(70, 76, 100), y=36)
    return p.imaxe()


@debuxo("ic_vento", 96, 96)
def ic_vento():
    p = Pincel(96, 96)
    cor, b = (150, 200, 250), (60, 100, 170)
    for y, x1, x2 in ((28, 10, 62), (48, 4, 78), (68, 14, 56)):
        pts = [(x1, y), (x2, y)]
        pts += [(x2 + math.cos(a) * 8, y - 8 + math.sin(a) * 8) for a in [math.pi / 2 - i * 0.5 for i in range(9)]]
        p.linha(pts, b, g=8)
        p.linha(pts, cor, g=4.5)
    return p.imaxe()


@debuxo("ic_arco", 96, 96)
def ic_arco():
    p = Pincel(96, 96)
    cores = [(232, 64, 64), (248, 152, 40), (250, 222, 64), (88, 196, 88), (72, 144, 232), (144, 88, 208)]
    for i, c in enumerate(cores):
        p.arco(48, 70, 38 - i * 5, math.pi, 2 * math.pi, c, g=5.5)
    nube(p, 18, 70, 0.45, NUBE_B, BORDE_NUBE, g=2)
    nube(p, 78, 70, 0.45, NUBE_B, BORDE_NUBE, g=2)
    return p.imaxe()


@debuxo("ic_aurora", 96, 96)
def ic_aurora():
    p = Pincel(96, 96)
    p.rect(6, 6, 84, 84, (24, 32, 86), radio=16, borde=(14, 20, 50), g=3)
    for x in range(10, 86, 2):
        y = 36 + math.sin(x / 9) * 8
        p.linha([(x, y), (x, y + 18)], (90, 236, 160), g=2.2)
        p.linha([(x, y + 12), (x, y + 24)], (70, 190, 210), g=2.2)
    for x, y in ((20, 18), (70, 16), (50, 24), (80, 70)):
        p.circulo(x, y, 1.6, BRANCO, borde=None)
    p.poli([(8, 86), (8, 72), (30, 64), (50, 74), (70, 62), (88, 70), (88, 86)], (226, 236, 250), borde=None)
    return p.imaxe()


@debuxo("ic_lume", 96, 96)
def ic_lume():
    p = Pincel(96, 96)
    p.pegar(_lume((20, 4)), 18, 10, 60, 76)
    return p.imaxe()


# ================================================================ ILUSTRACIÓNS (300x220)

W, H = 300, 220


def _lago(p, y=176):
    p.poli([(0, y), (70, y - 10), (180, y - 6), (300, y - 12), (300, 220), (0, 220)], (90, 160, 236), borde=(50, 110, 190), g=2)
    for x, yy in ((40, y + 18), (150, y + 22), (240, y + 14)):
        p.linha([(x, yy), (x + 26, yy)], (190, 224, 255), g=3)


@debuxo("chuvia", W, H)
def i_chuvia():
    p = Pincel(W, H)
    ceo(p, (120, 140, 176), (176, 196, 220))
    chan(p, 184, (110, 178, 92))
    rng = random.Random(1)
    for _ in range(16):
        pinga(p, rng.randrange(40, 260), rng.randrange(96, 176), 1.1)
    nube(p, 150, 62, 2.6, NUBE_G, BORDE_NUBE, g=3)
    p.elipse(80, 200, 26, 6, (130, 190, 240), borde=(60, 120, 190), g=1.5)
    p.elipse(210, 196, 20, 5, (130, 190, 240), borde=(60, 120, 190), g=1.5)
    return p.imaxe()


@debuxo("neve", W, H)
def i_neve():
    p = Pincel(W, H)
    ceo(p, (150, 172, 210), (206, 218, 238))
    chan(p, 172, (246, 250, 255), borde=(170, 190, 224))
    arbore_conifera(p, 52, 196, 1.6, neve=True)
    arbore_conifera(p, 250, 192, 1.3, neve=True)
    rng = random.Random(2)
    for _ in range(14):
        folerpa(p, rng.randrange(60, 240), rng.randrange(96, 166), 1.2)
    nube(p, 150, 58, 2.5, NUBE_G, BORDE_NUBE, g=3)
    return p.imaxe()


@debuxo("sarabia", W, H)
def i_sarabia():
    p = Pincel(W, H)
    ceo(p, (90, 100, 136), (150, 160, 186))
    chan(p, 184, (104, 168, 90))
    rng = random.Random(3)
    for _ in range(14):
        p.circulo(rng.randrange(40, 260), rng.randrange(98, 176), 5, (250, 252, 255), borde=(110, 126, 160), g=2)
    for x in range(20, 290, 22):
        p.circulo(x + rng.randrange(-6, 6), 196 + rng.randrange(-4, 8), 4, (250, 252, 255), borde=(110, 126, 160), g=1.5)
    nube(p, 150, 58, 2.6, NUBE_E, borde=(64, 70, 96), g=3)
    return p.imaxe()


@debuxo("arco", W, H)
def i_arco():
    p = Pincel(W, H)
    ceo(p, (110, 186, 250), (200, 232, 255))
    sol(p, 254, 46, 20)
    cores = [(232, 64, 64), (248, 152, 40), (250, 222, 64), (88, 196, 88), (72, 144, 232), (144, 88, 208)]
    for i, c in enumerate(cores):
        p.arco(150, 196, 126 - i * 9, math.pi, 2 * math.pi, c, g=9.5)
    chan(p, 184, (112, 196, 92))
    nube(p, 40, 170, 1.2, NUBE_B, BORDE_NUBE, g=2.5)
    for x, y in ((90, 120), (110, 150), (70, 140)):
        pinga(p, x, y, 0.9)
    return p.imaxe()


@debuxo("aurora", W, H)
def i_aurora():
    p = Pincel(W, H)
    ceo(p, (10, 16, 50), (42, 52, 110))
    rng = random.Random(4)
    for _ in range(30):
        p.circulo(rng.randrange(W), rng.randrange(120), rng.choice((1, 1.4, 2)), BRANCO, borde=None)
    for x in range(0, W, 2):
        y = 50 + math.sin(x / 26) * 18
        for k, c in enumerate(((60, 160, 120), (90, 236, 160), (150, 250, 200), (80, 200, 220), (60, 120, 160))):
            p.linha([(x, y + k * 10), (x, y + k * 10 + 10)], c, g=2.4)
    p.poli([(0, 220), (0, 170), (60, 140), (110, 168), (170, 132), (230, 162), (300, 140), (300, 220)], (226, 236, 250),
           borde=(150, 170, 210), g=2)
    casa_lateral(p, 230, 196, 1.1, (180, 70, 60))
    p.rect(236, 180, 6, 6, (255, 220, 100), borde=None)
    return p.imaxe()


@debuxo("vento", W, H)
def i_vento():
    p = Pincel(W, H)
    ceo(p)
    chan(p, 180, (118, 196, 96))
    p.linha_contorno([(246, 184), (240, 140), (226, 100)], TRONCO, g=10, gb=2)
    for dx, dy, r in ((206, 92, 26), (232, 76, 24), (214, 68, 20)):
        p.circulo(dx, dy, r, None, borde=(40, 100, 50), g=2.5)
    for dx, dy, r in ((206, 92, 26), (232, 76, 24), (214, 68, 20)):
        p.circulo(dx, dy, r, (82, 168, 80), borde=None)
    for y, x1, x2 in ((50, 14, 140), (96, 30, 168), (140, 10, 120)):
        pts = [(x1, y), (x2, y)] + [(x2 + math.cos(a) * 14, y - 14 + math.sin(a) * 14)
                                   for a in [math.pi / 2 - i * 0.5 for i in range(10)]]
        p.linha(pts, (90, 140, 210), g=8)
        p.linha(pts, BRANCO, g=4.5)
    for x, y, c in ((60, 70, (230, 140, 40)), (110, 120, (210, 90, 40)), (150, 60, (240, 180, 50)), (80, 160, (220, 120, 40))):
        p.poli([(x, y - 9), (x + 7, y), (x, y + 9), (x - 7, y)], c, borde=(140, 70, 30), g=1.5)
    return p.imaxe()


def _evaporacion(p, con_nube):
    ceo(p)
    sol(p, 46, 42, 22, cara=True)
    _lago(p, 168)
    for x in (110, 160, 210):
        pts = [(x + math.sin(t / 8) * 6, 160 - t) for t in range(0, 80, 4)]
        for k in range(0, len(pts) - 1, 2):
            p.linha([pts[k], pts[k + 1]], BRANCO, g=4)
        top = pts[-1]
        p.poli([(top[0] - 7, top[1] + 4), (top[0] + 7, top[1] + 4), (top[0], top[1] - 6)], BRANCO, borde=(120, 160, 210), g=1.2)
    if con_nube:
        nube(p, 228, 46, 1.4, NUBE_B, BORDE_NUBE, g=2.5)


@debuxo("nubes", W, H)
def i_nubes():
    p = Pincel(W, H)
    _evaporacion(p, True)
    return p.imaxe()


@debuxo("evaporacion", W, H)
def i_evap():
    p = Pincel(W, H)
    _evaporacion(p, False)
    return p.imaxe()


@debuxo("condensacion", W, H)
def i_cond():
    p = Pincel(W, H)
    ceo(p)
    _lago(p, 184)
    rng = random.Random(5)
    for _ in range(26):
        x, y = rng.randrange(40, 260), rng.randrange(100, 170)
        p.circulo(x, y, 2.5, BRANCO, borde=(150, 180, 220), g=1)
    for x in (90, 150, 210):
        p.linha([(x, 160), (x, 116)], BRANCO, g=4)
        p.poli([(x - 7, 116), (x + 7, 116), (x, 106)], BRANCO, borde=(120, 160, 210), g=1.2)
    nube(p, 150, 58, 2.4, NUBE_B, BORDE_NUBE, g=3)
    return p.imaxe()


@debuxo("treboada", W, H)
def i_treb():
    p = Pincel(W, H)
    ceo(p, (44, 50, 80), (96, 104, 130))
    chan(p, 186, (80, 130, 80))
    for x in range(30, 280, 26):
        p.linha([(x, 110), (x - 6, 130)], (150, 180, 230), g=2.5)
    lostrego(p, 140, 80, 2.2)
    nube(p, 150, 56, 2.6, NUBE_E, borde=(50, 56, 80), g=3)
    return p.imaxe()


@debuxo("terra", W, H)
def i_terra():
    p = Pincel(W, H)
    p.rect(0, 0, W, H, (12, 14, 40), borde=None)
    rng = random.Random(6)
    for _ in range(40):
        p.circulo(rng.randrange(W), rng.randrange(H), rng.choice((1, 1.5)), BRANCO, borde=None)
    p.circulo(130, 112, 86, (170, 220, 255), borde=None)
    p.circulo(130, 112, 80, (130, 196, 250), borde=None)
    p.circulo(130, 112, 72, (56, 120, 220), borde=(30, 70, 150), g=2)
    for cx, cy, r in ((106, 86, 22), (150, 132, 26), (120, 150, 14), (170, 80, 12), (90, 120, 10)):
        p.circulo(cx, cy, r, (86, 182, 96), borde=(50, 120, 60), g=1.5)
    for cx, cy in ((140, 70), (90, 140), (176, 112)):
        nube(p, cx, cy, 0.35, BRANCO, None)
    p.linha([(214, 60), (196, 74)], BRANCO, g=2.5)
    p.texto("ATMOSFERA", 250, 50, 14, BRANCO, borde=(12, 14, 40))
    return p.imaxe()


@debuxo("mapa", W, H)
def i_mapa():
    p = Pincel(W, H)
    p.rect(0, 0, W, H, (170, 220, 250), borde=None)
    p.poli([(40, 50), (120, 30), (220, 40), (270, 90), (250, 170), (160, 196), (70, 180), (30, 120)], (150, 210, 120),
           borde=(80, 140, 80), g=2.5)
    for nome, x, y in (("ic_soleado", 70, 70), ("ic_chuvia", 150, 50), ("ic_neve", 200, 110), ("ic_nubrado", 100, 120)):
        p.pegar(DEBUXOS[nome][0](), x, y, 64, 64)
    return p.imaxe()


# ---------------------------------------------------------------- instrumentos

def _fondo_instr(p):
    p.degradado(0, 0, W, H, (232, 242, 252), (206, 224, 244))
    p.elipse(150, 200, 110, 12, (190, 208, 230), borde=None)


@debuxo("termometro", W, H)
def i_termometro():
    p = Pincel(W, H)
    _fondo_instr(p)
    p.rect(136, 14, 28, 160, (252, 252, 255), radio=14, g=3)
    for i, n in enumerate(("40", "30", "20", "10", "0")):
        y = 34 + i * 28
        p.linha([(166, y), (180, y)], CONT, g=2)
        p.texto(n, 200, y, 14, CONT)
    p.rect(144, 70, 12, 120, (230, 60, 50), radio=6, borde=None)
    p.circulo(150, 186, 20, (230, 60, 50), g=3)
    p.circulo(144, 180, 5, (255, 150, 140), borde=None)
    p.texto("°C", 100, 60, 26, (230, 60, 50))
    return p.imaxe()


@debuxo("pluviometro", W, H)
def i_pluviometro():
    p = Pincel(W, H)
    _fondo_instr(p)
    for x, y in ((120, 18), (160, 10), (190, 26)):
        pinga(p, x, y, 1.1)
    p.rect(112, 74, 76, 120, (214, 236, 252), radio=8, g=3)
    p.rect(116, 134, 68, 56, (90, 160, 236), radio=6, borde=None)
    p.linha([(126, 138), (150, 138)], (190, 224, 255), g=3)
    p.poli([(90, 42), (210, 42), (168, 76), (132, 76)], (176, 186, 200), g=3)
    for y in range(90, 186, 16):
        p.linha([(188, y), (200, y)], CONT, g=2)
    p.texto("l/m²", 238, 120, 22, (50, 110, 190))
    return p.imaxe()


@debuxo("higrometro", W, H)
def i_higrometro():
    p = Pincel(W, H)
    _fondo_instr(p)
    p.circulo(150, 108, 84, (120, 150, 190), g=3)
    p.circulo(150, 108, 72, (252, 252, 255), borde=None)
    for k in range(11):
        a = math.pi * 0.8 + k * math.pi * 1.4 / 10
        c = mestura((240, 120, 60), (60, 140, 230), k / 10)
        p.linha([(150 + math.cos(a) * 58, 108 + math.sin(a) * 58), (150 + math.cos(a) * 68, 108 + math.sin(a) * 68)], c, g=4)
    a = math.pi * 0.8 + math.pi * 1.4 * 0.65
    p.linha_contorno([(150, 108), (150 + math.cos(a) * 54, 108 + math.sin(a) * 54)], (220, 60, 50), g=4, gb=1.5)
    p.circulo(150, 108, 7, CONT, borde=None)
    pinga(p, 150, 150, 2.0)
    p.texto("%", 112, 140, 26, (50, 110, 190))
    p.texto("HUMIDADE", 150, 74, 13, CONT)
    return p.imaxe()


@debuxo("anemometro", W, H)
def i_anemometro():
    p = Pincel(W, H)
    _fondo_instr(p)
    p.rect(145, 96, 10, 104, (150, 156, 170), radio=4, g=2.5)
    for k in range(3):
        a = -math.pi / 2 + k * 2 * math.pi / 3 + 0.4
        ex, ey = 150 + math.cos(a) * 80, 80 + math.sin(a) * 34
        p.linha_contorno([(150, 80), (ex, ey)], (170, 176, 190), g=5, gb=2)
        p.circulo(ex, ey, 17, (240, 120, 60), g=3)
        p.circulo(ex + 4, ey, 9, (180, 70, 40), borde=None)
    p.circulo(150, 80, 10, (200, 206, 220), g=2.5)
    for y in (30, 140):
        p.arco(150, 80, 110 if y == 30 else 104, -0.9 if y == 30 else 0.3, -0.4 if y == 30 else 0.8, (120, 170, 230), g=3)
    p.texto("m/s", 246, 186, 22, (50, 110, 190))
    return p.imaxe()


@debuxo("viravento", W, H)
def i_viravento():
    p = Pincel(W, H)
    _fondo_instr(p)
    p.rect(146, 92, 8, 110, (90, 90, 100), radio=3, g=2)
    p.linha_contorno([(84, 150), (216, 150)], (90, 90, 100), g=4, gb=1.5)
    p.linha_contorno([(150, 126), (150, 176)], (90, 90, 100), g=4, gb=1.5)
    for t, x, y in (("O", 70, 150), ("L", 230, 150), ("N", 150, 116), ("S", 150, 190)):
        p.texto(t, x, y, 18, (200, 60, 50), borde=BRANCO)
    p.poli([(70, 84), (220, 84), (220, 76), (240, 88), (220, 100), (220, 92), (70, 92)], (60, 60, 70), g=2)
    p.poli([(70, 76), (54, 70), (60, 88), (54, 106), (70, 100)], (60, 60, 70), g=2)
    # galo
    p.elipse(150, 62, 26, 16, (60, 60, 70), g=2)
    p.circulo(176, 44, 10, (60, 60, 70), g=2)
    p.poli([(172, 34), (176, 26), (180, 34), (184, 28), (186, 38)], (220, 60, 50), g=1.5)
    p.poli([(186, 44), (196, 47), (186, 50)], (240, 180, 50), g=1.5)
    p.poli([(124, 56), (104, 30), (116, 34), (112, 18), (132, 46)], (60, 60, 70), g=2)
    return p.imaxe()


@debuxo("barometro", W, H)
def i_barometro():
    p = Pincel(W, H)
    _fondo_instr(p)
    p.circulo(150, 108, 88, (176, 120, 70), g=3)
    p.circulo(150, 108, 74, (252, 248, 236), borde=(120, 80, 50), g=2)
    for k in range(9):
        a = math.pi * 0.75 + k * math.pi * 1.5 / 8
        p.linha([(150 + math.cos(a) * 60, 108 + math.sin(a) * 60), (150 + math.cos(a) * 70, 108 + math.sin(a) * 70)], CONT, g=2.5)
    for k, n in ((0, "960"), (4, "1000"), (8, "1040")):
        a = math.pi * 0.75 + k * math.pi * 1.5 / 8
        p.texto(n, 150 + math.cos(a) * 44, 108 + math.sin(a) * 44, 13, CONT)
    a = math.pi * 0.75 + math.pi * 1.5 * 0.6
    p.linha_contorno([(150, 108), (150 + math.cos(a) * 62, 108 + math.sin(a) * 62)], (40, 40, 50), g=4, gb=1)
    p.circulo(150, 108, 7, (200, 160, 60), g=2)
    p.texto("mb", 150, 150, 20, CONT)
    return p.imaxe()


# ---------------------------------------------------------------- factores climáticos

@debuxo("latitude", W, H)
def i_latitude():
    p = Pincel(W, H)
    p.rect(0, 0, W, H, (16, 20, 52), borde=None)
    p.circulo(330, 110, 70, SOL, borde=SOL_B, g=3)
    p.circulo(124, 110, 92, (56, 120, 220), borde=(30, 70, 150), g=2.5)
    for cx, cy, r in ((96, 80, 24), (150, 130, 28), (110, 154, 16), (160, 70, 14)):
        p.circulo(cx, cy, r, (86, 182, 96), borde=(50, 120, 60), g=1.5)
    p.elipse(124, 30, 40, 12, (240, 248, 255), borde=None)
    p.elipse(124, 192, 40, 12, (240, 248, 255), borde=None)
    p.linha([(32, 110), (216, 110)], (255, 226, 80), g=3)
    for y in (70, 110, 150):
        p.linha_contorno([(260, y), (224 if y == 110 else 210, y)], (255, 210, 60), g=4, gb=1)
    p.texto("CALOR", 124, 96, 20, (255, 160, 60), borde=(16, 20, 52))
    p.texto("FRÍO", 124, 52, 18, (170, 220, 255), borde=(16, 20, 52))
    p.texto("FRÍO", 124, 170, 18, (170, 220, 255), borde=(16, 20, 52))
    p.texto("Ecuador", 64, 122, 12, (255, 226, 80))
    return p.imaxe()


@debuxo("altitude", W, H)
def i_altitude():
    p = Pincel(W, H)
    ceo(p)
    montana(p, 150, 210, 300, 190, (150, 140, 128))
    for y, txt in ((200, "0 m · 20 °C"), (140, "1000 m · 10 °C"), (80, "2000 m · 0 °C")):
        p.linha([(4, y), (296, y)], (60, 80, 140), g=1.5)
        p.texto(txt, 66, y - 10, 13, (40, 50, 100), borde=BRANCO)
    p.texto("−1 °C cada 100 m", 226, 24, 15, (200, 50, 40), borde=BRANCO)
    return p.imaxe()


@debuxo("mar", W, H)
def i_mar():
    p = Pincel(W, H)
    ceo(p)
    sol(p, 150, 30, 14)
    p.poli([(0, 120), (90, 120), (110, 220), (0, 220)], (90, 160, 236), borde=(50, 110, 190), g=2)
    p.poli([(90, 120), (300, 110), (300, 220), (110, 220)], (126, 196, 100), borde=(70, 140, 60), g=2)
    p.poli([(90, 120), (104, 120), (124, 220), (110, 220)], (240, 220, 160), borde=None)
    casa_lateral(p, 150, 156, 0.9)
    for x in (236, 256, 276):
        p.rect(x - 8, 120, 16, 36, (220, 214, 200), g=1.5)
    p.texto("Clima máis suave", 90, 80, 14, (40, 120, 200), borde=BRANCO)
    p.texto("Clima máis extremo", 228, 92, 14, (220, 100, 40), borde=BRANCO)
    p.linha([(60, 150), (80, 150)], (190, 224, 255), g=3)
    return p.imaxe()


@debuxo("relevo", W, H)
def i_relevo():
    p = Pincel(W, H)
    ceo(p)
    chan(p, 190, (118, 196, 96))
    montana(p, 170, 196, 170, 150, (150, 140, 128))
    montana(p, 230, 196, 120, 100, (140, 132, 122), neve=False)
    nube(p, 60, 90, 1.3, NUBE_G, BORDE_NUBE, g=2.5)
    nube(p, 96, 110, 1.0, NUBE_G, BORDE_NUBE, g=2.5)
    for x in (40, 60, 80, 100):
        p.linha([(x, 124), (x - 4, 140)], AZUL_PINGA, g=2.5)
    p.linha_contorno([(4, 60), (60, 60)], (150, 200, 250), g=6, borde=(60, 100, 170), gb=1.5)
    p.poli([(60, 52), (74, 60), (60, 68)], (150, 200, 250), borde=(60, 100, 170), g=1.5)
    sol(p, 268, 48, 16)
    return p.imaxe()


@debuxo("climograma", W, H)
def i_climograma():
    p = Pincel(W, H)
    p.rect(10, 10, 280, 200, (255, 255, 255), radio=12, borde=(120, 140, 180), g=3)
    vals_p = [36, 34, 28, 44, 43, 29, 9, 7, 22, 47, 42, 55]
    vals_t = [5.7, 7.7, 10.4, 12.3, 16.4, 21.3, 25.4, 25.0, 20.8, 14.9, 9.5, 6.7]
    for i, v in enumerate(vals_p):
        p.rect(34 + i * 20, 190 - v * 2.6, 14, v * 2.6, (90, 150, 240), borde=(50, 100, 190), g=1.2)
    pts = [(41 + i * 20, 190 - v * 5.2) for i, v in enumerate(vals_t)]
    p.linha(pts, (220, 60, 50), g=3.5)
    for q in pts:
        p.circulo(q[0], q[1], 3.5, (220, 60, 50), borde=None)
    p.linha([(28, 30), (28, 192), (276, 192)], CONT, g=2.5)
    return p.imaxe()


# ---------------------------------------------------------------- paisaxes

@debuxo("paisaxe_oceanica", W, H)
def i_p_oceanica():
    p = Pincel(W, H)
    ceo(p, (150, 180, 214), (214, 230, 244))
    nube(p, 70, 40, 1.4, NUBE_B, BORDE_NUBE, g=2)
    nube(p, 230, 30, 1.2, NUBE_G, BORDE_NUBE, g=2)
    outeiro(p, 60, 200, 160, 80, (96, 180, 90))
    outeiro(p, 260, 210, 170, 90, (80, 166, 84))
    chan(p, 186, (110, 196, 96), (0, -4, 6, -2, 4))
    arbore_carballo(p, 70, 196, 1.2)
    arbore_faia(p, 150, 200, 1.0)
    arbore_carballo(p, 234, 202, 1.05, (64, 150, 76))
    casa_lateral(p, 190, 170, 0.7, (170, 70, 60))
    return p.imaxe()


@debuxo("paisaxe_montana", W, H)
def i_p_montana():
    p = Pincel(W, H)
    ceo(p, (110, 176, 246), (200, 230, 255))
    montana(p, 90, 200, 220, 170, (146, 136, 126))
    montana(p, 220, 200, 200, 140, (136, 128, 120))
    p.poli([(0, 220), (0, 180), (80, 168), (160, 186), (240, 172), (300, 182), (300, 220)], (150, 146, 130),
           borde=(100, 96, 86), g=2)
    for x, y in ((40, 186), (130, 190), (200, 186), (262, 192)):
        p.elipse(x, y, 16, 6, (110, 176, 90), borde=(60, 120, 60), g=1.5)
    matogueira(p, 90, 200, 0.9, (110, 150, 70), (240, 210, 80))
    matogueira(p, 230, 202, 0.8, (110, 150, 70), None)
    return p.imaxe()


@debuxo("paisaxe_mediterranea", W, H)
def i_p_med():
    p = Pincel(W, H)
    ceo(p, (90, 170, 250), (196, 230, 255))
    sol(p, 250, 40, 18)
    p.rect(0, 130, W, 18, (70, 150, 230), borde=None)
    outeiro(p, 80, 220, 170, 80, (222, 196, 120))
    outeiro(p, 250, 226, 170, 84, (210, 180, 104))
    chan(p, 190, (226, 200, 126), (0, -4, 4, -2, 2))
    arbore_pineiro(p, 70, 200, 1.3)
    arbore_acineira(p, 160, 196, 1.2)
    arbore_pineiro(p, 240, 204, 1.1)
    matogueira(p, 120, 206, 0.7, (150, 160, 90), None)
    return p.imaxe()


@debuxo("paisaxe_canaria", W, H)
def i_p_canaria():
    p = Pincel(W, H)
    ceo(p, (100, 180, 250), (200, 234, 255))
    p.rect(0, 140, W, 20, (60, 140, 220), borde=None)
    p.poli([(80, 150), (150, 40), (170, 40), (250, 150)], (150, 110, 90), borde=(100, 70, 60), g=2.5)
    p.poli([(140, 56), (150, 40), (170, 40), (180, 56), (166, 52), (156, 58)], (250, 252, 255), borde=None)
    chan(p, 176, (120, 100, 86), (0, -6, 4, -4, 2))
    arbore_drago(p, 90, 204, 1.2)
    arbore_palmeira(p, 210, 210, 1.2)
    arbore_palmeira(p, 260, 206, 0.9)
    return p.imaxe()


@debuxo("paisaxe_transicion", W, H)
def i_p_trans():
    p = Pincel(W, H)
    ceo(p, (130, 190, 250), (210, 236, 255))
    nube(p, 210, 40, 1.1, NUBE_B, BORDE_NUBE, g=2)
    chan(p, 150, (230, 206, 110), (0, -4, 2, -2, 0))
    for y in range(160, 220, 14):
        p.linha([(0, y), (300, y + 6)], (210, 180, 90), g=2)
    arbore_carballo(p, 70, 180, 1.0, (110, 160, 70))
    arbore_acineira(p, 150, 176, 1.1)
    arbore_pineiro(p, 236, 182, 1.0)
    return p.imaxe()


# ---------------------------------------------------------------- plantas (tarxetas)

def _planta(f, *args):
    p = Pincel(200, 200)
    p.elipse(100, 184, 70, 12, (200, 220, 170), borde=None)
    f(p, *args)
    return p.imaxe()


@debuxo("carballo", 200, 200)
def pl_carballo():
    return _planta(lambda p: arbore_carballo(p, 100, 186, 2.2))


@debuxo("faia", 200, 200)
def pl_faia():
    return _planta(lambda p: arbore_faia(p, 100, 186, 1.8))


@debuxo("pineiro", 200, 200)
def pl_pineiro():
    return _planta(lambda p: arbore_pineiro(p, 100, 186, 2.1))


@debuxo("acineira", 200, 200)
def pl_acineira():
    return _planta(lambda p: arbore_acineira(p, 100, 186, 2.5))


@debuxo("drago", 200, 200)
def pl_drago():
    return _planta(lambda p: arbore_drago(p, 100, 186, 2.2))


@debuxo("palmeira", 200, 200)
def pl_palmeira():
    return _planta(lambda p: arbore_palmeira(p, 100, 190, 1.75))


@debuxo("musgo", 200, 200)
def pl_musgo():
    def f(p):
        p.poli([(30, 186), (50, 120), (100, 96), (150, 112), (176, 186)], (150, 146, 140), borde=(100, 96, 90), g=3)
        for x, y, r in ((60, 130, 16), (90, 112, 18), (124, 116, 16), (150, 140, 14), (100, 140, 14), (70, 160, 12)):
            p.circulo(x, y, r, (110, 180, 80), borde=(60, 120, 50), g=2)
        for x, y in ((86, 106), (120, 112), (64, 126)):
            p.circulo(x, y, 4, (160, 220, 120), borde=None)
    return _planta(f)


@debuxo("matogueira", 200, 200)
def pl_matogueira():
    return _planta(lambda p: (matogueira(p, 70, 186, 2.2, (110, 150, 70), (240, 210, 80)),
                              matogueira(p, 136, 186, 2.6, (100, 140, 64), (220, 120, 200))))


# ---------------------------------------------------------------- outros

@debuxo("estacion", W, H)
def i_estacion():
    p = Pincel(W, H)
    ceo(p)
    chan(p, 176, (118, 196, 96))
    for x in (64, 104):
        p.linha([(x, 196), (x, 140)], (220, 220, 226), g=4)
    p.rect(48, 92, 72, 54, (252, 252, 255), radio=4, g=2.5)
    for y in range(100, 142, 8):
        p.linha([(54, y), (114, y)], (190, 196, 210), g=2)
    p.poli([(42, 94), (84, 76), (126, 94)], (240, 240, 246), g=2.5)
    p.rect(196, 40, 6, 156, (150, 156, 170), radio=3, g=2)
    for k in range(3):
        a = k * 2 * math.pi / 3
        ex, ey = 199 + math.cos(a) * 26, 40 + math.sin(a) * 8
        p.linha([(199, 40), (ex, ey)], (170, 176, 190), g=2.5)
        p.circulo(ex, ey, 6, (240, 120, 60), g=1.5)
    p.poli([(170, 70), (226, 70), (240, 76), (226, 82), (170, 82)], (60, 60, 70), g=1.5)
    p.rect(240, 140, 30, 44, (214, 236, 252), radio=4, g=2)
    p.poli([(232, 126), (278, 126), (262, 142), (248, 142)], (176, 186, 200), g=2)
    p.rect(140, 150, 40, 26, (60, 100, 180), g=2)
    p.linha([(160, 176), (160, 196)], (150, 156, 170), g=3)
    return p.imaxe()


@debuxo("satelite", W, H)
def i_satelite():
    p = Pincel(W, H)
    p.rect(0, 0, W, H, (12, 14, 40), borde=None)
    rng = random.Random(7)
    for _ in range(30):
        p.circulo(rng.randrange(W), rng.randrange(160), 1.2, BRANCO, borde=None)
    p.circulo(150, 430, 280, (56, 120, 220), borde=(150, 210, 255), g=4)
    p.circulo(90, 200, 40, (86, 182, 96), borde=None)
    p.circulo(210, 196, 34, (86, 182, 96), borde=None)
    for x in (48, 192):
        p.rect(x, 60, 60, 28, (60, 100, 200), g=2)
        for k in range(1, 4):
            p.linha([(x + k * 15, 60), (x + k * 15, 88)], (150, 190, 250), g=1.5)
    p.rect(116, 54, 68, 40, (232, 190, 60), radio=6, g=2.5)
    p.linha([(150, 94), (150, 112)], CONT, g=3)
    p.elipse(150, 116, 12, 5, (220, 220, 230), g=2)
    for r in (20, 34, 48):
        p.arco(150, 120, r, 0.3 * math.pi, 0.7 * math.pi, (255, 230, 120), g=3)
    return p.imaxe()


@debuxo("gps", W, H)
def i_gps():
    p = Pincel(W, H)
    p.rect(0, 0, W, H, (214, 236, 200), borde=None)
    for pts in (((0, 60), (300, 90)), ((80, 0), (130, 220)), ((0, 170), (300, 140)), ((220, 0), (200, 220))):
        p.linha(list(pts), (255, 255, 255), g=12)
        p.linha(list(pts), (250, 210, 120), g=4)
    p.circulo(70, 130, 22, (120, 200, 110), borde=(70, 150, 70), g=2)
    p.circulo(250, 50, 18, (120, 180, 240), borde=(60, 120, 200), g=2)
    p.poli([(150, 150), (126, 106), (128, 86), (150, 70), (172, 86), (174, 106)], (230, 60, 60), borde=(150, 30, 30), g=2.5)
    p.circulo(150, 92, 9, BRANCO, borde=None)
    p.elipse(150, 154, 16, 5, (0, 0, 0), borde=None)
    return p.imaxe()


@debuxo("fabrica", W, H)
def i_fabrica():
    p = Pincel(W, H)
    ceo(p, (200, 170, 150), (240, 214, 190))
    sol(p, 250, 40, 18)
    chan(p, 184, (150, 160, 110))
    for x, h in ((70, 110), (110, 90)):
        p.rect(x, 184 - h - 40, 22, h, (170, 90, 70), g=2.5)
        for k, (dx, dy, r) in enumerate(((0, -10, 14), (14, -30, 18), (34, -48, 22))):
            p.circulo(x + 11 + dx, 184 - h - 40 + dy, r, (120, 116, 120), borde=(80, 76, 84), g=2)
    p.rect(40, 130, 150, 56, (200, 120, 90), g=2.5)
    p.poli([(40, 130), (75, 110), (75, 130), (110, 110), (110, 130), (145, 110), (145, 130), (190, 130)], (180, 100, 74), g=2.5)
    for x in (56, 96, 136):
        p.rect(x, 146, 22, 18, (250, 220, 120), g=1.5)
    p.rect(214, 160, 56, 22, (220, 60, 60), radio=8, g=2)
    p.circulo(226, 184, 7, (50, 50, 60), g=1.5)
    p.circulo(258, 184, 7, (50, 50, 60), g=1.5)
    p.circulo(206, 172, 6, (150, 146, 150), borde=(90, 86, 94), g=1.5)
    return p.imaxe()
