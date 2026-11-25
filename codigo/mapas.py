"""Mapas simplificados para os retos: España (climas), Galicia (variedades do
clima oceánico), globo terráqueo (zonas climáticas) e montaña (altitude).

Cada función devolve (imaxe, ancoras), onde 'ancoras' son os puntos
(en píxeles da imaxe) onde van os ocos para arrastrar as tarxetas.
Os mapas son simplificados para 4º de Primaria.
"""
import math

import pygame

from pincel import Pincel, CONT, escurecer

CORES_CLIMA = {
    "oceanico": (96, 184, 104),
    "continental": (250, 214, 84),
    "contmed": (252, 238, 160),
    "mediterraneo": (244, 160, 76),
    "montana": (156, 116, 200),
    "subtropical": (236, 120, 176),
}
MAR = (176, 218, 248)
TERRA_VECIÑA = (234, 228, 212)

# Contorno da España peninsular (lonxitude, latitude), sentido horario desde a desembocadura do Miño
COSTA_NORTE_OESTE = [(-8.87, 41.87), (-8.9, 42.1), (-8.75, 42.25), (-8.95, 42.35), (-8.85, 42.5), (-9.05, 42.55),
                     (-9.0, 42.75), (-9.3, 42.9), (-9.25, 43.1), (-9.0, 43.2), (-8.6, 43.3), (-8.4, 43.37), (-8.2, 43.45),
                     (-8.3, 43.55), (-8.0, 43.7), (-7.7, 43.78), (-7.4, 43.7), (-7.05, 43.55)]
ESPANA = COSTA_NORTE_OESTE + [
    (-5.8, 43.6), (-4.5, 43.4), (-3.8, 43.47), (-3.0, 43.35), (-1.8, 43.38), (-1.4, 43.05), (-0.7, 42.85),
    (0.7, 42.8), (1.7, 42.5), (3.2, 42.4), (3.2, 41.9), (2.2, 41.4), (1.0, 41.05), (0.8, 40.7), (-0.1, 40.0),
    (-0.3, 39.45), (0.2, 38.75), (-0.5, 38.3), (-0.75, 37.6), (-1.6, 37.3), (-2.0, 36.75), (-2.9, 36.75),
    (-4.4, 36.7), (-5.35, 36.15), (-6.0, 36.3), (-6.3, 36.55), (-6.4, 36.8), (-7.4, 37.2)]
FRONTEIRA_PT = [(-7.4, 37.2), (-7.5, 37.6), (-7.25, 38.2), (-7.0, 38.85), (-7.3, 39.5), (-6.9, 40.25), (-6.8, 41.0),
                (-6.2, 41.6), (-6.6, 41.95), (-7.2, 41.9), (-7.6, 41.86), (-8.05, 41.82), (-8.2, 42.12), (-8.65, 42.0)]
ESPANA = ESPANA + FRONTEIRA_PT
PORTUGAL = [(-8.87, 41.87), (-8.65, 40.6), (-9.5, 38.8), (-8.8, 37.0), (-7.4, 37.2)] + FRONTEIRA_PT[1:] + [(-8.87, 41.87)]
FRANCIA = [(-1.8, 43.38), (-1.4, 43.05), (-0.7, 42.85), (0.7, 42.8), (1.7, 42.5), (3.2, 42.4), (3.5, 43.3),
           (4.8, 43.4), (5.2, 44.6), (-1.6, 44.6)]
AFRICA = [(-6.5, 35.8), (-5.9, 35.8), (-5.3, 35.9), (-4.0, 35.2), (-2.0, 35.1), (0.0, 35.8), (2.0, 36.6),
          (5.0, 36.9), (5.0, 34.0), (-7.0, 34.0)]
