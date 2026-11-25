"""Retos táctiles sobre os contidos:
- EscenaClasificar: arrastrar tarxetas ás caixas.
- EscenaOrdenar: arrastrar os pasos aos ocos 1, 2, 3.
- EscenaUnir: trazar frechas entre conceptos e explicacións.
- EscenaColocar: arrastrar tarxetas ao seu lugar nun mapa ou debuxo.
- EscenaMapaTempo: colocar símbolos no mapa do tempo segundo a predición.
- EscenaQuiz: serie de preguntas.
- EscenaClimograma: ler, completar e comparar climogramas.

En todos se pode arrastrar OU tocar a tarxeta e despois o destino.
Cada reto chama a al_terminar({"acertos": n, "erros": n}).
"""
import math
import random

import pygame

import datos
import mapas
import texto as tx
import ui
from config import ANCHO, ALTO, HUD_ALTO, C
from mapa import Decorado, crear_fondo, centro_tile
from pincel import escurecer, aclarar
from preguntas import PanelPregunta, Banco

PAPEL = (255, 251, 238)


def imaxe_de(j, clave, w, h):
    """Busca primeiro o símbolo (ic_) e despois a ilustración."""
    nome = "ic_" + clave if j.arte.existe("ic_" + clave) else clave
    return j.arte.encaixar(nome, w, h)


# ================================================================ base


class Tarxeta:
    def __init__(self, rect, texto, clave, pista="", imaxe=None, titulo=None):
        self.casa = pygame.Rect(rect)
        self.rect = self.casa.copy()
        self.pos = [float(self.rect.x), float(self.rect.y)]
        self.texto, self.clave, self.pista = texto, clave, pista
        self.imaxe, self.titulo = imaxe, titulo
        self.colocada = False
        self.erro_t = 0.0

    def volver(self, dt):
        self.pos[0] += (self.casa.x - self.pos[0]) * min(1, dt * 12)
        self.pos[1] += (self.casa.y - self.pos[1]) * min(1, dt * 12)
        self.rect.topleft = (round(self.pos[0]), round(self.pos[1]))


