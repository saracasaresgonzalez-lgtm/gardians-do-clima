"""BATALLA FINAL por quendas contra o Barón Feluxe (misión 7).

Cada quenda o Barón ataca e Nubi defende respondendo unha pregunta de todo o tema:
- Resposta correcta: Nubi contraataca con auga e o Barón perde vida.
- Resposta incorrecta: Nubi perde vida (e lese a explicación).
"""
import math
import random

import pygame

import datos
import texto as tx
import ui
from config import ANCHO, C
from pincel import Pincel, escurecer
from preguntas import PanelPregunta

DANO_BARON = 20   # 5 acertos para gañar
DANO_NUBI = 25    # 4 erros para perder
CAIXA = (16, 446, 1248, 262)


class EscenaBatalla:
    def __init__(self, j, titulo, pool, al_terminar):
        self.j = j
        self.banco = j.bancos[pool]
        self.al_terminar = al_terminar
        self.f = j.fuentes
        self.globo = j.arte.imaxe("globo", 200, 245)
        self.nubi = j.arte.imaxe("nubi", 250, 179)
        self.t = 0.0
        self.acertos = self.erros = 0
        self.quenda = 0
        self.parts = []
        self.esquina = ui.BotonsEsquina(j)
        self.fondo = self._crear_fondo()
        self.reiniciar()

    def reiniciar(self):
        self.hp_b = self.hp_b_vis = 100.0
        self.hp_n = self.hp_n_vis = 100.0
        self.tremor_b = self.tremor_n = 0.0
        self.foxe = 0.0
        self.panel = None
        self.imaxe = None
        self.botons = []
        self.mensaxe("O Barón Feluxe desafíate! Cada resposta correcta será un ataque de auga.", self.nova_quenda)

    # ------------------------------------------------------------ estados

    def mensaxe(self, txt, seguinte):
        self.estado = "mensaxe"
        self.txt = txt
        self.letras = 0.0
        self.seguinte = seguinte

    def anim(self, tempo, seguinte):
        self.estado = "anim"
        self.t_anim = tempo
        self.seguinte = seguinte

    def nova_quenda(self):
        ataque = datos.ATAQUES_BARON[self.quenda % len(datos.ATAQUES_BARON)]
        self.mensaxe(f"O Barón Feluxe usa {ataque}! Responde ben para defenderte.", self.preguntar)

    def preguntar(self):
        p = self.banco.seguinte()
        self.estado = "pregunta"
        self.panel = PanelPregunta(self.j, p, rect=CAIXA, compacto=True)
        clave = p.get("img") or (("ic_" + p["icona"]) if p.get("icona") else None)
        self.imaxe = self.j.arte.encaixar(clave, 330, 240) if clave else None

    def _resposta(self, acerto):
        self.panel = None
        self.imaxe = None
        ataque_n = datos.ATAQUES_NUBI[self.quenda % len(datos.ATAQUES_NUBI)]
        self.quenda += 1
        if acerto:
            self.acertos += 1

            def golpe():
                self.hp_b = max(0, self.hp_b - DANO_BARON)
                self.tremor_b = 0.6
                self.j.sonidos.play("apagar")
                self.mensaxe(f"Nubi usa {ataque_n}! É moi eficaz!", self.victoria if self.hp_b <= 0 else self.nova_quenda)
            self.efecto = "chuvia"
            self.anim(1.0, golpe)
        else:
            self.erros += 1

            def golpe():
                self.hp_n = max(0, self.hp_n - DANO_NUBI)
                self.tremor_n = 0.6
                self.j.sonidos.play("risa")
                self.mensaxe("O ataque alcanza a Nubi... Lembra a explicación e segue adiante!",
                             self.derrota if self.hp_n <= 0 else self.nova_quenda)
            self.efecto = "fume"
            self.anim(1.0, golpe)

    def victoria(self):
        self.j.sonidos.play("bonus")
        self.foxe = 0.01
        self.mensaxe("O Barón Feluxe foxe no seu dirixible! GAÑASTE A BATALLA!", self._fin_victoria)

    def _fin_victoria(self):
        self.al_terminar({"acertos": self.acertos, "erros": self.erros, "ganou": True})

    def derrota(self):
        self.j.sonidos.play("error")
        self.estado = "derrota"
        self.txt = "Nubi quedou sen forzas... Queres tentalo de novo?"
        self.botons = [ui.Boton((200, 590, 380, 84), "Tentar de novo", C.BOTON_VERDE, fonte="g"),
                       ui.Boton((700, 590, 380, 84), "Seguir", C.BOTON_GRIS, fonte="g")]

    # ------------------------------------------------------------ bucle

    def update(self, dt):
        self.t += dt
        ent = self.j.entrada
        if self.esquina.update():
            return
        self.hp_b_vis += (self.hp_b - self.hp_b_vis) * min(1, dt * 4)
        self.hp_n_vis += (self.hp_n - self.hp_n_vis) * min(1, dt * 4)
        self.tremor_b = max(0.0, self.tremor_b - dt)
        self.tremor_n = max(0.0, self.tremor_n - dt)
        if self.foxe:
            self.foxe += dt
        self._particulas(dt)

        if self.estado == "mensaxe":
            total = len(self.txt)
            antes = int(self.letras)
            self.letras = min(total, self.letras + 50 * dt)
            if int(self.letras) // 3 != antes // 3 and self.letras < total:
                self.j.sonidos.play("texto")
            if ent.clic:
                if self.letras < total:
                    self.letras = total
                else:
                    self.j.sonidos.play("confirmar")
                    self.seguinte()
        elif self.estado == "pregunta":
            self.panel.update(dt)
            if self.panel.rematado:
                self._resposta(self.panel.acerto)
        elif self.estado == "anim":
            self.t_anim -= dt
            if self.t_anim <= 0:
                self.seguinte()
        elif self.estado == "derrota":
            if self.botons[0].tocado(ent):
                self.j.sonidos.play("confirmar")
                self.reiniciar()
            elif self.botons[1].tocado(ent):
                self.al_terminar({"acertos": self.acertos, "erros": self.erros, "ganou": False})

    def _particulas(self, dt):
        if self.estado == "anim":
            if self.efecto == "chuvia":
                for _ in range(5):
                    self.parts.append(["gota", random.uniform(930, 1130), 0.0, 0.0, 520.0, 0.5])
            elif random.random() < dt * 30:
                self.parts.append(["fume", random.uniform(930, 990), random.uniform(160, 220),
                                   -620.0 + random.uniform(-40, 40), 160.0 + random.uniform(-30, 30), 1.0])
        for p in self.parts:
            p[1] += p[3] * dt
            p[2] += p[4] * dt
            p[5] -= dt
        self.parts = [p for p in self.parts if p[5] > 0]

    # ------------------------------------------------------------ debuxo

    def _crear_fondo(self):
        p = Pincel(ANCHO, 446, ss=2)
        p.degradado(0, 0, ANCHO, 446, (120, 186, 250), (214, 238, 255))
        from arte import nube
        nube(p, 220, 80, 1.6)
        nube(p, 640, 50, 1.2)
        p.poli([(0, 330), (220, 270), (460, 320), (700, 260), (980, 310), (1280, 270), (1280, 446), (0, 446)],
               (150, 206, 140), borde=(110, 170, 110), g=2)
        p.rect(0, 360, ANCHO, 90, (124, 200, 96), borde=None)
        p.elipse(1030, 250, 200, 40, (100, 170, 80), borde=(70, 130, 60), g=3)
        p.elipse(1030, 244, 190, 30, (136, 214, 104), borde=None)
        p.elipse(300, 400, 210, 40, (100, 170, 80), borde=(70, 130, 60), g=3)
        p.elipse(300, 394, 200, 30, (136, 214, 104), borde=None)
        return p.imaxe()

    def _barra(self, s, x, y, w, valor, nome, mostrar_num=False):
        h = 108 if mostrar_num else 92
        tx.caja(s, (x, y, w, h), fondo=(255, 250, 236))
        tx.texto(s, self.f.m, nome, (x + 22, y + 12))
        pygame.draw.rect(s, (60, 60, 74), (x + 22, y + 52, w - 44, 22), border_radius=11)
        frac = max(0.0, valor / 100)
        cor = (72, 200, 96) if frac > 0.5 else (240, 200, 48) if frac > 0.2 else (224, 64, 56)
        if frac > 0:
            pygame.draw.rect(s, cor, (x + 26, y + 56, max(14, int((w - 52) * frac)), 14), border_radius=7)
        if mostrar_num:
            tx.texto(s, self.f.p, f"VIDA {int(round(valor))}/100", (x + w - 170, y + 76), C.TEXTO)

    def draw(self, s):
        s.blit(self.fondo, (0, 0))
        bx = 930 + (math.sin(self.t * 40) * 8 if self.tremor_b else 0) + self.foxe * 220
        by = 20 + math.sin(self.t * 2) * 8 - self.foxe * 200
        if not (self.tremor_b and int(self.t * 20) % 2):
            s.blit(self.globo, (int(bx), int(by)))
        nx = 175 + (math.sin(self.t * 40) * 8 if self.tremor_n else 0)
        ny = 220 + math.sin(self.t * 3) * 6
        if not (self.tremor_n and int(self.t * 20) % 2):
            s.blit(self.nubi, (int(nx), int(ny)))
        for p in self.parts:
            if p[0] == "gota":
                pygame.draw.line(s, (80, 140, 240), (int(p[1]), int(p[2])), (int(p[1]) - 2, int(p[2]) + 14), 4)
            else:
                pygame.draw.circle(s, (110, 106, 116), (int(p[1]), int(p[2])), 12)
                pygame.draw.circle(s, (80, 76, 86), (int(p[1]), int(p[2])), 12, 2)

        self._barra(s, 30, 24, 440, self.hp_b_vis, "BARÓN FELUXE")
        self._barra(s, 760, 310, 480, self.hp_n_vis, "NUBI", True)
        if self.imaxe is not None:
            ix, iy = 500 + (330 - self.imaxe.get_width()) // 2, 30
            pygame.draw.rect(s, C.CAJA_BORDE, (ix - 6, iy - 6, self.imaxe.get_width() + 12, self.imaxe.get_height() + 12),
                             border_radius=10)
            s.blit(self.imaxe, (ix, iy))

        if self.estado == "pregunta" and self.panel:
            self.panel.debuxar(s)
        else:
            tx.caja(s, CAIXA)
            if self.estado in ("mensaxe", "anim"):
                txt = self.txt[:int(self.letras)] if self.estado == "mensaxe" else self.txt
                tx.parrafo(s, self.f.g, txt, (50, 480, ANCHO - 100, 180))
                if self.estado == "mensaxe" and self.letras >= len(self.txt) and int(self.t * 3) % 2 == 0:
                    tx.texto(s, self.f.m, "Toca para continuar", (ANCHO - 330, 650), C.CAJA_BORDE)
                    tx.triangulo(s, ANCHO - 70, 660, (232, 72, 56), t=22)
            elif self.estado == "derrota":
                tx.parrafo(s, self.f.g, self.txt, (50, 480, ANCHO - 100, 80))
                for b in self.botons:
                    b.debuxar(s, self.j)
        self.esquina.draw(s)
