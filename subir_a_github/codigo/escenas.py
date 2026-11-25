"""Pantallas e fluxo do xogo: título, menú de misións, diálogos,
misión completada e resultados finais. Todo funciona tocando a pantalla."""
import json
import math
import os

import pygame

import datos
import texto as tx
import ui
from batalla import EscenaBatalla
from config import ANCHO, ALTO, HUD_ALTO, C, WEB
from lumes import EscenaLumes
from mapa import Decorado
from retos import (EscenaClasificar, EscenaOrdenar, EscenaUnir, EscenaColocar, EscenaMapaTempo,
                   EscenaQuiz, EscenaClimograma)

RUTA_RECORD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "record.json")


def cargar_record():
    try:
        with open(RUTA_RECORD, encoding="utf-8") as fh:
            return int(json.load(fh).get("nivel1", 0))
    except (OSError, ValueError, AttributeError):
        return 0


def guardar_record(puntos):
    try:
        with open(RUTA_RECORD, "w", encoding="utf-8") as fh:
            json.dump({"nivel1": puntos}, fh)
    except OSError:
        pass


def estrelas_de(res):
    total = res["acertos"] + res["erros"]
    ratio = res["acertos"] / total if total else 1.0
    if res.get("bosque") is not None:
        ratio = (ratio + res["bosque"]) / 2
    if res.get("ganou") is False:
        ratio = min(ratio, 0.5)
    return 3 if ratio >= 0.85 else 2 if ratio >= 0.6 else 1


def puntos_de(res):
    extra = res.get("puntos", 0)
    return res["acertos"] * 100 + extra + (300 if res.get("ganou") else 0)


# ---------------------------------------------------------------- fluxo


def ir_titulo(j):
    j.cambiar(EscenaTitulo(j))


def ir_menu(j):
    j.cambiar(EscenaMenu(j))


def novo_xogo(j):
    j.partida = {}
    j.cambiar(EscenaDialogo(j, datos.INTRO, lambda: iniciar_mision(j, 0)))


def iniciar_mision(j, idx):
    m = datos.MISIONS[idx]
    titulo = f"MISIÓN {idx + 1} · {m['titulo'].upper()}"
    res = {"acertos": 0, "erros": 0}

    def paso(k, r=None):
        if r:
            res["acertos"] += r.get("acertos", 0)
            res["erros"] += r.get("erros", 0)
            for clave in ("bosque", "ganou"):
                if clave in r:
                    res[clave] = r[clave]
            if "puntos" in r:
                res["puntos"] = res.get("puntos", 0) + r["puntos"] - r.get("acertos", 0) * 100
        if k >= len(m["pasos"]):
            j.cambiar(EscenaMisionCompleta(j, idx, res))
            return
        tipo, ref = m["pasos"][k]
        seg = lambda r2=None: paso(k + 1, r2)
        if tipo == "dialogo":
            j.cambiar(EscenaDialogo(j, getattr(datos, ref), seg))
        elif tipo == "clasificar":
            j.cambiar(EscenaClasificar(j, titulo, getattr(datos, ref), seg))
        elif tipo == "ordenar":
            j.cambiar(EscenaOrdenar(j, titulo, getattr(datos, ref), seg))
        elif tipo == "unir":
            j.cambiar(EscenaUnir(j, titulo, getattr(datos, ref), seg))
        elif tipo == "colocar":
            j.cambiar(EscenaColocar(j, titulo, getattr(datos, ref), seg))
        elif tipo == "mapatempo":
            j.cambiar(EscenaMapaTempo(j, titulo, seg))
        elif tipo == "quiz":
            j.cambiar(EscenaQuiz(j, titulo, ref, seg))
        elif tipo == "climograma":
            j.cambiar(EscenaClimograma(j, titulo, ref, seg))
        elif tipo == "lumes":
            j.cambiar(EscenaLumes(j, "Apaga os lumes!", ref, seg))
        elif tipo == "batalla":
            j.cambiar(EscenaBatalla(j, titulo, ref, seg))

    paso(0)


# ---------------------------------------------------------------- título


