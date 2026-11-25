"""O mapa do Val Verde (vista desde arriba, estilo ilustración infantil).
Úsano a ronda dos lumes, o mapa do tempo e os decorados dos menús."""
import random

import pygame

from config import TILE, HUD_ALTO, COLS, FILAS
from pincel import Pincel

# T = árbore, B = mato seco, g = prado, A = lago, M = rocha, N = neve, H = casa
MAPA = [
    "TTTTBTTTTTTTTgTTTTTTTTNNNNNNNNNN",
    "TTBTTTTTTTTTggTTTTTBTTMNNNNNNNNN",
    "TTTTTTBTTTTTgTTTTTTTTMMMNNNNNNMM",
    "TTTTTTTTTTTggTTTTTTTTMMMMMNNMMMM",
    "TBTTTTggggggggggggTTTTTMMMMMMMMT",
    "TTTTTggAAAAAAAgggggTBTTTTMMMMTTT",
    "TTTTgAAAAAAAAAAggHgTTTTBTTTTTTTT",
    "BTTTgAAAAAAAAAAAgggTTTTTTTTBTTTT",
    "TTTTgAAAAAAAAAAAgHgggTTTTTTTTTTT",
    "TTTTggAAAAAAAAAggggHgTTTBTTTTTBT",
    "TBTTTgggAAAAAAggTTggTTTTTTTTTTTT",
    "TTTTTTTgggggggggTTTTTTTBTTTTTTTT",
    "TTTBTTTTTTggTTTTTTBTTTTTTTBTTTTT",
    "TTTTTTTTTTTgTTTTTTTTTTTTTTTTTTTT",
    "TTBTTTTTTTTTTTTTTBTTTTTTTTTTTTTT",
    "TTTTTTTBTTTTTTTTTTTTTTBTTTTTTTTT",
]
assert len(MAPA) == FILAS and all(len(f) == COLS for f in MAPA), "o mapa debe ter 32x16 casas"

INFLAMABLES = "TB"


def rect_tile(c, r):
    return pygame.Rect(c * TILE, HUD_ALTO + r * TILE, TILE, TILE)


def centro_tile(c, r):
    return c * TILE + TILE // 2, HUD_ALTO + r * TILE + TILE // 2


def tile_en(x, y):
    c = min(COLS - 1, max(0, int(x // TILE)))
    r = min(FILAS - 1, max(0, int((y - HUD_ALTO) // TILE)))
    return c, r


_cache_chan = None


def crear_chan():
    """Chan do val: herba, prados, lago e montañas (sen árbores)."""
    global _cache_chan
    if _cache_chan is not None:
        return _cache_chan
    W, H = COLS * TILE, FILAS * TILE
    p = Pincel(W, H, ss=2)
    p.rect(0, 0, W, H, (128, 202, 98), borde=None)
    rng = random.Random(11)
    for _ in range(140):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        cor = rng.choice([(118, 192, 90), (138, 210, 104), (122, 198, 96)])
        p.elipse(x, y, rng.uniform(20, 60), rng.uniform(10, 26), cor, borde=None)
    centros = lambda ch: [(c * TILE + TILE / 2, r * TILE + TILE / 2, c, r)
                          for r in range(FILAS) for c in range(COLS) if MAPA[r][c] in ch]
    for x, y, c, r in centros("gH"):
        p.circulo(x, y, 27, (156, 218, 112), borde=None)
    for x, y, c, r in centros("g"):
        for _ in range(2):
            fx, fy = x + rng.uniform(-16, 16), y + rng.uniform(-16, 16)
            col = rng.choice([(255, 255, 255), (255, 140, 160), (255, 220, 90), (180, 160, 255)])
            for dx, dy in ((-2.5, 0), (2.5, 0), (0, -2.5), (0, 2.5)):
                p.circulo(fx + dx, fy + dy, 2, col, borde=None)
            p.circulo(fx, fy, 1.6, (240, 170, 40), borde=None)
    # lago
    auga = centros("A")
    for x, y, c, r in auga:
        p.circulo(x, y, 36, (236, 220, 164), borde=None)
    for x, y, c, r in auga:
        p.circulo(x, y, 30, (100, 172, 238), borde=None)
    for x, y, c, r in auga:
        if all(0 <= r + dr < FILAS and 0 <= c + dc < COLS and MAPA[r + dr][c + dc] == "A"
               for dc in (-1, 0, 1) for dr in (-1, 0, 1)):
            p.circulo(x, y, 30, (82, 154, 230), borde=None)
    # montañas
    for x, y, c, r in centros("MN"):
        p.circulo(x, y, 30, (176, 166, 148), borde=None)
    from arte import montana
    for x, y, c, r in sorted(centros("MN"), key=lambda q: q[1]):
        montana(p, x + rng.uniform(-6, 6), y + 26, 78, rng.uniform(56, 76), (156, 146, 134), neve=MAPA[r][c] == "N")
    _cache_chan = p.imaxe()
    return _cache_chan


def debuxar_vexetacion(arte, grid, surf=None):
    """Capa coas árbores, o mato, as casas e o queimado (depende do estado do lume)."""
    W, H = COLS * TILE, FILAS * TILE
    s = surf or pygame.Surface((W, H), pygame.SRCALPHA)
    if surf is None:
        pass
    else:
        s.fill((0, 0, 0, 0))
    for r in range(FILAS):
        for c in range(COLS):
            ch = grid[r][c]
            x, y = c * TILE + TILE // 2, r * TILE + TILE // 2
            v = (c * 7 + r * 13) % 3
            ox = ((c * 31 + r * 17) % 9) - 4
            if ch == "T":
                s.blit(arte.imaxe(f"arbore{v}"), (x - 28 + ox, y - 44))
            elif ch == "B":
                s.blit(arte.imaxe("mato"), (x - 22 + ox, y - 22))
            elif ch == "Q":
                s.blit(arte.imaxe("queimado"), (x - 24, y - 16))
            elif ch == "H":
                s.blit(arte.imaxe("casa"), (x - 31, y - 40))
    return s


_cache_completo = None


def crear_fondo(arte):
    """Val completo (chan + vexetación), para decorados."""
    global _cache_completo
    if _cache_completo is None:
        f = crear_chan().copy()
        f.blit(debuxar_vexetacion(arte, MAPA), (0, 0))
        _cache_completo = f
    return _cache_completo


class Decorado:
    """O mapa do val cun veo escuro, para detrás de menús e diálogos."""

    def __init__(self, arte, alfa=110):
        self.mapa = crear_fondo(arte)
        self.veo = pygame.Surface(self.mapa.get_size(), pygame.SRCALPHA)
        self.veo.fill((16, 24, 64, alfa))

    def draw(self, s):
        s.fill((40, 80, 56))
        s.blit(self.mapa, (0, HUD_ALTO))
        s.blit(self.veo, (0, HUD_ALTO))
        pygame.draw.rect(s, (40, 80, 56), (0, 0, s.get_width(), HUD_ALTO))
        s.blit(self.veo, (0, HUD_ALTO - self.veo.get_height()))