BALEARES = [(2.95, 39.62, 0.45, 0.28), (4.1, 39.97, 0.24, 0.1), (1.42, 39.0, 0.18, 0.14), (1.45, 38.7, 0.07, 0.05)]
CANARIAS = [(-13.62, 29.05, 0.18, 0.28), (-14.05, 28.4, 0.22, 0.42), (-15.6, 27.95, 0.24, 0.22),
            (-16.6, 28.27, 0.34, 0.2), (-17.22, 28.1, 0.12, 0.1), (-17.86, 28.67, 0.12, 0.24), (-18.0, 27.75, 0.15, 0.08)]


def _dist_polilinea(lon, lat, pts, lat_ref=40):
    c = math.cos(math.radians(lat_ref))
    mellor = 99.0
    px, py = lon * c, lat
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        ax, ay, bx, by = x1 * c, y1, x2 * c, y2
        dx, dy = bx - ax, by - ay
        t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
        mellor = min(mellor, math.hypot(px - ax - t * dx, py - ay - t * dy))
    return mellor


def _elipse(lon, lat, clon, clat, rlon, rlat, ang=0.0):
    ca, sa = math.cos(ang), math.sin(ang)
    x, y = lon - clon, lat - clat
    u, v = x * ca + y * sa, -x * sa + y * ca
    return (u / rlon) ** 2 + (v / rlat) ** 2 < 1


# costa mediterránea (do cabo de Creus a Gibraltar) e costa de Huelva-Cádiz
_COSTA_MED = [(3.2, 42.4), (3.2, 41.9), (2.2, 41.4), (1.0, 41.05), (0.8, 40.7), (-0.1, 40.0), (-0.3, 39.45), (0.2, 38.75),
              (-0.5, 38.3), (-0.75, 37.6), (-1.6, 37.3), (-2.0, 36.75), (-2.9, 36.75), (-4.4, 36.7), (-5.35, 36.15),
              (-6.0, 36.3), (-6.3, 36.55), (-6.4, 36.8), (-7.4, 37.2)]


def clima_espana(lon, lat):
    onda = 0.08 * math.sin(lon * 3.1) + 0.06 * math.sin(lat * 5.3)
    if _elipse(lon, lat, 0.5, 42.7, 2.4, 0.36 + onda, 0.05):
        return "montana"          # Pireneos
    if _elipse(lon, lat, -5.3, 42.98, 1.8, 0.17 + onda / 2):
        return "montana"          # Cordilleira Cantábrica
    if _elipse(lon, lat, -4.4, 40.4, 1.5, 0.26 + onda, 0.25):
        return "montana"          # Sistema Central
    if _elipse(lon, lat, -2.2, 41.3, 0.5 + onda, 0.85, -0.5):
        return "montana"          # Sistema Ibérico
    if _elipse(lon, lat, -3.2, 37.08, 0.6, 0.17):
        return "montana"          # Serra Nevada
    if _elipse(lon, lat, -6.55, 42.55, 0.35, 0.3):
        return "montana"          # montañas de León
    if (lat > 42.72 + onda and lon < -1.6) or (lon < -6.9 and lat > 41.8):
        return "oceanico"
    if _dist_polilinea(lon, lat, _COSTA_MED) < 0.5 + onda:
        return "mediterraneo"
    if lat < 39.45 + 0.25 * math.sin(lon * 1.7):
        return "contmed"
    return "continental"


class Proxeccion:
    def __init__(self, lon0, lon1, lat0, lat1, w, h, marxe=10, lat_ref=40):
        c = math.cos(math.radians(lat_ref))
        self.c = c
        self.s = min((w - 2 * marxe) / ((lon1 - lon0) * c), (h - 2 * marxe) / (lat1 - lat0))
        self.lon0, self.lat1 = lon0, lat1
        self.ox = (w - (lon1 - lon0) * c * self.s) / 2
        self.oy = (h - (lat1 - lat0) * self.s) / 2

    def __call__(self, lon, lat):
        return (self.ox + (lon - self.lon0) * self.c * self.s, self.oy + (self.lat1 - lat) * self.s)

    def inversa(self, x, y):
        return (self.lon0 + (x - self.ox) / (self.c * self.s), self.lat1 - (y - self.oy) / self.s)