class EscenaTitulo:
    def __init__(self, j):
        self.j = j
        self.t = 0.0
        self.deco = Decorado(j.arte, 100)
        self.record = cargar_record()
        self.b_xogar = ui.Boton((ANCHO // 2 - 220, 430, 440, 96), "XOGAR", C.BOTON_VERDE, fonte="g")
        self.b_misions = ui.Boton((ANCHO // 2 - 220, 546, 440, 76), "ESCOLLER MISIÓN", C.BOTON, fonte="g")
        self.b_sair = ui.Boton((24, ALTO - 84, 150, 64), "Saír", C.BOTON_GRIS)
        self.b_sair.visible = not WEB   # no navegador péchase a pestana
        self.esquina = ui.BotonsEsquina(j, casa=False)

    def update(self, dt):
        self.t += dt
        ent = self.j.entrada
        if self.esquina.update():
            return
        if self.b_xogar.tocado(ent):
            self.j.sonidos.play("confirmar")
            novo_xogo(self.j)
        elif self.b_misions.tocado(ent):
            self.j.sonidos.play("confirmar")
            ir_menu(self.j)
        elif self.b_sair.tocado(ent) or (ent.tecla(pygame.K_ESCAPE) and not WEB):
            self.j.activo = False

    def draw(self, s):
        self.deco.draw(s)
        gx = (self.t * 70) % (ANCHO + 300) - 220
        s.blit(self.j.arte.imaxe("globo", 150, 184), (int(gx), 120 + int(math.sin(self.t * 2) * 8)))
        f = self.j.fuentes
        tx.titulo(s, f.t, "GARDIÁNS DO CLIMA", (ANCHO // 2, 110), grosor=6)
        s.blit(self.j.arte.imaxe("nubi", 210, 150), (ANCHO // 2 - 105, 180 + int(math.sin(self.t * 3) * 8)))
        tx.titulo(s, f.g, "Nivel 1: O tempo e o clima", (ANCHO // 2, 378), (255, 255, 255))
        self.b_xogar.debuxar(s, self.j)
        self.b_misions.debuxar(s, self.j)
        self.b_sair.debuxar(s, self.j)
        self.esquina.draw(s)
        if self.record:
            tx.texto(s, f.m, f"RÉCORD {self.record:05d}", (ANCHO - 260, ALTO - 64), C.AMARILLO, (20, 28, 60))


# ---------------------------------------------------------------- menú de misións


def debuxar_estrela(s, cx, cy, rad, chea):
    pts = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        rr = rad if k % 2 == 0 else rad * 0.45
        pts.append((cx + math.cos(ang) * rr, cy + math.sin(ang) * rr))
    pygame.draw.polygon(s, (255, 214, 60) if chea else (170, 176, 196), pts)
    pygame.draw.polygon(s, (150, 90, 20) if chea else (110, 116, 136), pts, 3)


class EscenaMenu:
    def __init__(self, j):
        self.j = j
        self.deco = Decorado(j.arte, 160)
        self.botons = []
        n = len(datos.MISIONS)
        for i in range(n):
            fila = 0 if i < 4 else 1
            na_fila = 4 if fila == 0 else n - 4
            w, h = 290, 268
            x0 = (ANCHO - (na_fila * w + (na_fila - 1) * 20)) // 2
            col = i if fila == 0 else i - 4
            self.botons.append((i, pygame.Rect(x0 + col * (w + 20), 108 + fila * (h + 18), w, h)))
        self.volver = ui.Boton((24, ALTO - 80, 200, 64), "<  Volver", C.BOTON_GRIS)
        self.esquina = ui.BotonsEsquina(j, casa=False)

    def update(self, dt):
        ent = self.j.entrada
        if self.esquina.update():
            return
        if self.volver.tocado(ent) or ent.tecla(pygame.K_ESCAPE):
            ir_titulo(self.j)
            return
        for i, r in self.botons:
            if ent.clic and r.collidepoint(ent.clic):
                self.j.sonidos.play("confirmar")
                iniciar_mision(self.j, i)
                return

    def draw(self, s):
        self.deco.draw(s)
        f = self.j.fuentes
        pygame.draw.rect(s, C.HUD, (0, 0, ANCHO, 92))
        tx.titulo(s, f.g, "ESCOLLE UNHA MISIÓN", (ANCHO // 2, 46))
        for i, r in self.botons:
            m = datos.MISIONS[i]
            tx.caja(s, r, fondo=(255, 251, 238))
            pygame.draw.rect(s, C.CAJA_BORDE, (r.x + 10, r.y + 10, r.w - 20, 40), border_radius=10)
            cab = f"MISIÓN {i + 1}  ·  páx. {m['paxinas']}"
            tx.texto(s, f.p, cab, (r.centerx, r.y + 16), C.AMARILLO, centro=True)
            img = self.j.arte.encaixar(m["icona"], 200, 110)
            s.blit(img, (r.centerx - img.get_width() // 2, r.y + 58))
            ft = f.m if f.m.size(m["titulo"])[0] <= r.w - 20 else f.p
            tx.parrafo(s, ft, m["titulo"], (r.x + 10, r.y + 172, r.w - 20, 64), centrado=True, max_lineas=2)
            est = self.j.partida.get(i, {}).get("estrelas", 0)
            for k in range(3):
                debuxar_estrela(s, r.centerx - 36 + k * 36, r.bottom - 22, 15, k < est)
        self.volver.debuxar(s, self.j)
        self.esquina.draw(s)


# ---------------------------------------------------------------- diálogos


class EscenaDialogo:
    LINEAS = 3

    def __init__(self, j, lineas, al_terminar):
        self.j = j
        self.al_terminar = al_terminar
        self.deco = Decorado(j.arte)
        self.t = 0.0
        self.paxinas = []
        for quen, txt in lineas:
            partes = tx.envolver(j.fuentes.g, txt, ANCHO - 90)
            for i in range(0, len(partes), self.LINEAS):
                self.paxinas.append((quen, partes[i:i + self.LINEAS]))
        self.i = 0
        self.letras = 0.0
        self.saltar = ui.Boton((ANCHO - 400, 16, 230, 60), "Saltar  >>", C.BOTON_GRIS)
        self.esquina = ui.BotonsEsquina(j)

    def _total(self):
        return sum(len(l) for l in self.paxinas[self.i][1])

    def update(self, dt):
        self.t += dt
        ent = self.j.entrada
        if self.esquina.update():
            return
        if self.saltar.tocado(ent):
            self.j.sonidos.play("confirmar")
            self.al_terminar()
            return
        antes = int(self.letras)
        self.letras = min(self._total(), self.letras + 55 * dt)
        if int(self.letras) // 3 != antes // 3 and self.letras < self._total():
            self.j.sonidos.play("texto")
        if ent.clic:
            if self.letras < self._total():
                self.letras = self._total()
            else:
                self.i += 1
                self.letras = 0
                self.j.sonidos.play("confirmar")
                if self.i >= len(self.paxinas):
                    self.al_terminar()

    def draw(self, s):
        if self.i >= len(self.paxinas):
            return
        self.deco.draw(s)
        quen, lineas = self.paxinas[self.i]
        nome, cor = datos.PERSONAJES[quen]
        f = self.j.fuentes
        if quen in ("baron", "tubito"):
            s.blit(self.j.arte.imaxe("globo", 230, 282), (960, 110 + int(math.sin(self.t * 2) * 10)))
        else:
            s.blit(self.j.arte.imaxe("nubi", 300, 214), (900, 200 + int(math.sin(self.t * 3) * 8)))

        tx.caja(s, (30, 252, 236, 236), fondo=(250, 246, 236))
        s.blit(self.j.arte.imaxe("retrato_" + quen, 216, 216), (40, 262))
        ancho_nome = f.g.size(nome)[0] + 40
        tx.caja(s, (30, 484, ancho_nome, 60), fondo=cor, borde=(30, 30, 50), sombra=False)
        tx.texto(s, f.g, nome, (50, 490), C.BLANCO)

        tx.caja(s, (16, 540, ANCHO - 32, 168))
        restantes = int(self.letras)
        for n, linea in enumerate(lineas):
            tx.texto(s, f.g, linea[:max(0, restantes)], (44, 560 + n * 46))
            restantes -= len(linea)
        if self.letras >= self._total() and int(self.t * 3) % 2 == 0:
            tx.texto(s, f.p, "Toca para continuar", (ANCHO - 290, 670), C.CAJA_BORDE)
            tx.triangulo(s, ANCHO - 70, 676, (232, 72, 56), t=22)
        self.saltar.debuxar(s, self.j)
        self.esquina.draw(s)


# ---------------------------------------------------------------- misión completada


class EscenaMisionCompleta:
    def __init__(self, j, idx, res):
        self.j = j
        self.idx = idx
        self.res = res
        self.t = 0.0
        self.deco = Decorado(j.arte, 170)
        self.estrelas = estrelas_de(res)
        self.puntos = puntos_de(res)
        anterior = j.partida.get(idx, {})
        if self.estrelas >= anterior.get("estrelas", 0):
            j.partida[idx] = {"estrelas": self.estrelas, "puntos": self.puntos}
        ultima = idx == len(datos.MISIONS) - 1
        self.b_seguir = ui.Boton((ANCHO // 2 + 20, 590, 400, 86),
                                 "Ver resultados  >" if ultima else "Seguinte misión  >", C.BOTON_VERDE, fonte="g")
        self.b_repetir = ui.Boton((ANCHO // 2 - 420, 590, 400, 86), "Repetir misión", C.BOTON, fonte="g")
        self.esquina = ui.BotonsEsquina(j)
        j.sonidos.play("bonus")

    def update(self, dt):
        self.t += dt
        ent = self.j.entrada
        if self.esquina.update() or self.t < 0.5:
            return
        if self.b_seguir.tocado(ent):
            self.j.sonidos.play("confirmar")
            if self.idx + 1 < len(datos.MISIONS):
                iniciar_mision(self.j, self.idx + 1)
            else:
                self.j.cambiar(EscenaFinal(self.j))
        elif self.b_repetir.tocado(ent):
            self.j.sonidos.play("confirmar")
            iniciar_mision(self.j, self.idx)

    def draw(self, s):
        self.deco.draw(s)
        f = self.j.fuentes
        m = datos.MISIONS[self.idx]
        tx.titulo(s, f.t, f"MISIÓN {self.idx + 1} COMPLETADA!", (ANCHO // 2, 70), grosor=5)
        tx.titulo(s, f.g, m["titulo"], (ANCHO // 2, 140), (255, 255, 255))
        for k in range(3):
            visible = self.t > 0.3 + k * 0.3
            debuxar_estrela(s, ANCHO // 2 - 110 + k * 110, 230, 46, visible and k < self.estrelas)
        tx.caja(s, (ANCHO // 2 - 330, 310, 660, 250))
        filas = [("Respostas correctas", str(self.res["acertos"])), ("Erros", str(self.res["erros"]))]
        if self.res.get("bosque") is not None:
            filas.append(("Bosque salvado", f"{int(self.res['bosque'] * 100)}%"))
        if self.res.get("ganou") is not None:
            filas.append(("Batalla", "Gañada!" if self.res["ganou"] else "Perdida"))
        filas.append(("Puntos", f"{self.puntos:05d}"))
        for i, (k, v) in enumerate(filas):
            cor = C.ERRO if k == "Puntos" else C.TEXTO
            tx.texto(s, f.g, k, (ANCHO // 2 - 300, 326 + i * 44), cor)
            tx.texto(s, f.g, v, (ANCHO // 2 + 300 - f.g.size(v)[0], 326 + i * 44), C.CAJA_BORDE)
        self.b_repetir.debuxar(s, self.j)
        self.b_seguir.debuxar(s, self.j)
        self.esquina.draw(s)


# ---------------------------------------------------------------- final


class EscenaFinal:
    def __init__(self, j):
        self.j = j
        self.t = 0.0
        self.deco = Decorado(j.arte, 170)
        self.total = sum(v["puntos"] for v in j.partida.values())
        self.estrelas = sum(v["estrelas"] for v in j.partida.values())
        self.nuevo_record = self.total > cargar_record()
        if self.nuevo_record:
            guardar_record(self.total)
        self.b_menu = ui.Boton((ANCHO // 2 - 220, 616, 440, 80), "Menú principal", C.BOTON, fonte="g")

    def update(self, dt):
        self.t += dt
        if self.t > 0.5 and self.b_menu.tocado(self.j.entrada):
            self.j.sonidos.play("confirmar")
            ir_titulo(self.j)

    def draw(self, s):
        self.deco.draw(s)
        f = self.j.fuentes
        tx.titulo(s, f.g, "PARABÉNS, GARDIÁNS DO CLIMA!", (ANCHO // 2, 50))
        s.blit(self.j.arte.imaxe("nubi", 160, 114), (60, 20 + int(math.sin(self.t * 3) * 6)))
        tx.caja(s, (170, 104, ANCHO - 340, 496))
        for i, m in enumerate(datos.MISIONS):
            y = 124 + i * 52
            tx.texto(s, f.g, f"{i + 1}. {m['titulo']}", (204, y))
            est = self.j.partida.get(i, {}).get("estrelas", 0)
            for k in range(3):
                debuxar_estrela(s, ANCHO - 330 + k * 44, y + 22, 18, k < est)
        pygame.draw.line(s, C.CAJA_LINEA, (204, 496 + 32), (ANCHO - 204, 496 + 32), 3)
        tx.texto(s, f.g, f"Estrelas: {self.estrelas}/{3 * len(datos.MISIONS)}", (204, 540), C.CAJA_BORDE)
        total = f"PUNTOS {self.total:05d}"
        tx.texto(s, f.g, total, (ANCHO - 204 - f.g.size(total)[0], 540), C.ERRO)
        if self.nuevo_record and int(self.t * 3) % 2 == 0:
            tx.titulo(s, f.g, "NOVO RÉCORD!", (ANCHO // 2, 600))
        self.b_menu.debuxar(s, self.j)
