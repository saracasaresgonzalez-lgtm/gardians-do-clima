"""Elementos táctiles: botóns grandes, veos, avisos e cabeceira."""
import pygame

import texto as tx
from config import ANCHO, ALTO, C
from pincel import escurecer, aclarar

_velos = {}


def pantalla_completa():
    """Activa ou desactiva a pantalla completa (no ordenador e no navegador)."""
    from config import WEB
    try:
        if WEB:
            import platform
            doc = platform.window.document
            if doc.fullscreenElement:
                doc.exitFullscreen()
            else:
                doc.documentElement.requestFullscreen()
        else:
            pygame.display.toggle_fullscreen()
    except Exception:
        pass


def velo(s, alfa=140, cor=(14, 20, 50)):
    clave = (alfa, cor)
    if clave not in _velos:
        v = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        v.fill((*cor, alfa))
        _velos[clave] = v
    s.blit(_velos[clave], (0, 0))


class Boton:
    """Botón grande para tocar. Actívase ao tocalo."""

    def __init__(self, rect, texto, cor=C.BOTON, icona=None, fonte="m"):
        self.rect = pygame.Rect(rect)
        self.texto = texto
        self.cor = cor
        self.icona = icona
        self.fonte = fonte
        self.visible = True

    def tocado(self, ent):
        return self.visible and ent.clic is not None and self.rect.collidepoint(ent.clic)

    def debuxar(self, s, j, cor=None):
        if not self.visible:
            return
        cor = cor or self.cor
        ent = j.entrada
        baixo = ent.premido and self.rect.collidepoint(ent.pos)
        r = self.rect.move(0, 4 if baixo else 0)
        rad = min(22, r.h // 2)
        if not baixo:
            pygame.draw.rect(s, escurecer(cor, 0.55), self.rect.move(0, 6), border_radius=rad)
        pygame.draw.rect(s, escurecer(cor, 0.7), r, border_radius=rad)
        pygame.draw.rect(s, cor, r.inflate(-6, -6), border_radius=rad - 3)
        pygame.draw.rect(s, aclarar(cor, 0.18), (r.x + 6, r.y + 5, r.w - 12, (r.h - 10) // 2), border_radius=rad - 4)

        x0, ancho = r.x + 16, r.w - 32
        if self.icona is not None:
            s.blit(self.icona, (r.x + 14, r.centery - self.icona.get_height() // 2))
            x0 += self.icona.get_width() + 10
            ancho -= self.icona.get_width() + 10
        if not self.texto:
            return
        f = {"m": j.fuentes.m, "p": j.fuentes.p, "g": j.fuentes.g}[self.fonte]
        lineas = tx.envolver(f, self.texto, ancho)
        if len(lineas) > 1 and self.fonte != "p":
            f = j.fuentes.p
            lineas = tx.envolver(f, self.texto, ancho)
        lh = f.get_linesize()
        y = r.centery - len(lineas) * lh // 2
        for i, l in enumerate(lineas):
            x = x0 + (ancho - f.size(l)[0]) // 2
            tx.texto(s, f, l, (x, y + i * lh), C.BLANCO, escurecer(cor, 0.5))


def aviso(s, j, txt, bo, arriba=True):
    """Caixa coa explicación (verde se acertou, vermella se non). Por defecto tapa a cabeceira."""
    f = j.fuentes.m
    lineas = tx.envolver(f, txt, ANCHO - 200)
    lh = f.get_linesize()
    h = max(96 if arriba else 0, 24 + len(lineas) * lh)
    y = 2 if arriba else ALTO - h - 8
    cor = C.OK if bo else C.ERRO
    tx.caja(s, (8, y, ANCHO - 16, h), borde=cor, g=5)
    retrato = j.arte.imaxe("retrato_brisa", 72, 72)
    s.blit(retrato, (24, y + (h - 72) // 2))
    y_txt = y + (h - len(lineas) * lh) // 2
    for i, l in enumerate(lineas):
        tx.texto(s, f, l, (112, y_txt + i * lh), cor)


class BotonsEsquina:
    """Botóns da esquina para a mestra: pantalla completa e (opcional) volver ao inicio."""

    def __init__(self, j, casa=True, y=18):
        self.j = j
        self.casa = pygame.Rect(ANCHO - 70, y, 56, 56) if casa else None
        self.pantalla = pygame.Rect(ANCHO - (134 if casa else 70), y, 56, 56)

    def update(self):
        ent = self.j.entrada
        if ent.clic and self.pantalla.collidepoint(ent.clic):
            pantalla_completa()
            return True
        if ent.clic and self.casa and self.casa.collidepoint(ent.clic):
            self.j.ir_inicio()
            return True
        return False

    def draw(self, s):
        for r in (self.pantalla, self.casa):
            if r:
                pygame.draw.rect(s, (30, 44, 90), r, border_radius=12)
                pygame.draw.rect(s, C.HUD_BORDE, r, 3, border_radius=12)
        p = self.pantalla
        for (x, y, dx, dy) in ((p.x + 13, p.y + 13, 1, 1), (p.right - 14, p.y + 13, -1, 1),
                               (p.x + 13, p.bottom - 14, 1, -1), (p.right - 14, p.bottom - 14, -1, -1)):
            pygame.draw.line(s, C.BLANCO, (x, y), (x + 10 * dx, y), 4)
            pygame.draw.line(s, C.BLANCO, (x, y), (x, y + 10 * dy), 4)
        if self.casa:
            c = self.casa
            pygame.draw.polygon(s, C.BLANCO, [(c.centerx, c.y + 11), (c.x + 11, c.y + 28), (c.right - 11, c.y + 28)])
            pygame.draw.rect(s, C.BLANCO, (c.x + 17, c.y + 28, c.w - 34, 16))
            pygame.draw.rect(s, (30, 44, 90), (c.centerx - 4, c.y + 34, 8, 10))


def cabeceira(s, j, titulo, instrucion):
    pygame.draw.rect(s, C.HUD, (0, 0, ANCHO, 96))
    pygame.draw.rect(s, C.HUD_BORDE, (0, 92, ANCHO, 4))
    tx.texto(s, j.fuentes.g, titulo, (24, 8), C.AMARILLO, (20, 28, 60))
    tx.texto(s, j.fuentes.m, instrucion, (24, 56), C.BLANCO, (20, 28, 60))