def _rexions(w, h, prox, clasificar, cores, paso=3):
    """Imaxe de cores por rexión: calcúlase en baixa resolución e amplíase suavizada."""
    bw, bh = max(1, w // paso), max(1, h // paso)
    baixa = pygame.Surface((bw, bh))
    for yy in range(bh):
        for xx in range(bw):
            lon, lat = prox.inversa(xx * paso + paso / 2, yy * paso + paso / 2)
            baixa.set_at((xx, yy), cores[clasificar(lon, lat)])
    return pygame.transform.smoothscale(baixa, (w, h))


def _mascara(w, h, poligonos, elipses=(), ss=2):
    m = pygame.Surface((w * ss, h * ss), pygame.SRCALPHA)
    for pol in poligonos:
        pygame.draw.polygon(m, (255, 255, 255, 255), [(x * ss, y * ss) for x, y in pol])
    for cx, cy, rx, ry in elipses:
        pygame.draw.ellipse(m, (255, 255, 255, 255), ((cx - rx) * ss, (cy - ry) * ss, 2 * rx * ss, 2 * ry * ss))
    return pygame.transform.smoothscale(m, (w, h))


def _aplicar(cores, mascara):
    s = pygame.Surface(cores.get_size(), pygame.SRCALPHA)
    s.blit(cores, (0, 0))
    s.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    return s


# ================================================================ ESPAÑA

def mapa_espana(w=860, h=600):
    prox = Proxeccion(-9.8, 4.7, 35.4, 44.2, w, h)
    p = Pincel(w, h, ss=2)
    p.degradado(0, 0, w, h, MAR, (150, 200, 240))
    for pol in (PORTUGAL, FRANCIA, AFRICA):
        p.poli([prox(*q) for q in pol], TERRA_VECIÑA, borde=(170, 160, 140), g=1.5)
    fondo = p.imaxe()

    pen = [prox(*q) for q in ESPANA]
    elips = []
    for lon, lat, rx, ry in BALEARES:
        x, y = prox(lon, lat)
        elips.append((x, y, rx * prox.c * prox.s, ry * prox.s))
    cores = _rexions(w, h, prox, lambda lo, la: "mediterraneo" if lo > 1.2 and la < 40.3 else clima_espana(lo, la),
                     CORES_CLIMA)
    terra = _aplicar(cores, _mascara(w, h, [pen], elips))
    fondo.blit(terra, (0, 0))

    q = Pincel(w, h, ss=2)
    q.linha(pen, CONT, g=2.5, pechar=True)
    for x, y, rx, ry in elips:
        pygame.draw.ellipse(q.s, CONT, q._re(x, y, rx, ry), q.R(2.2))
    # recadro das Canarias
    bx, by, bw, bh = 12, h - 150, 250, 136
    q.rect(bx, by, bw, bh, None, radio=8, borde=CONT, g=2)
    fondo.blit(q.imaxe(), (0, 0))
    pygame.draw.rect(fondo, MAR, (bx + 2, by + 2, bw - 4, bh - 4), border_radius=6)
    pc = Proxeccion(-18.4, -13.2, 27.5, 29.5, bw, bh, marxe=14, lat_ref=28.5)
    r = Pincel(bw, bh, ss=3)
    for lon, lat, rx, ry in CANARIAS:
        x, y = pc(lon, lat)
        r.elipse(x, y, rx * pc.c * pc.s, ry * pc.s, CORES_CLIMA["subtropical"], borde=CONT, g=1.6)
    fondo.blit(r.imaxe(), (bx, by))

    anc = {}
    for clave, (lon, lat) in {"oceanico": (-7.9, 42.95), "continental": (-4.6, 41.7), "contmed": (-3.6, 38.9),
                              "mediterraneo": (-0.45, 39.3), "montana": (0.4, 42.62)}.items():
        anc[clave] = tuple(round(v) for v in prox(lon, lat))
    anc["subtropical"] = (bx + bw // 2, by + bh // 2)
    return fondo, anc


# ================================================================ GALICIA

GALICIA = COSTA_NORTE_OESTE + [(-7.0, 43.4), (-6.85, 43.1), (-6.85, 42.85), (-6.8, 42.5), (-6.85, 42.25),
                               (-7.0, 42.05), (-7.2, 41.9), (-7.6, 41.86), (-8.05, 41.82), (-8.2, 42.12), (-8.65, 42.0)]
CIDADES = {"A Coruña": (-8.41, 43.36), "Ferrol": (-8.23, 43.48), "Santiago": (-8.54, 42.88),
           "Pontevedra": (-8.64, 42.43), "Vigo": (-8.72, 42.24), "Lugo": (-7.56, 43.01), "Ourense": (-7.86, 42.34)}


_LIMITE_TERRA = [(-7.05, 43.55), (-7.0, 43.4), (-6.85, 43.1), (-6.85, 42.85), (-6.8, 42.5), (-6.85, 42.25), (-7.0, 42.05),
                 (-7.2, 41.9), (-7.6, 41.86), (-8.05, 41.82), (-8.2, 42.12)]


def clima_galicia(lon, lat):
    onda = 0.05 * math.sin(lon * 9 + lat * 4) + 0.04 * math.sin(lat * 13)
    if _dist_polilinea(lon, lat, COSTA_NORTE_OESTE, 43) < 0.33 + onda:
        return "litoral"
    if _dist_polilinea(lon, lat, _LIMITE_TERRA, 43) < 0.3 + onda * 1.5:
        return "montana"
    return "interior"


CORES_GALICIA = {"litoral": (150, 214, 130), "interior": (56, 150, 84), "montana": (176, 140, 210)}


def mapa_galicia(w=640, h=600):
    prox = Proxeccion(-9.45, -6.6, 41.7, 43.9, w, h, lat_ref=42.8)
    p = Pincel(w, h, ss=2)
    p.degradado(0, 0, w, h, MAR, (150, 200, 240))
    p.poli([prox(*q) for q in [(-6.85, 43.6), (-5.5, 43.6), (-5.5, 41.6), (-8.05, 41.82), (-7.6, 41.86), (-7.2, 41.9),
                                (-7.0, 42.05), (-6.85, 42.25), (-6.8, 42.5), (-6.85, 42.85), (-6.85, 43.1), (-7.0, 43.4),
                                (-7.05, 43.55)]], TERRA_VECIÑA, borde=(170, 160, 140), g=1.5)
    p.poli([prox(*q) for q in [(-8.87, 41.87), (-8.65, 42.0), (-8.2, 42.12), (-8.05, 41.82), (-8.05, 41.6), (-9.0, 41.6)]],
           TERRA_VECIÑA, borde=(170, 160, 140), g=1.5)
    fondo = p.imaxe()
    pol = [prox(*q) for q in GALICIA]
    cores = _rexions(w, h, prox, clima_galicia, CORES_GALICIA, paso=4)
    fondo.blit(_aplicar(cores, _mascara(w, h, [pol])), (0, 0))
    q = Pincel(w, h, ss=2)
    q.linha(pol, CONT, g=2.5, pechar=True)
    for nome, (lon, lat) in CIDADES.items():
        x, y = prox(lon, lat)
        q.circulo(x, y, 5, (255, 255, 255), borde=CONT, g=2)
        q.texto(nome, x + (-8 if nome in ("Vigo", "Pontevedra") else 8), y + 14, 15, CONT, centro=False, borde=(255, 255, 255))
    fondo.blit(q.imaxe(), (0, 0))
    anc = {k: tuple(round(v) for v in prox(lon, lat))
           for k, (lon, lat) in {"litoral": (-8.95, 43.05), "interior": (-7.85, 42.75), "montana": (-7.05, 42.55)}.items()}
    return fondo, anc


# ================================================================ GLOBO (zonas climáticas)

ZONAS = [(66.5, 90, (204, 230, 252)), (23.5, 66.5, (150, 210, 120)), (-23.5, 23.5, (250, 190, 90)),
         (-66.5, -23.5, (150, 210, 120)), (-90, -66.5, (204, 230, 252))]


def globo_zonas(w=640, h=600):
    p = Pincel(w, h, ss=2)
    cx, cy = w * 0.34, h / 2
    R = min(w, h) * 0.4
    p.circulo(cx, cy, R, (30, 40, 80), borde=None)
    capa = Pincel(w, h, ss=2)
    for lat0, lat1, cor in ZONAS:
        y0 = cy - R * math.sin(math.radians(lat1))
        y1 = cy - R * math.sin(math.radians(lat0))
        capa.rect(0, y0, w, y1 - y0, cor, borde=None)
    mascara = Pincel(w, h, ss=2)
    mascara.circulo(cx, cy, R, (255, 255, 255), borde=None)
    capa.s.blit(mascara.s, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    p.s.blit(capa.s, (0, 0))
    for lat, nome in ((66.5, "Círculo polar ártico"), (23.5, "Trópico de Cáncer"), (0, "Ecuador"),
                      (-23.5, "Trópico de Capricornio"), (-66.5, "Círculo polar antártico")):
        y = cy - R * math.sin(math.radians(lat))
        dx = R * math.cos(math.radians(lat))
        g = 3 if lat == 0 else 2
        for k in range(0, int(2 * dx), 16):
            p.linha([(cx - dx + k, y), (cx - dx + min(k + 9, 2 * dx), y)], (60, 70, 120) if lat else (200, 60, 50), g=g)
        p.texto(nome, cx + R + 10, y - 9, 14, (40, 50, 100), centro=False, borde=(255, 255, 255))
    p.aro(cx, cy, R, CONT, g=3)
    def punto(lat, frac):
        y = cy - R * math.sin(math.radians(lat))
        return (round(cx + frac * R * math.cos(math.radians(lat))), round(y))
    anc = {"fria_n": punto(78, 0.25), "temp_n": punto(48, 0.3), "calida": punto(0, 0.3),
           "temp_s": punto(-45, 0.3), "fria_s": punto(-78, 0.25), "espana": punto(40, -0.55)}
    return p.imaxe(), anc


# ================================================================ MONTAÑA (altitude)

def montana_altitude(w=860, h=600):
    p = Pincel(w, h, ss=2)
    p.degradado(0, 0, w, h, (120, 186, 250), (214, 238, 255))
    base, cume = h - 40, 70
    p.poli([(0, base), (w * 0.62, cume), (w, base * 0.7), (w, h), (0, h)], (150, 140, 128), borde=escurecer((150, 140, 128), 0.6), g=3)
    p.poli([(w * 0.62, cume), (w, base * 0.7), (w, h), (w * 0.62, h)], (134, 126, 116), borde=None)
    p.poli([(w * 0.53, cume + 70), (w * 0.62, cume), (w * 0.72, cume + 60), (w * 0.66, cume + 54), (w * 0.6, cume + 76)],
           (250, 252, 255), borde=(170, 190, 220), g=1.5)
    p.rect(0, base, w, h - base, (118, 196, 96), borde=None)
    anc = {}
    for i, alt in enumerate((0, 500, 1000, 1500, 2000)):
        y = base - i * (base - cume - 40) / 4
        for k in range(0, w, 22):
            p.linha([(k, y), (k + 12, y)], (40, 60, 120), g=2)
        p.rect(14, y - 18, 110, 36, (255, 255, 255), radio=10, borde=(40, 60, 120), g=2)
        p.texto(f"{alt} m", 69, y, 20, (40, 60, 120))
        anc[f"m{alt}"] = (round(w * 0.28 + i * w * 0.07), round(y))
    x0, y0 = anc["m0"]
    p.rect(x0 - 60, y0 - 26, 120, 52, (255, 238, 200), radio=14, borde=(200, 90, 40), g=3)
    p.texto("20 °C", x0, y0, 26, (200, 60, 40))
    return p.imaxe(), anc