def debuxar_tarxeta(s, j, t, seleccionada=False):
    r = t.rect
    borde = C.ERRO if t.erro_t > 0 else (C.NARANJA if seleccionada else C.CAJA_BORDE)
    tx.caja(s, r, fondo=PAPEL, borde=borde, radio=14, g=4)
    f = j.fuentes.p if len(t.texto) > 22 else j.fuentes.m
    if t.titulo:  # tarxeta grande (ordenar): título, imaxe e texto
        tx.texto(s, j.fuentes.m, t.titulo, (r.centerx, r.y + 10), C.CAJA_BORDE, centro=True)
        s.blit(t.imaxe, (r.centerx - t.imaxe.get_width() // 2, r.y + 46))
        y = r.y + 52 + t.imaxe.get_height()
        tx.parrafo(s, j.fuentes.p, t.texto, (r.x + 14, y, r.w - 28, r.bottom - y - 6), centrado=True, max_lineas=2)
    elif t.imaxe is not None and t.imaxe.get_height() > r.h * 0.6:  # imaxe arriba
        s.blit(t.imaxe, (r.centerx - t.imaxe.get_width() // 2, r.y + 8))
        tx.parrafo(s, j.fuentes.m, t.texto, (r.x + 8, r.bottom - 40, r.w - 16, 34), centrado=True, max_lineas=1)
    else:
        x, w = r.x + 14, r.w - 28
        if t.imaxe is not None:
            s.blit(t.imaxe, (x, r.centery - t.imaxe.get_height() // 2))
            x += t.imaxe.get_width() + 10
            w -= t.imaxe.get_width() + 10
        tx.parrafo(s, f, t.texto, (x, r.y + 4, w, r.h - 8), centrado=True, max_lineas=3)


class Reto:
    """Base común: cabeceira, avisos, contador, botóns da esquina e final."""

    def __init__(self, j, titulo, instrucion, al_terminar):
        self.j = j
        self.titulo = titulo
        self.instrucion = instrucion
        self.al_terminar = al_terminar
        self.deco = Decorado(j.arte, 150)
        self.acertos = self.erros = 0
        self.aviso = None
        self.t = 0.0
        self.rematado = False
        self.esquina = ui.BotonsEsquina(j)
        self.boton_seguir = ui.Boton((ANCHO // 2 - 140, ALTO // 2 + 40, 280, 70), "Continuar  >", C.BOTON_LARANXA)

    def avisar(self, txt, bo):
        self.aviso = [txt, 5.0, bo]

    def acertar(self, pista=None):
        self.acertos += 1
        self.j.sonidos.play("blip")
        if pista:
            self.avisar(pista, True)

    def fallar(self, pista):
        self.erros += 1
        self.j.sonidos.play("error")
        self.avisar(pista, False)

    def completar(self):
        self.rematado = True
        self.j.sonidos.play("bonus")

    def update_comun(self, dt):
        self.t += dt
        if self.esquina.update():
            return True
        if self.aviso:
            self.aviso[1] -= dt
            if self.aviso[1] <= 0:
                self.aviso = None
        if self.rematado and self.boton_seguir.tocado(self.j.entrada):
            self.j.sonidos.play("confirmar")
            self.al_terminar({"acertos": self.acertos, "erros": self.erros})
            return True
        return False

    def debuxar_comun(self, s):
        ui.cabeceira(s, self.j, self.titulo, self.instrucion)
        cont = f"Acertos {self.acertos}    Erros {self.erros}"
        tx.texto(s, self.j.fuentes.m, cont, (ANCHO - 160 - self.j.fuentes.m.size(cont)[0], 14), C.BLANCO, (20, 28, 60))
        self.esquina.draw(s)
        if self.aviso and not self.rematado:
            ui.aviso(s, self.j, self.aviso[0], self.aviso[2])
        if self.rematado:
            ui.velo(s, 100)
            tx.caja(s, (ANCHO // 2 - 300, ALTO // 2 - 130, 600, 270), borde=C.OK, g=5)
            tx.titulo(s, self.j.fuentes.t, "MOI BEN!", (ANCHO // 2, ALTO // 2 - 70))
            tx.texto(s, self.j.fuentes.m, f"Acertos: {self.acertos}      Erros: {self.erros}",
                     (ANCHO // 2, ALTO // 2 - 16), C.TEXTO, centro=True)
            self.boton_seguir.debuxar(s, self.j)


class ArrastreMixin:
    """Arrastrar ou tocar-e-tocar unha tarxeta. Chama a self.soltar_en(tarxeta, pos)."""

    def iniciar_arrastre(self):
        self.arrastrando = None
        self.offset = (0, 0)
        self.clic_pos = None
        self.seleccionada = None

    def xestionar_arrastre(self, dt, tarxetas):
        ent = self.j.entrada
        for t in tarxetas:
            t.erro_t = max(0.0, t.erro_t - dt)
        if ent.clic and not self.rematado and ent.clic[1] > 96:
            libres = [t for t in tarxetas if not t.colocada and t.rect.collidepoint(ent.clic)]
            if libres:
                t = libres[-1]
                self.arrastrando = t
                self.offset = (ent.clic[0] - t.rect.x, ent.clic[1] - t.rect.y)
                self.clic_pos = ent.clic
            elif self.seleccionada:
                t = self.seleccionada
                self.seleccionada = None
                self.soltar_en(t, ent.clic)
        if self.arrastrando:
            t = self.arrastrando
            if ent.premido:
                t.pos = [ent.pos[0] - self.offset[0], ent.pos[1] - self.offset[1]]
                t.rect.topleft = (round(t.pos[0]), round(t.pos[1]))
            if ent.soltar or not ent.premido:
                fin = ent.soltar or ent.pos
                self.arrastrando = None
                if math.hypot(fin[0] - self.clic_pos[0], fin[1] - self.clic_pos[1]) < 12:
                    self.seleccionada = None if self.seleccionada is t else t
                    self.j.sonidos.play("texto")
                else:
                    self.seleccionada = None
                    self.soltar_en(t, fin)
        for t in tarxetas:
            if t is not self.arrastrando and not t.colocada:
                t.volver(dt)

    def debuxar_tarxetas(self, s, tarxetas):
        for t in tarxetas:
            if not t.colocada and t is not self.arrastrando:
                debuxar_tarxeta(s, self.j, t, t is self.seleccionada)
        if self.arrastrando:
            debuxar_tarxeta(s, self.j, self.arrastrando, True)


# ================================================================ clasificar


class EscenaClasificar(Reto, ArrastreMixin):
    def __init__(self, j, titulo, d, al_terminar):
        super().__init__(j, titulo, d["instrucion"], al_terminar)
        self.iniciar_arrastre()
        tarx = list(d["tarxetas"])
        random.shuffle(tarx)
        con_imaxe = any(len(t) > 3 for t in tarx)
        cols = 4 if con_imaxe else 5 if len(tarx) > 8 else 4 if len(tarx) > 6 else 3
        tw, th = (270, 150) if con_imaxe else (232 if cols == 5 else 290, 88)
        self.tarxetas = []
        for i, item in enumerate(tarx):
            texto_, clave, pista = item[:3]
            img = j.arte.encaixar(item[3], 140, 104) if len(item) > 3 else None
            fila_n = min(cols, len(tarx) - (i // cols) * cols)
            x0 = (ANCHO - (fila_n * tw + (fila_n - 1) * 16)) // 2
            rect = (x0 + (i % cols) * (tw + 16), 110 + (i // cols) * (th + 14), tw, th)
            self.tarxetas.append(Tarxeta(rect, texto_, clave, pista, img))
        filas = (len(tarx) + cols - 1) // cols
        y_caixas = 110 + filas * (th + 14) + 10
        n = len(d["caixas"])
        w = (ANCHO - 40 - (n - 1) * 16) // n
        self.caixas = [{"clave": c, "nome": nome, "cor": cor, "items": [], "erro_t": 0.0,
                        "rect": pygame.Rect(20 + i * (w + 16), y_caixas, w, ALTO - y_caixas - 14)}
                       for i, (c, nome, cor) in enumerate(d["caixas"])]

    def soltar_en(self, t, pos):
        for cx in self.caixas:
            if cx["rect"].collidepoint(pos):
                if cx["clave"] == t.clave:
                    t.colocada = True
                    cx["items"].append(t)
                    self.acertar(t.pista)
                    if all(x.colocada for x in self.tarxetas):
                        self.completar()
                else:
                    t.erro_t = cx["erro_t"] = 0.9
                    self.fallar(t.pista)
                return

    def update(self, dt):
        if self.update_comun(dt):
            return
        for cx in self.caixas:
            cx["erro_t"] = max(0.0, cx["erro_t"] - dt)
        self.xestionar_arrastre(dt, self.tarxetas)

    def draw(self, s):
        self.deco.draw(s)
        f = self.j.fuentes
        for cx in self.caixas:
            r = cx["rect"]
            borde = C.ERRO if cx["erro_t"] > 0 else cx["cor"]
            tx.caja(s, r, fondo=(244, 248, 255), borde=borde, g=5)
            pygame.draw.rect(s, cx["cor"], (r.x + 8, r.y + 8, r.w - 16, 48), border_radius=10)
            tx.parrafo(s, f.m if f.m.size(cx["nome"])[0] < r.w - 30 else f.p, cx["nome"],
                       (r.x + 12, r.y + 8, r.w - 24, 48), C.BLANCO, escurecer(cx["cor"], 0.5), centrado=True)
            if self.seleccionada and not self.rematado:
                pygame.draw.rect(s, C.NARANJA, r.inflate(8, 8), 4, border_radius=18)
            for k, t in enumerate(cx["items"]):
                y = r.y + 66 + k * 42
                if y + 36 > r.bottom:
                    break
                pygame.draw.rect(s, (220, 242, 226), (r.x + 12, y, r.w - 24, 36), border_radius=10)
                pygame.draw.lines(s, C.OK, False, [(r.x + 24, y + 18), (r.x + 31, y + 26), (r.x + 44, y + 9)], 4)
                txt = t.texto
                while f.p.size(txt)[0] > r.w - 84 and len(txt) > 4:
                    txt = txt[:-2]
                if txt != t.texto:
                    txt = txt.rstrip() + "…"
                tx.texto(s, f.p, txt, (r.x + 56, y + 5), C.OK)
        self.debuxar_tarxetas(s, self.tarxetas)
        self.debuxar_comun(s)


# ================================================================ ordenar


class EscenaOrdenar(Reto, ArrastreMixin):
    def __init__(self, j, titulo, d, al_terminar):
        super().__init__(j, titulo, d["instrucion"], al_terminar)
        self.iniciar_arrastre()
        n = len(d["pasos"])
        w, h, gap = 372, 284, 40
        x0 = (ANCHO - (n * w + (n - 1) * gap)) // 2
        self.ocos = [{"n": i, "rect": pygame.Rect(x0 + i * (w + gap), 110, w, h), "tarxeta": None, "erro_t": 0.0}
                     for i in range(n)]
        orde = list(range(n))
        while orde == sorted(orde):
            random.shuffle(orde)
        self.tarxetas = []
        for pos, i in enumerate(orde):
            nome, texto_, img, pista = d["pasos"][i]
            t = Tarxeta((x0 + pos * (w + gap), 418, w, h), texto_, i, pista, j.arte.encaixar(img, 300, 170), nome)
            self.tarxetas.append(t)

    def soltar_en(self, t, pos):
        for oco in self.ocos:
            if oco["rect"].collidepoint(pos) and oco["tarxeta"] is None:
                if oco["n"] == t.clave:
                    t.colocada = True
                    t.rect.topleft = oco["rect"].topleft
                    oco["tarxeta"] = t
                    self.acertar(t.pista)
                    if all(o["tarxeta"] for o in self.ocos):
                        self.completar()
                else:
                    t.erro_t = oco["erro_t"] = 0.9
                    self.fallar(f"Ese non é o paso {oco['n'] + 1}. {t.pista}")
                return

    def update(self, dt):
        if self.update_comun(dt):
            return
        for o in self.ocos:
            o["erro_t"] = max(0.0, o["erro_t"] - dt)
        self.xestionar_arrastre(dt, self.tarxetas)

    def draw(self, s):
        self.deco.draw(s)
        for k, o in enumerate(self.ocos):
            r = o["rect"]
            cor = C.ERRO if o["erro_t"] > 0 else (C.NARANJA if self.seleccionada else (200, 214, 240))
            pygame.draw.rect(s, (44, 60, 110), r, border_radius=18)
            pygame.draw.rect(s, cor, r, 5, border_radius=18)
            tx.titulo(s, self.j.fuentes.t, str(k + 1), r.center, (140, 160, 210), (44, 60, 110))
            if k < len(self.ocos) - 1:
                ax = r.right + 8
                pygame.draw.polygon(s, C.AMARILLO, [(ax, r.centery - 16), (ax + 24, r.centery), (ax, r.centery + 16)])
        for o in self.ocos:
            if o["tarxeta"]:
                debuxar_tarxeta(s, self.j, o["tarxeta"])
        self.debuxar_tarxetas(s, self.tarxetas)
        self.debuxar_comun(s)


# ================================================================ unir con frechas


def frecha(s, cor, a, b, g=7):
    pygame.draw.line(s, escurecer(cor, 0.6), a, b, g + 4)
    pygame.draw.line(s, cor, a, b, g)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    pts = [b, (b[0] + math.cos(ang + 2.6) * 26, b[1] + math.sin(ang + 2.6) * 26),
           (b[0] + math.cos(ang - 2.6) * 26, b[1] + math.sin(ang - 2.6) * 26)]
    pygame.draw.polygon(s, cor, pts)
    pygame.draw.polygon(s, escurecer(cor, 0.6), pts, 3)


class EscenaUnir(Reto):
    def __init__(self, j, titulo, d, al_terminar):
        super().__init__(j, titulo, d["instrucion"], al_terminar)
        pares = d["parellas"]
        n = len(pares)
        alto = min(112, (ALTO - 112 - 10) // n)
        self.esq, self.der = [], []
        for i, (nome, img, explic, pista) in enumerate(pares):
            ih = alto - 18
            ic = imaxe_de(j, img, int(ih * (1.36 if not j.arte.existe("ic_" + img) else 1)), ih)
            rect = pygame.Rect(40, 112 + i * alto, 430 if nome else 260, alto - 12)
            self.esq.append({"i": i, "nome": nome, "img": ic, "pista": pista, "rect": rect, "feito": False})
        orde = list(range(n))
        while n > 1 and any(a == b for a, b in zip(orde, range(n))):
            random.shuffle(orde)
        for fila, i in enumerate(orde):
            rect = pygame.Rect(ANCHO - 40 - 560, 112 + fila * alto, 560, alto - 12)
            self.der.append({"i": i, "texto": pares[i][2], "rect": rect, "feito": False})
        self.linhas = []
        self.erro_linha = None
        self.orixe = None
        self.arrastrando = False

    def _pe(self, e):
        return e["rect"].right + 6, e["rect"].centery

    def _pd(self, d):
        return d["rect"].x - 6, d["rect"].centery

    def _probar(self, e, pos):
        for d in self.der:
            if d["rect"].inflate(20, 10).collidepoint(pos) and not d["feito"]:
                if d["i"] == e["i"]:
                    e["feito"] = d["feito"] = True
                    self.linhas.append((e, d))
                    self.acertar(e["pista"])
                    if all(x["feito"] for x in self.esq):
                        self.completar()
                else:
                    self.erro_linha = (self._pe(e), self._pd(d), 1.0)
                    self.fallar(e["pista"])
                self.orixe = None
                return True
        return False

    def update(self, dt):
        if self.update_comun(dt):
            return
        ent = self.j.entrada
        if self.erro_linha:
            a, b, t = self.erro_linha
            self.erro_linha = (a, b, t - dt) if t - dt > 0 else None
        if self.rematado:
            return
        if ent.clic and ent.clic[1] > 96:
            tocado = next((e for e in self.esq if not e["feito"] and e["rect"].inflate(16, 8).collidepoint(ent.clic)), None)
            if tocado:
                self.orixe = tocado
                self.arrastrando = True
                self.j.sonidos.play("texto")
            elif self.orixe:
                self._probar(self.orixe, ent.clic)
        if self.arrastrando and (ent.soltar or not ent.premido):
            self.arrastrando = False
            fin = ent.soltar or ent.pos
            if self.orixe and not self.orixe["rect"].inflate(16, 8).collidepoint(fin):
                if not self._probar(self.orixe, fin):
                    self.orixe = None

    def draw(self, s):
        self.deco.draw(s)
        f = self.j.fuentes
        for e in self.esq:
            r = e["rect"]
            cor = C.OK if e["feito"] else (C.NARANJA if e is self.orixe else C.CAJA_BORDE)
            tx.caja(s, r, fondo=PAPEL, borde=cor, g=4)
            img = e["img"]
            if e["nome"]:
                s.blit(img, (r.x + 12, r.centery - img.get_height() // 2))
                tx.parrafo(s, f.m, e["nome"], (r.x + 24 + img.get_width(), r.y, r.w - 36 - img.get_width(), r.h), centrado=True)
            else:
                s.blit(img, (r.centerx - img.get_width() // 2, r.centery - img.get_height() // 2))
            pygame.draw.circle(s, cor, self._pe(e), 10)
        for d in self.der:
            r = d["rect"]
            cor = C.OK if d["feito"] else C.CAJA_BORDE
            tx.caja(s, r, fondo=PAPEL, borde=cor, g=4)
            tx.parrafo(s, f.m, d["texto"], (r.x + 20, r.y, r.w - 40, r.h), centrado=True, max_lineas=2)
            pygame.draw.circle(s, cor, self._pd(d), 10)
        for e, d in self.linhas:
            frecha(s, C.OK, self._pe(e), self._pd(d))
        if self.erro_linha:
            frecha(s, C.ERRO, self.erro_linha[0], self.erro_linha[1])
        if self.orixe and self.arrastrando:
            frecha(s, C.NARANJA, self._pe(self.orixe), self.j.entrada.pos)
        self.debuxar_comun(s)


# ================================================================ colocar nun mapa ou debuxo


class EscenaColocar(Reto, ArrastreMixin):
    def __init__(self, j, titulo, d, al_terminar):
        super().__init__(j, titulo, d["instrucion"], al_terminar)
        self.iniciar_arrastre()
        xerador = getattr(mapas, {"mapa_espana": "mapa_espana", "mapa_galicia": "mapa_galicia",
                                  "globo_zonas": "globo_zonas", "montana_altitude": "montana_altitude"}[d["fondo"]])
        w, h = (640, 600) if d["fondo"] == "mapa_galicia" else (860, 600)
        self.fondo, anc = xerador(w, h)
        self.fx, self.fy = 16 + (860 - w) // 2, 108
        self.ocos = [{"clave": c, "pos": (self.fx + anc[a][0], self.fy + anc[a][1]), "tarxeta": None, "erro_t": 0.0}
                     for c, a in d["ocos"]]
        tarx = list(d["tarxetas"])
        random.shuffle(tarx)
        alto = min(84, (ALTO - 120) // len(tarx) - 10)
        self.tarxetas = [Tarxeta((900, 116 + i * (alto + 10), 364, alto), t, c, p) for i, (t, c, p) in enumerate(tarx)]

    def soltar_en(self, t, pos):
        libres = [o for o in self.ocos if o["tarxeta"] is None]
        if not libres:
            return
        o = min(libres, key=lambda o: math.hypot(pos[0] - o["pos"][0], pos[1] - o["pos"][1]))
        if math.hypot(pos[0] - o["pos"][0], pos[1] - o["pos"][1]) > 80:
            return
        if o["clave"] == t.clave:
            t.colocada = True
            o["tarxeta"] = t
            self.acertar(t.pista)
            if all(x["tarxeta"] for x in self.ocos):
                self.completar()
        else:
            t.erro_t = o["erro_t"] = 0.9
            self.fallar(t.pista if t.clave != "x" else t.pista)

    def update(self, dt):
        if self.update_comun(dt):
            return
        for o in self.ocos:
            o["erro_t"] = max(0.0, o["erro_t"] - dt)
        self.xestionar_arrastre(dt, self.tarxetas)

    def draw(self, s):
        self.deco.draw(s)
        tx.caja(s, (self.fx - 8, self.fy - 8, self.fondo.get_width() + 16, self.fondo.get_height() + 16), radio=12)
        s.blit(self.fondo, (self.fx, self.fy))
        f = self.j.fuentes
        for o in self.ocos:
            x, y = o["pos"]
            if o["tarxeta"]:
                txt = o["tarxeta"].texto
                w = f.m.size(txt)[0] + 28
                tx.caja(s, (x - w // 2, y - 24, w, 48), fondo=(230, 248, 234), borde=C.OK, radio=14, g=4)
                tx.texto(s, f.m, txt, (x, y - 17), C.OK, centro=True)
            else:
                cor = C.ERRO if o["erro_t"] > 0 else (C.NARANJA if (self.seleccionada or self.arrastrando) else C.BLANCO)
                pygame.draw.circle(s, (30, 40, 80), (x, y), 34)
                pygame.draw.circle(s, (70, 96, 170), (x, y), 30)
                pygame.draw.circle(s, cor, (x, y), 34, 5)
                tx.texto(s, f.g, "?", (x, y - 26), C.BLANCO, centro=True)
        self.debuxar_tarxetas(s, self.tarxetas)
        self.debuxar_comun(s)


# ================================================================ mapa do tempo (misión 1)


class EscenaMapaTempo(Reto):
    PALETA = ["soleado", "sol_nubes", "nubrado", "chuvia", "neve", "treboada", "vento"]

    def __init__(self, j, titulo, al_terminar):
        super().__init__(j, titulo, "Le a predición e arrastra cada símbolo ao seu lugar do mapa.", al_terminar)
        self.fondo = crear_fondo(j.arte)
        montana = random.choice(["neve", "nubrado", "vento"])
        resto = ["chuvia", "soleado", random.choice([x for x in ("sol_nubes", "nubrado", "vento") if x != montana])]
        random.shuffle(resto)
        asig = dict(zip(["lago", "aldea", "bosque"], resto))
        asig["montana"] = montana
        self.lugares = []
        for clave, (nome, prep, c, r) in datos.LUGARES.items():
            self.lugares.append({"clave": clave, "nome": nome, "prep": prep, "pos": centro_tile(c, r),
                                 "esperado": asig[clave], "posto": None, "erro_t": 0.0})
        self.iconas = {k: j.arte.imaxe("ic_" + k, 72, 72) for k in self.PALETA}
        self.botons_paleta = [(k, pygame.Rect(28 + i * 84, 618, 78, 84)) for i, k in enumerate(self.PALETA)]
        self.arrastrando = None
        self.seleccionada = None
        self.pos_arrastre = (0, 0)
        self.clic_pos = None
        self.panel = None
        self.preguntas_finais = self._preguntas_finais()

    def _preguntas_finais(self):
        nomes = {l["clave"]: l["nome"].capitalize() for l in self.lugares}
        chuv = next(l for l in self.lugares if l["esperado"] == "chuvia")
        sol_ = next(l for l in self.lugares if l["esperado"] == "soleado")
        ops = list(nomes.values())

        def p(texto_, lugar, exp):
            outras = [o for o in ops if o != nomes[lugar["clave"]]]
            random.shuffle(outras)
            return {"tipo": "test", "p": texto_, "ops": [nomes[lugar["clave"]]] + outras[:2], "ok": 0, "exp": exp}
        return [p("Mañá queres saír de excursión. Onde necesitarás o paraugas?", chuv,
                  f"{chuv['prep']} choverá. O tempo atmosférico dinos que roupa levar e se precisamos paraugas."),
                p("E onde necesitarás as lentes de sol?", sol_, f"{sol_['prep']} fará sol: alí necesitarás lentes de sol.")]

    def _soltar(self, clave, pos):
        for l in self.lugares:
            if l["posto"] is None and math.hypot(pos[0] - l["pos"][0], pos[1] - l["pos"][1]) < 70:
                if l["esperado"] == clave:
                    l["posto"] = clave
                    self.acertar(f"Correcto! {l['prep']} {datos.TEMPO[clave][1]}.")
                    if all(x["posto"] for x in self.lugares):
                        self.panel = PanelPregunta(self.j, self.preguntas_finais.pop(0), "LE O TEU MAPA DO TEMPO")
                else:
                    l["erro_t"] = 0.9
                    self.fallar(f"Ese símbolo significa «{datos.TEMPO[clave][0]}». Le de novo a predición: "
                                f"{l['prep'].lower()} {datos.TEMPO[l['esperado']][1]}.")
                return

    def update(self, dt):
        if self.panel:
            self.panel.update(dt)
            if self.panel.rematado:
                if self.panel.acerto:
                    self.acertos += 1
                else:
                    self.erros += 1
                self.panel = None
                if self.preguntas_finais:
                    self.panel = PanelPregunta(self.j, self.preguntas_finais.pop(0), "LE O TEU MAPA DO TEMPO")
                else:
                    self.completar()
            return
        if self.update_comun(dt):
            return
        for l in self.lugares:
            l["erro_t"] = max(0.0, l["erro_t"] - dt)
        if self.rematado:
            return
        ent = self.j.entrada
        if ent.clic and ent.clic[1] > 96:
            tocado = next((k for k, r in self.botons_paleta if r.collidepoint(ent.clic)), None)
            if tocado:
                self.arrastrando = tocado
                self.clic_pos = self.pos_arrastre = ent.clic
            elif self.seleccionada:
                clave, self.seleccionada = self.seleccionada, None
                self._soltar(clave, ent.clic)
        if self.arrastrando:
            self.pos_arrastre = ent.pos
            if ent.soltar or not ent.premido:
                fin = ent.soltar or ent.pos
                clave, self.arrastrando = self.arrastrando, None
                if math.hypot(fin[0] - self.clic_pos[0], fin[1] - self.clic_pos[1]) < 12:
                    self.seleccionada = None if self.seleccionada == clave else clave
                    self.j.sonidos.play("texto")
                else:
                    self.seleccionada = None
                    self._soltar(clave, fin)

    def draw(self, s):
        s.fill(C.NEGRO)
        s.blit(self.fondo, (0, HUD_ALTO))
        f = self.j.fuentes
        tx.caja(s, (16, 110, 440, 196), fondo=PAPEL)
        tx.texto(s, f.m, "PREDICIÓN PARA MAÑÁ", (36, 122), C.CAJA_BORDE)
        for i, l in enumerate(self.lugares):
            tx.texto(s, f.m, f"{l['prep']} {datos.TEMPO[l['esperado']][1]}.", (36, 162 + i * 34),
                     C.OK if l["posto"] else C.TEXTO)
        for l in self.lugares:
            x, y = l["pos"]
            cor = C.ERRO if l["erro_t"] > 0 else (C.NARANJA if (self.seleccionada or self.arrastrando) else C.BLANCO)
            pygame.draw.circle(s, (30, 40, 80), (x, y), 50)
            pygame.draw.circle(s, (255, 255, 255) if l["posto"] else (70, 96, 170), (x, y), 45)
            pygame.draw.circle(s, cor, (x, y), 50, 5)
            if l["posto"]:
                ic = self.iconas[l["posto"]]
                s.blit(ic, (x - 36, y - 36))
            else:
                tx.texto(s, f.g, "?", (x, y - 26), C.BLANCO, centro=True)
            w = f.m.size(l["nome"])[0] + 24
            pygame.draw.rect(s, C.CAJA_BORDE, (x - w // 2, y + 52, w, 38), border_radius=10)
            tx.texto(s, f.m, l["nome"], (x, y + 55), C.BLANCO, centro=True)
        tx.caja(s, (12, 604, 620, 110), fondo=PAPEL)
        for k, r in self.botons_paleta:
            if k == self.seleccionada:
                pygame.draw.rect(s, C.NARANJA, r.inflate(8, 8), border_radius=14)
            pygame.draw.rect(s, (226, 238, 252), r, border_radius=12)
            s.blit(self.iconas[k], (r.x + 3, r.y + 6))
        if self.arrastrando:
            x, y = self.pos_arrastre
            s.blit(self.j.arte.imaxe("ic_" + self.arrastrando, 90, 90), (x - 45, y - 45))
        self.debuxar_comun(s)
        if self.panel:
            self.panel.debuxar(s)


# ================================================================ quiz


class EscenaQuiz(Reto):
    def __init__(self, j, titulo, pool, al_terminar, n=None):
        super().__init__(j, titulo, "Responde as preguntas.", al_terminar)
        banco = j.bancos[pool]
        self.preguntas = [banco.seguinte() for _ in range(n or datos.PREGUNTAS_QUIZ)]
        self.i = 0
        self.panel = self._panel()

    def _panel(self):
        return PanelPregunta(self.j, self.preguntas[self.i], f"PREGUNTA {self.i + 1} DE {len(self.preguntas)}",
                             rect=(90, 106, 1100, 600))

    def update(self, dt):
        if self.panel and not self.rematado:
            self.t += dt
            if self.esquina.update():
                return
            self.panel.update(dt)
            if self.panel.rematado:
                if self.panel.acerto:
                    self.acertos += 1
                else:
                    self.erros += 1
                self.i += 1
                if self.i < len(self.preguntas):
                    self.panel = self._panel()
                else:
                    self.panel = None
                    self.completar()
            return
        self.update_comun(dt)

    def draw(self, s):
        self.deco.draw(s)
        if self.panel:
            ui.cabeceira(s, self.j, self.titulo, self.instrucion)
            self.esquina.draw(s)
            self.panel.debuxar(s)
        else:
            self.debuxar_comun(s)


# ================================================================ climogramas


def debuxar_climograma(s, j, rect, d, ocultas_b=(), ocultos_p=(), valores=None, correctos=(), resaltar=None):
    """Debuxa un climograma: barras azuis (precipitacións) e liña vermella (temperaturas).
    As precipitacións debúxanse á dobre escala que as temperaturas."""
    valores = valores or {}
    r = pygame.Rect(rect)
    f = j.fuentes
    tx.caja(s, r, fondo=(255, 255, 255), radio=14)
    tit = f"{d['nome']}  ·  {d['altitude']} m  ·  {str(d['tmedia']).replace('.', ',')} °C  ·  {d['total']} mm"
    ft = f.m if f.m.size(tit)[0] < r.w - 40 else f.p
    tx.texto(s, ft, tit, (r.centerx, r.y + 12), C.CAJA_BORDE, centro=True)
    pmax = 80 if max(d["prec"]) <= 80 else math.ceil(max(d["prec"]) / 40) * 40
    tmax = pmax / 2
    area = pygame.Rect(r.x + 74, r.y + 84, r.w - 160, r.h - 136)
    for k in range(5):
        y = area.bottom - area.h * k / 4
        pygame.draw.line(s, (226, 232, 242), (area.x, y), (area.right, y), 2)
        tx.texto(s, f.p, f"{int(tmax * k / 4)}", (area.x - 12 - f.p.size(f"{int(tmax * k / 4)}")[0], y - 14), (200, 60, 50))
        tx.texto(s, f.p, f"{int(pmax * k / 4)}", (area.right + 12, y - 14), (50, 100, 200))
    tx.texto(s, f.p, "°C", (area.x - 50, area.y - 38), (200, 60, 50))
    tx.texto(s, f.p, "mm", (area.right + 12, area.y - 38), (50, 100, 200))
    colw = area.w / 12
    pts = []
    for i in range(12):
        cx = area.x + colw * (i + 0.5)
        bw = colw * 0.62
        if resaltar == i:
            pygame.draw.rect(s, (255, 244, 200), (area.x + colw * i, area.y, colw, area.h))
        if i in ocultas_b and i not in valores.get("b", {}):
            pygame.draw.rect(s, (180, 190, 210), (cx - bw / 2, area.bottom - 60, bw, 60), 3, border_radius=4)
            tx.texto(s, f.m, "?", (cx, area.bottom - 50), (120, 130, 160), centro=True)
        else:
            v = valores.get("b", {}).get(i, d["prec"][i])
            hh = area.h * v / pmax
            cor = (90, 150, 240) if i not in ocultas_b else ((80, 190, 110) if i in correctos else (150, 190, 250))
            pygame.draw.rect(s, cor, (cx - bw / 2, area.bottom - hh, bw, hh), border_top_left_radius=4, border_top_right_radius=4)
            pygame.draw.rect(s, escurecer(cor, 0.6), (cx - bw / 2, area.bottom - hh, bw, hh), 2,
                             border_top_left_radius=4, border_top_right_radius=4)
        if i in ocultos_p and i not in valores.get("p", {}):
            pts.append(None)
        else:
            v = valores.get("p", {}).get(i, d["temp"][i])
            pts.append((cx, area.bottom - area.h * v / tmax, i))
        tx.texto(s, f.m, datos.MESES_CURTOS[i], (cx, area.bottom + 8), C.TEXTO, centro=True)
    for a, b in zip(pts, pts[1:]):
        if a and b:
            pygame.draw.line(s, (220, 60, 50), a[:2], b[:2], 5)
    for q in pts:
        if q:
            cor = (80, 190, 110) if (q[2] in ocultos_p and q[2] in correctos) else (220, 60, 50)
            pygame.draw.circle(s, cor, q[:2], 9)
            pygame.draw.circle(s, escurecer(cor, 0.6), q[:2], 9, 2)
    for i in ocultos_p:
        if i not in valores.get("p", {}):
            cx = area.x + colw * (i + 0.5)
            pygame.draw.circle(s, (255, 255, 255), (cx, area.y + 26), 18)
            pygame.draw.circle(s, (220, 60, 50), (cx, area.y + 26), 18, 3)
            tx.texto(s, f.m, "?", (cx, area.y + 10), (220, 60, 50), centro=True)
    pygame.draw.line(s, C.TEXTO, (area.x, area.y - 10), (area.x, area.bottom), 3)
    pygame.draw.line(s, C.TEXTO, (area.right, area.y - 10), (area.right, area.bottom), 3)
    pygame.draw.line(s, C.TEXTO, (area.x, area.bottom), (area.right, area.bottom), 3)
    return area, pmax, tmax


class EscenaClimograma(Reto):
    def __init__(self, j, titulo, modo, al_terminar):
        instr = {"ler": "Observa o climograma de Ciudad Real e responde.",
                 "construir": "Completa o climograma coa táboa: toca na columna do mes, á altura correcta.",
                 "comparar": "Compara os dous climogramas e responde."}[modo]
        super().__init__(j, titulo, instr, al_terminar)
        self.modo = modo
        self.cr = datos.CLIMOGRAMAS["ciudad_real"]
        self.panel = None
        if modo == "ler":
            self.preguntas = random.sample(datos.LER_CLIMOGRAMA, 5)
            self.i = 0
            self._novo_panel()
        elif modo == "construir":
            c = datos.CONSTRUIR
            self.d = datos.CLIMOGRAMAS[c["cidade"]]
            self.barras, self.puntos = set(c["barras"]), set(c["puntos"])
            self.valores = {"b": {}, "p": {}}
            self.correctos = set()
            self.area = None
            self.marca = None
        else:
            self.preguntas = list(datos.COMPARAR)
            self.i = 0
            self.orde = ["santander", "ciudad_real"]
            random.shuffle(self.orde)
            self.resposta = None
            self.botons = [ui.Boton((ANCHO // 2 - 340 + k * 360, 610, 320, 80), datos.CLIMOGRAMAS[c]["nome"], C.BOTON, fonte="g")
                           for k, c in enumerate(self.orde)]
            self.continuar = ui.Boton((ANCHO - 290, 618, 250, 70), "Continuar  >", C.BOTON_LARANXA)

    def _novo_panel(self):
        self.panel = PanelPregunta(self.j, self.preguntas[self.i], f"PREGUNTA {self.i + 1} DE {len(self.preguntas)}",
                                   rect=(726, 108, 540, 600), veo=False)

    # ------------------------------------------------------------ actualizar
    def update(self, dt):
        if self.rematado:
            self.update_comun(dt)
            return
        if self.update_comun(dt):
            return
        ent = self.j.entrada
        if self.modo == "ler":
            self.panel.update(dt)
            if self.panel.rematado:
                self.acertos += self.panel.acerto
                self.erros += not self.panel.acerto
                self.i += 1
                if self.i < len(self.preguntas):
                    self._novo_panel()
                else:
                    self.completar()
        elif self.modo == "construir":
            if self.marca:
                self.marca[1] -= dt
                if self.marca[1] <= 0:
                    self.marca = None
            if ent.clic and self.area and self.area[0].inflate(0, 40).collidepoint(ent.clic):
                area, pmax, tmax = self.area
                i = int((ent.clic[0] - area.x) / (area.w / 12))
                i = max(0, min(11, i))
                frac = max(0.0, min(1.0, (area.bottom - ent.clic[1]) / area.h))
                mes = datos.MESES[i]
                if i in self.barras and i not in self.correctos:
                    v = round(frac * pmax)
                    self.valores["b"][i] = v
                    real = self.d["prec"][i]
                    if abs(v - real) <= max(5, pmax / 16):
                        self.valores["b"][i] = real
                        self.correctos.add(i)
                        self.acertar(f"Moi ben! En {mes.lower()} caeron {real} mm.")
                    else:
                        del self.valores["b"][i]
                        self.marca = [ent.clic, 1.2]
                        cara = "máis arriba" if v < real else "máis abaixo"
                        self.fallar(f"Mira a táboa: en {mes.lower()} caeron {real} mm. Toca {cara}.")
                elif i in self.puntos and i not in self.correctos:
                    v = round(frac * tmax, 1)
                    self.valores["p"][i] = v
                    real = self.d["temp"][i]
                    if abs(v - real) <= max(2, tmax / 16):
                        self.valores["p"][i] = real
                        self.correctos.add(i)
                        self.acertar(f"Moi ben! En {mes.lower()} a temperatura media foi {str(real).replace('.', ',')} °C.")
                    else:
                        del self.valores["p"][i]
                        self.marca = [ent.clic, 1.2]
                        cara = "máis arriba" if v < real else "máis abaixo"
                        self.fallar(f"Mira a táboa: en {mes.lower()} a temperatura foi {str(real).replace('.', ',')} °C. Toca {cara}.")
                if len(self.correctos) == len(self.barras) + len(self.puntos):
                    self.completar()
        else:
            if self.resposta is None:
                for k, b in enumerate(self.botons):
                    if b.tocado(ent):
                        bo = self.orde[k] == self.preguntas[self.i]["ok"]
                        self.resposta = bo
                        self.acertos += bo
                        self.erros += not bo
                        self.j.sonidos.play("bonus" if bo else "error")
            elif self.continuar.tocado(ent):
                self.resposta = None
                self.i += 1
                if self.i >= len(self.preguntas):
                    self.completar()

    # ------------------------------------------------------------ debuxo
    def draw(self, s):
        self.deco.draw(s)
        f = self.j.fuentes
        if self.modo == "ler":
            debuxar_climograma(s, self.j, (16, 108, 696, 600), self.cr)
            if self.panel and not self.rematado:
                self.panel.debuxar(s)
        elif self.modo == "construir":
            r = pygame.Rect(16, 108, 352, 600)
            tx.caja(s, r, fondo=(255, 255, 255))
            tx.texto(s, f.p, "Mes", (36, 120), C.CAJA_BORDE)
            tx.texto(s, f.p, "°C", (206, 120), (200, 60, 50))
            tx.texto(s, f.p, "mm", (290, 120), (50, 100, 200))
            for i in range(12):
                y = 158 + i * 44
                if i in self.barras or i in self.puntos:
                    cor = (220, 244, 226) if i in self.correctos else (255, 238, 170)
                    pygame.draw.rect(s, cor, (24, y - 4, 336, 40), border_radius=8)
                tx.texto(s, f.m, datos.MESES[i], (36, y), C.TEXTO)
                tx.texto(s, f.m, str(self.d["temp"][i]).replace(".", ","), (200, y),
                         (200, 60, 50) if i in self.puntos else C.TEXTO)
                tx.texto(s, f.m, str(self.d["prec"][i]), (290, y), (50, 100, 200) if i in self.barras else C.TEXTO)
            self.area = debuxar_climograma(s, self.j, (384, 108, 880, 600), self.d, self.barras, self.puntos,
                                           self.valores, self.correctos)
            if self.marca:
                (mx, my), _ = self.marca
                for a, b in (((mx - 14, my - 14), (mx + 14, my + 14)), ((mx - 14, my + 14), (mx + 14, my - 14))):
                    pygame.draw.line(s, (255, 255, 255), a, b, 11)
                    pygame.draw.line(s, C.ERRO, a, b, 7)
        else:
            for k, c in enumerate(self.orde):
                debuxar_climograma(s, self.j, (16 + k * 632, 108, 616, 380), datos.CLIMOGRAMAS[c])
            if not self.rematado and self.i < len(self.preguntas):
                q = self.preguntas[self.i]
                tx.caja(s, (16, 500, ANCHO - 32, 208))
                tx.texto(s, f.g, q["p"], (ANCHO // 2, 520), C.TEXTO, centro=True)
                if self.resposta is None:
                    for b in self.botons:
                        b.debuxar(s, self.j)
                else:
                    cor = C.OK if self.resposta else C.ERRO
                    nome_ok = datos.CLIMOGRAMAS[q["ok"]]["nome"]
                    tx.texto(s, f.g, ("Moi ben! " if self.resposta else "Case... Era ") + nome_ok, (48, 572), cor)
                    tx.parrafo(s, f.m, q["exp"], (48, 624, ANCHO - 400, 80), max_lineas=2)
                    self.continuar.debuxar(s, self.j)
        self.debuxar_comun(s)
