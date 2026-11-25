"""Panel de preguntas táctil (escoller, verdadeiro/falso, completar) e banco de preguntas."""
import random

import pygame

import texto as tx
import ui
from config import C


class Banco:
    """Reparte as preguntas sen repetir ata que se esgotan."""

    def __init__(self, preguntas):
        self.todas = list(preguntas)
        self.restantes = []

    def seguinte(self):
        if not self.restantes:
            self.restantes = self.todas[:]
            random.shuffle(self.restantes)
        return self.restantes.pop()


class PanelPregunta:
    """Pregunta con botóns grandes. Cando rematado=True, 'acerto' indica se acertou.
    compacto=True: versión baixa para a batalla (a imaxe debúxaa a escena)."""

    def __init__(self, j, pregunta, cabeceira="PREGUNTA", rect=(90, 56, 1100, 620), compacto=False, veo=True):
        self.j = j
        self.veo = veo and not compacto
        self.cab = cabeceira
        self.rect = pygame.Rect(rect)
        self.compacto = compacto
        self.p = pregunta
        if pregunta["tipo"] == "vf":
            self.ops = ["VERDADEIRO", "FALSO"]
            self.ok = 0 if pregunta["ok"] else 1
        else:
            correcta = pregunta["ops"][pregunta["ok"]]
            self.ops = list(pregunta["ops"])
            random.shuffle(self.ops)
            self.ok = self.ops.index(correcta)
        self.imaxe = None
        if not compacto:
            clave = pregunta.get("img") or (("ic_" + pregunta["icona"]) if pregunta.get("icona") else None)
            if clave:
                self.imaxe = j.arte.encaixar(clave, 330, 240)
        self.estado = "pregunta"
        self.escolla = None
        self.acerto = None
        self.rematado = False
        self._crear_botons()

    def _crear_botons(self):
        r = self.rect
        self.botons = []
        if self.compacto:
            y0, alto, gap = r.y + 84, 52, 8
        else:
            y0, alto, gap = r.y + 330, 70, 14
        self.y0 = y0
        if self.p["tipo"] == "vf":
            w = (r.w - 80) // 2
            h = 74 if self.compacto else 110
            for i, txt in enumerate(self.ops):
                cor = C.BOTON_VERDE if i == 0 else C.BOTON_ROJO
                self.botons.append(ui.Boton((r.x + 28 + i * (w + 24), y0 + 10, w, h), txt, cor, fonte="g"))
        else:
            for i, txt in enumerate(self.ops):
                self.botons.append(ui.Boton((r.x + 28, y0 + i * (alto + gap), r.w - 56, alto), txt, C.BOTON))
        self.continuar = ui.Boton((r.right - 262, r.bottom - 82, 236, 62), "Continuar  >", C.BOTON_LARANXA)

    def update(self, dt=0):
        ent = self.j.entrada
        if self.estado == "pregunta":
            for i, b in enumerate(self.botons):
                if b.tocado(ent):
                    self.escolla = i
                    self.acerto = i == self.ok
                    self.estado = "resposta"
                    self.j.sonidos.play("bonus" if self.acerto else "error")
                    break
        elif self.continuar.tocado(ent):
            self.rematado = True

    def debuxar(self, s):
        j, r, f = self.j, self.rect, self.j.fuentes
        if self.veo:
            ui.velo(s, 120)
        tx.caja(s, r)
        if not self.compacto:
            pygame.draw.rect(s, C.CAJA_BORDE, (r.x + 10, r.y + 10, r.w - 20, 44), border_radius=10)
            tx.texto(s, f.m, self.cab, (r.x + 28, r.y + 16), C.AMARILLO)
            top = r.y + 72
        else:
            top = r.y + 18

        x_txt = r.x + 30
        if self.imaxe:
            pygame.draw.rect(s, C.CAJA_BORDE, (r.x + 26, top - 4, self.imaxe.get_width() + 8, self.imaxe.get_height() + 8),
                             border_radius=8)
            s.blit(self.imaxe, (r.x + 30, top))
            x_txt = r.x + 30 + self.imaxe.get_width() + 30
        if self.compacto:
            tx.parrafo(s, f.m, self.p["p"], (x_txt, top, r.right - 30 - x_txt, 60), max_lineas=2)
        else:
            fq = f.g if len(tx.envolver(f.g, self.p["p"], r.right - 30 - x_txt)) <= 5 else f.m
            tx.parrafo(s, fq, self.p["p"], (x_txt, top, r.right - 30 - x_txt, 250), max_lineas=6)

        if self.estado == "pregunta":
            for b in self.botons:
                b.debuxar(s, j)
            return

        cor = C.OK if self.acerto else C.ERRO
        if self.compacto:
            cab = "Moi ben!  " + self.ops[self.ok] if self.acerto else "Case... Era: " + self.ops[self.ok]
            tx.texto(s, f.m, cab, (r.x + 30, self.y0 - 8), cor)
            tx.parrafo(s, f.m, self.p["exp"], (r.x + 30, self.y0 + 32, r.w - 330, 120), max_lineas=3)
        else:
            caixa = pygame.Rect(r.x + 18, self.y0 - 8, r.w - 36, r.bottom - self.y0 - 10)
            tx.caja(s, caixa, borde=cor, sombra=False)
            y = caixa.y + 18
            if self.acerto:
                tx.texto(s, f.g, "Moi ben!", (caixa.x + 24, y), cor)
                tx.texto(s, f.m, self.ops[self.ok], (caixa.x + 200, y + 10), C.OK)
                y += 60
            else:
                tx.texto(s, f.m, "Case... A resposta correcta é:", (caixa.x + 24, y), cor)
                y += 38
                tx.texto(s, f.g, self.ops[self.ok], (caixa.x + 24, y), C.OK)
                y += 56
            tx.parrafo(s, f.m, self.p["exp"], (caixa.x + 24, y, caixa.w - 300, caixa.bottom - y - 10), max_lineas=4)
        self.continuar.debuxar(s, j)
