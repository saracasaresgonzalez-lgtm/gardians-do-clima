"""APAGA OS LUMES! (ronda arcade táctil da misión 5).

A Banda Tisne solta faíscas desde o dirixible. Ao tocar un lume, Nubi voa ata el
e aparece unha pregunta: se se acerta, chove e o lume apágase; se non, o lume medra.
Mentres se responde, o xogo detense (pensado para a pizarra dixital).
"""
import math
import random

import pygame

import datos
import texto as tx
import ui
from config import ANCHO, ALTO, TILE, HUD_ALTO, COLS, FILAS, C
from mapa import MAPA, INFLAMABLES, crear_chan, debuxar_vexetacion, rect_tile, centro_tile, tile_en
from preguntas import PanelPregunta

DIRECCIONS = [((0, -1), "Norte"), ((1, -1), "Nordés"), ((1, 0), "Leste"), ((1, 1), "Sueste"),
              ((0, 1), "Sur"), ((-1, 1), "Sudoeste"), ((-1, 0), "Oeste"), ((-1, -1), "Noroeste")]
FORZAS = ["en calma", "frouxo", "forte"]

# Dificultade (o xogo para mentres se responde)
DURACION = 75.0
MAX_LUMES = 10
PROB_PROPAGAR = 0.6


def _circulo_alfa(r, cor, alfa):
    s = pygame.Surface((r * 2 + 1, r * 2 + 1), pygame.SRCALPHA)
    pygame.draw.circle(s, (*cor, alfa), (r, r), r)
    return s


class Part:
    __slots__ = ("tipo", "x", "y", "vx", "vy", "vida", "vmax")

    def __init__(self, tipo, x, y, vx, vy, vida):
        self.tipo, self.x, self.y, self.vx, self.vy = tipo, x, y, vx, vy
        self.vida = self.vmax = vida


class EscenaLumes:
    def __init__(self, j, titulo, pool, al_terminar):
        self.j = j
        self.titulo = titulo
        self.banco = j.bancos[pool]
        self.al_terminar = al_terminar
        self.arte = j.arte
        self.f = j.fuentes
        self.snd = j.sonidos

        self.grid = [list(fila) for fila in MAPA]
        self.total_veg = sum(ch in INFLAMABLES for fila in MAPA for ch in fila)
        self.chan = crear_chan()
        self.veg = debuxar_vexetacion(self.arte, self.grid)
        self.tiles_agua = [(c, r) for r in range(FILAS) for c in range(COLS) if MAPA[r][c] == "A"]
        self.tiles_prado = [(c, r) for r in range(FILAS) for c in range(COLS) if MAPA[r][c] == "g"]

        self.t = 0.0
        self.tempo = DURACION
        self.conta = 3.5
        self.ultimo_num = None
        self.fin = None
        self.t_fin = 0.0
        self.banner = False
        self.boton = ui.Boton((ANCHO // 2 - 140, 470, 280, 70), "Continuar  >", C.BOTON_LARANXA)
        self.esquina = ui.BotonsEsquina(j, y=12)

        self.gx, self.gy = 640.0, 520.0
        self.destino = None
        self.obxectivo = None
        self.panel = None
        self.chovendo = 0.0
        self.alvo_chuvia = None

        self.acertos = self.erros = self.puntos = self.apagados = 0
        self.lumes = {}
        self.parts = []
        self.chispas = []
        self.arcos = []
        self.globo = None
        self.t_globo = 9.0
        self.raio = None
        self.t_raio = 14.0
        self.vento = (1.0, 0.0)
        self.vento_f = 1
        self.t_vento = 22.0
        self.toasts = []
        self.vistos = set()
        self.acum_amb = 0.0

        self.img_fume = [_circulo_alfa(r, (96, 92, 100), 120) for r in range(6, 18, 2)]
        self.img_vapor = [_circulo_alfa(r, (244, 248, 255), 180) for r in range(6, 18, 2)]
        self.img_sombra = pygame.Surface((80, 22), pygame.SRCALPHA)
        pygame.draw.ellipse(self.img_sombra, (0, 0, 0, 70), (0, 0, 80, 22))
        self.nubi = self.arte.imaxe("nubi", 112, 80)
        self.nubi_gris = self.arte.imaxe("nubi_gris", 112, 80)
        self.globo_img = self.arte.imaxe("globo", 96, 118)
        self.lume_peq = [pygame.transform.smoothscale(self.arte.imaxe(f"lume{k}"), (30, 38)) for k in range(3)]

        matos = [(c, r) for r in range(FILAS) for c in range(COLS) if MAPA[r][c] == "B"]
        for c, r in random.sample(matos, 2):
            self._acender(c, r, son=False)

    # ------------------------------------------------------------ axudas

    def rect_nube(self):
        bob = int(math.sin(self.t * 3) * 4)
        return pygame.Rect(int(self.gx) - 56, int(self.gy) - 96 + bob, 112, 80)

    def bosque(self):
        queimados = sum(ch == "Q" for fila in self.grid for ch in fila)
        return (self.total_veg - queimados) / self.total_veg

    def tip(self, clave):
        if clave not in self.vistos:
            self.vistos.add(clave)
            self.toasts.append([datos.TIPS[clave], 4.5])

    def avisar(self, txt, dur=3.0):
        self.toasts.append([txt, dur])

    # ------------------------------------------------------------ bucle

    def update(self, dt):
        ent = self.j.entrada
        if self.panel:
            self.panel.update(dt)
            if self.panel.rematado:
                acerto = self.panel.acerto
                self.panel = None
                self._resolver(acerto)
            return
        if self.esquina.update():
            return
        if self.banner:
            if self.boton.tocado(ent):
                self.snd.play("confirmar")
                self.al_terminar({"acertos": self.acertos, "erros": self.erros, "bosque": self.bosque(),
                                  "puntos": self.puntos})
            return

        self.t += dt
        self._particulas(dt)
        for a in self.arcos:
            a["t"] -= dt
        self.arcos = [a for a in self.arcos if a["t"] > 0]

        if self.conta > 0:
            self.conta -= dt
            num = 3 if self.conta > 2.5 else 2 if self.conta > 1.5 else 1 if self.conta > 0.5 else 0
            if num != self.ultimo_num:
                self.ultimo_num = num
                self.snd.play("ya" if num == 0 else "cuenta")
            if self.conta <= 0:
                self.tip("inicio")
            return

        if self.fin is not None:
            self.t_fin += dt
            if self.t_fin > 2.2:
                self.banner = True
            return

        self.tempo -= dt
        if ent.clic:
            self._tocar(ent.clic)
        self._mover(dt)
        self._chover(dt)
        self._lumes(dt)
        self._mover_globo(dt)
        self._mover_chispas(dt)
        self._raio_sol(dt)
        self._cambiar_vento(dt)
        if self.toasts:
            self.toasts[0][1] -= dt * (2 if len(self.toasts) > 2 else 1)
            if self.toasts[0][1] <= 0:
                self.toasts.pop(0)
        if self.tempo <= 0:
            self.tempo = 0
            self.fin = "TEMPO!"
            self.snd.play("bonus")

    # ------------------------------------------------------------ toques e movemento

    def _tocar(self, pos):
        if pos[1] < HUD_ALTO or self.chovendo > 0:
            return
        g = self.globo
        if g and g["estado"] == "cruza" and pygame.Rect(g["x"], g["y"], 96, 118).inflate(30, 30).collidepoint(pos):
            self.obxectivo = ("globo", None)
            self.snd.play("texto")
            return
        mellor, dist = None, 99
        for (c, r) in self.lumes:
            cx, cy = centro_tile(c, r)
            d = math.hypot(pos[0] - cx, pos[1] - cy + 10)
            if d < 40 and d < dist:
                mellor, dist = (c, r), d
        if mellor:
            self.obxectivo = ("lume", mellor)
            self.destino = centro_tile(*mellor)
        elif self.raio and rect_tile(self.raio["c"], self.raio["r"]).inflate(30, 30).collidepoint(pos):
            self.obxectivo = ("raio", None)
            self.destino = centro_tile(self.raio["c"], self.raio["r"])
        else:
            self.obxectivo = None
            self.destino = pos
        self.snd.play("texto")

    def _mover(self, dt):
        if self.obxectivo and self.obxectivo[0] == "globo":
            g = self.globo
            if not g or g["estado"] != "cruza":
                self.obxectivo = None
            else:
                self.destino = (g["x"] + 48, g["y"] + 140)
        if not self.destino:
            return
        self.destino = (max(60, min(ANCHO - 60, self.destino[0])), max(HUD_ALTO + 100, min(ALTO - 10, self.destino[1])))
        dx, dy = self.destino[0] - self.gx, self.destino[1] - self.gy
        d = math.hypot(dx, dy)
        paso = 380 * dt
        if d <= max(paso, 4):
            self.gx, self.gy = self.destino
            self.destino = None
            self._chegar()
        else:
            self.gx += dx / d * paso
            self.gy += dy / d * paso

    def _chegar(self):
        if not self.obxectivo:
            return
        tipo, ref = self.obxectivo
        valido = ((tipo == "lume" and ref in self.lumes) or
                  (tipo == "globo" and self.globo and self.globo["estado"] == "cruza") or
                  (tipo == "raio" and self.raio))
        if not valido:
            self.obxectivo = None
            return
        cab = {"lume": "PARA APAGAR O LUME, RESPONDE BEN:",
               "globo": "PARA MOLLAR O DIRIXIBLE, RESPONDE BEN:",
               "raio": "PARA CREAR UN ARCO DA VELLA, RESPONDE BEN:"}[tipo]
        self.panel = PanelPregunta(self.j, self.banco.seguinte(), cab)

    def _resolver(self, acerto):
        tipo, ref = self.obxectivo
        self.obxectivo = None
        if acerto:
            self.acertos += 1
            self.puntos += 100
            if tipo == "lume":
                self.chovendo = 1.0
                self.alvo_chuvia = ref
            elif tipo == "globo" and self.globo:
                self.globo["estado"] = "foxe"
                self.globo["frase"] = [random.choice(datos.QUIPS_HUIDA), 2.4]
                self.puntos += 50
                self.snd.play("risa")
            elif tipo == "raio" and self.raio:
                rt = rect_tile(self.raio["c"], self.raio["r"])
                self.arcos.append({"x": rt.centerx, "y": rt.bottom, "t": 3.5})
                self.raio = None
                self.t_raio = random.uniform(12, 16)
                self.puntos += 50
                self.tip("arco")
        else:
            self.erros += 1
            if tipo == "lume" and ref in self.lumes:
                self.lumes[ref]["int"] = 1.0
                self._propagar(*ref)
                self.tip("medrou")
            elif tipo == "globo" and self.globo:
                self._soltar_chispa(self.globo)
            elif tipo == "raio":
                self.raio = None
                self.t_raio = random.uniform(12, 16)
                self.avisar("O raio de sol desapareceu...")

    def _chover(self, dt):
        if self.chovendo <= 0:
            return
        nube = self.rect_nube()
        for _ in range(4):
            x = self.gx + random.uniform(-40, 40)
            vida = (self.gy + random.uniform(-8, 8) - nube.bottom) / 380
            self.parts.append(Part("gota", x, nube.bottom - 6, random.uniform(-8, 8), 380, max(0.05, vida)))
        self.chovendo -= dt
        if self.chovendo <= 0 and self.alvo_chuvia in self.lumes:
            c, r = self.alvo_chuvia
            del self.lumes[self.alvo_chuvia]
            self.alvo_chuvia = None
            self.apagados += 1
            self.snd.play("apagar")
            self.tip("apagado")
            x, y = centro_tile(c, r)
            for _ in range(6):
                self.parts.append(Part("vapor", x + random.uniform(-10, 10), y - 10, random.uniform(-12, 12), -45, 1.0))

    # ------------------------------------------------------------ lume

    def _acender(self, c, r, son=True):
        if self.grid[r][c] in INFLAMABLES and (c, r) not in self.lumes and len(self.lumes) < MAX_LUMES:
            self.lumes[(c, r)] = {"int": 0.2, "cheo": 0.0, "prop": 3.0}
            if son:
                self.snd.play("chispa", 0.2)

    def _lumes(self, dt):
        queimou = False
        for clave in list(self.lumes):
            fu = self.lumes[clave]
            c, r = clave
            mato = self.grid[r][c] == "B"
            fu["int"] = min(1.0, fu["int"] + (0.25 if mato else 0.12) * dt * (1 + 0.4 * self.vento_f))
            if fu["int"] < 1.0:
                continue
            fu["cheo"] += dt
            fu["prop"] -= dt
            if fu["prop"] <= 0:
                fu["prop"] = random.uniform(7, 9) / (1 + 0.4 * self.vento_f)
                if random.random() < PROB_PROPAGAR:
                    self._propagar(c, r)
            if fu["cheo"] > (16 if mato else 22) and clave != self.alvo_chuvia:
                self.grid[r][c] = "Q"
                del self.lumes[clave]
                queimou = True
                x, y = centro_tile(c, r)
                for _ in range(4):
                    self.parts.append(Part("fume", x, y - 10, random.uniform(-10, 10), -30, 1.6))
        if queimou:
            self.veg = debuxar_vexetacion(self.arte, self.grid, self.veg)

    def _propagar(self, c, r):
        wx, wy = self.vento
        cands, pesos = [], []
        for dc in (-1, 0, 1):
            for dr in (-1, 0, 1):
                nc, nr = c + dc, r + dr
                if (dc or dr) and 0 <= nc < COLS and 0 <= nr < FILAS:
                    ch = self.grid[nr][nc]
                    if ch in INFLAMABLES and (nc, nr) not in self.lumes:
                        alineado = (dc * wx + dr * wy) / math.hypot(dc, dr)
                        w = 1 + max(0.0, alineado) * 3 * self.vento_f
                        if ch == "B":
                            w *= 1.6
                        if dc and dr:
                            w *= 0.6
                        cands.append((nc, nr))
                        pesos.append(w)
        if cands:
            self._acender(*random.choices(cands, pesos)[0])

    # ------------------------------------------------------------ Banda Tisne

    def _mover_globo(self, dt):
        if self.globo is None:
            self.t_globo -= dt
            if self.t_globo <= 0:
                d = random.choice((-1, 1))
                y0 = HUD_ALTO + 10 + random.uniform(0, 70)
                self.globo = {"x": -100 if d > 0 else ANCHO + 4, "y0": y0, "y": y0, "dir": d, "estado": "cruza",
                              "t_chispa": 2.0, "frase": None, "restantes": 2, "primeira": True}
                self.tip("globo")
                self.snd.play("risa")
            return
        g = self.globo
        if g["frase"]:
            g["frase"][1] -= dt
            if g["frase"][1] <= 0:
                g["frase"] = None
        if g["estado"] == "cruza":
            g["x"] += g["dir"] * 80 * dt
            g["y"] = g["y0"] + math.sin(self.t * 2.2) * 8
            g["t_chispa"] -= dt
            if g["t_chispa"] <= 0 and g["restantes"] > 0 and 0 < g["x"] + 48 < ANCHO:
                g["t_chispa"] = random.uniform(3.0, 4.5)
                if self._soltar_chispa(g):
                    g["restantes"] -= 1
                    if g["primeira"]:
                        g["frase"] = [random.choice(datos.QUIPS_CHISPA), 2.4]
                    g["primeira"] = False
            if g["x"] > ANCHO + 110 or g["x"] < -110:
                self.globo = None
                self.t_globo = random.uniform(12, 16)
        else:
            g["x"] += g["dir"] * 150 * dt
            g["y"] -= 120 * dt
            if g["y"] < -150:
                self.globo = None
                self.t_globo = random.uniform(13, 17)

    def _soltar_chispa(self, g):
        c0 = int((g["x"] + 48) // TILE)
        for c in (c0, c0 - 1, c0 + 1, c0 - 2, c0 + 2):
            if not 0 <= c < COLS:
                continue
            filas = [r for r in range(FILAS) if self.grid[r][c] in INFLAMABLES and (c, r) not in self.lumes]
            if filas:
                pesos = [3 if self.grid[r][c] == "B" else 1 for r in filas]
                r = random.choices(filas, pesos)[0]
                tx_, ty_ = centro_tile(c, r)
                self.chispas.append({"x": g["x"] + 48, "y": g["y"] + 112, "tx": tx_, "ty": ty_})
                return True
        return False

    def _mover_chispas(self, dt):
        for ch in list(self.chispas):
            dx, dy = ch["tx"] - ch["x"], ch["ty"] - ch["y"]
            dist = math.hypot(dx, dy)
            paso = 150 * dt
            if dist <= paso:
                self.chispas.remove(ch)
                self._acender(*tile_en(ch["tx"], ch["ty"]))
            else:
                ch["x"] += dx / dist * paso
                ch["y"] += dy / dist * paso

    # ------------------------------------------------------------ sol e vento

    def _raio_sol(self, dt):
        if self.raio is None:
            self.t_raio -= dt
            if self.t_raio <= 0:
                c, r = random.choice(self.tiles_prado)
                self.raio = {"c": c, "r": r, "t": 12.0}
                self.tip("raio")
        else:
            self.raio["t"] -= dt
            if self.raio["t"] <= 0 and self.obxectivo != ("raio", None):
                self.raio = None
                self.t_raio = random.uniform(12, 16)

    def _cambiar_vento(self, dt):
        self.t_vento -= dt
        if self.t_vento > 0:
            return
        self.t_vento = random.uniform(18, 24)
        (dx, dy), nome = random.choice(DIRECCIONS)
        h = math.hypot(dx, dy)
        self.vento = (dx / h, dy / h)
        self.vento_f = random.choice((0, 1, 1, 2))
        self.snd.play("viento")
        if "vento" not in self.vistos:
            self.tip("vento")
        elif self.vento_f == 0:
            self.avisar("A veleta está quieta: o vento está en calma.")
        else:
            self.avisar(f"A veleta xira: vento {FORZAS[self.vento_f]} cara ao {nome}.")

    # ------------------------------------------------------------ partículas

    def _particulas(self, dt):
        self.acum_amb += 5 * dt
        while self.acum_amb >= 1:
            self.acum_amb -= 1
            c, r = random.choice(self.tiles_agua)
            x, y = centro_tile(c, r)
            self.parts.append(Part("vaporlago", x + random.uniform(-16, 16), y + random.uniform(-16, 16), 0, -30, 1.6))
        for (c, r), fu in self.lumes.items():
            if random.random() < dt * 3 * fu["int"]:
                x, y = centro_tile(c, r)
                self.parts.append(Part("fume", x + random.uniform(-8, 8), y - 30, self.vento[0] * self.vento_f * 15, -35, 1.5))
        novas = []
        for p in self.parts:
            p.x += p.vx * dt
            p.y += p.vy * dt
            p.vida -= dt
            if p.tipo == "gota" and p.vida <= 0:
                novas.append(Part("salpica", p.x, p.y, 0, 0, 0.18))
        self.parts = [p for p in self.parts if p.vida > 0] + novas
        if len(self.parts) > 700:
            self.parts = self.parts[-700:]

    # ------------------------------------------------------------ debuxo

    def draw(self, s):
        s.blit(self.chan, (0, HUD_ALTO))
        fase = int(self.t * 3)
        for (c, r) in self.tiles_agua[::2]:
            x, y = centro_tile(c, r)
            ox = ((c * 7 + r * 5 + fase) % 5) * 4 - 8
            pygame.draw.line(s, C.AGUA_CLARA, (x + ox - 8, y), (x + ox + 8, y), 3)
        if self.raio:
            self._debuxar_raio(s)
        s.blit(self.veg, (0, HUD_ALTO))
        for (c, r), fu in sorted(self.lumes.items(), key=lambda kv: kv[0][1]):
            k = int(self.t * 8 + c + r) % 3
            x, y = centro_tile(c, r)
            if fu["int"] < 0.5:
                s.blit(self.lume_peq[k], (x - 15, y - 30))
            else:
                s.blit(self.arte.imaxe(f"lume{k}"), (x - 22, y - 48))
            if self.obxectivo == ("lume", (c, r)):
                pygame.draw.circle(s, C.AMARILLO, (x, y - 10), 30, 4)
        for ch in self.chispas:
            col = C.AMARILLO if int(self.t * 20) % 2 else C.NARANJA
            pygame.draw.circle(s, col, (int(ch["x"]), int(ch["y"])), 6)
            pygame.draw.circle(s, (200, 60, 20), (int(ch["x"]), int(ch["y"])), 6, 2)

        s.blit(self.img_sombra, (int(self.gx) - 40, int(self.gy) - 11))
        for a in self.arcos:
            self._debuxar_arco(s, a)
        self._debuxar_particulas(s)
        nube = self.rect_nube()
        s.blit(self.nubi_gris if self.chovendo > 0 else self.nubi, nube.topleft)

        g = self.globo
        if g:
            s.blit(self.globo_img, (int(g["x"]), int(g["y"])))
            if g["frase"]:
                tx.bocadillo(s, self.f.p, g["frase"][0], (int(g["x"]) + 48, int(g["y"]) + 118))

        self._hud(s)
        self._debuxar_toast(s)

        if self.conta > 0:
            num = 3 if self.conta > 2.5 else 2 if self.conta > 1.5 else 1 if self.conta > 0.5 else 0
            tx.titulo(s, self.f.g, self.titulo.upper(), (ANCHO // 2, ALTO // 2 - 90), (255, 255, 255))
            tx.titulo(s, self.f.t, str(num) if num else "XA!", (ANCHO // 2, ALTO // 2))
        if self.fin and not self.banner:
            tx.titulo(s, self.f.t, self.fin, (ANCHO // 2, ALTO // 2))
        if self.banner:
            ui.velo(s, 130)
            tx.caja(s, (ANCHO // 2 - 320, 150, 640, 420))
            tx.titulo(s, self.f.g, "RONDA REMATADA", (ANCHO // 2, 196))
            filas = [("Bosque salvado", f"{int(self.bosque() * 100)}%"), ("Lumes apagados", str(self.apagados)),
                     ("Respostas correctas", str(self.acertos)), ("Respostas incorrectas", str(self.erros))]
            for i, (k, v) in enumerate(filas):
                tx.texto(s, self.f.m, k, (ANCHO // 2 - 270, 250 + i * 46))
                tx.texto(s, self.f.m, v, (ANCHO // 2 + 270 - self.f.m.size(v)[0], 250 + i * 46), C.CAJA_BORDE)
            self.boton.debuxar(s, self.j)
        if self.panel:
            self.panel.debuxar(s)

    def _debuxar_raio(self, s):
        rt = rect_tile(self.raio["c"], self.raio["r"])
        alto = rt.bottom - HUD_ALTO
        haz = pygame.Surface((TILE + 20, alto), pygame.SRCALPHA)
        parpadeo = 70 + int(30 * math.sin(self.t * 6))
        haz.fill((255, 236, 120, parpadeo))
        pygame.draw.rect(haz, (255, 248, 200, parpadeo + 50), (18, 0, 24, alto))
        s.blit(haz, (rt.x - 10, HUD_ALTO))
        for i in range(4):
            yy = rt.bottom - 6 - ((self.t * 80 + i * 50) % alto)
            pygame.draw.circle(s, (255, 255, 255), (rt.x + 6 + i * 10, int(yy)), 3)

    def _debuxar_particulas(self, s):
        for p in self.parts:
            x, y = int(p.x), int(p.y)
            if p.tipo == "gota":
                pygame.draw.line(s, (90, 150, 240), (x, y), (x - 1, y + 10), 3)
            elif p.tipo == "salpica":
                pygame.draw.circle(s, C.AGUA_CLARA, (x - 4, y), 2)
                pygame.draw.circle(s, C.AGUA_CLARA, (x + 4, y), 2)
            elif p.tipo == "vaporlago":
                pygame.draw.circle(s, (230, 244, 255) if p.vida > p.vmax * 0.3 else (180, 214, 245), (x, y), 3)
            elif p.tipo in ("fume", "vapor"):
                imgs = self.img_fume if p.tipo == "fume" else self.img_vapor
                img = imgs[min(len(imgs) - 1, int((1 - p.vida / p.vmax) * len(imgs)))]
                s.blit(img, (x - img.get_width() // 2, y - img.get_height() // 2))

    def _debuxar_arco(self, s, a):
        capa = pygame.Surface((160, 84), pygame.SRCALPHA)
        cores = [(232, 64, 64), (248, 152, 40), (248, 224, 64), (88, 200, 88), (72, 144, 232), (144, 88, 208)]
        for i, cor in enumerate(cores):
            rad = 76 - i * 7
            pygame.draw.circle(capa, cor, (80, 80), rad, 7, draw_top_left=True, draw_top_right=True)
        capa.set_alpha(int(255 * min(1, a["t"] / 1.0)))
        s.blit(capa, (a["x"] - 80, a["y"] - 80))

    def _hud(self, s):
        f = self.f.m
        pygame.draw.rect(s, C.HUD, (0, 0, ANCHO, HUD_ALTO))
        pygame.draw.rect(s, C.HUD_BORDE, (0, HUD_ALTO - 4, ANCHO, 4))
        ty = (HUD_ALTO - f.get_height()) // 2
        tx.texto(s, f, self.titulo.upper(), (20, ty), C.AMARILLO)
        x = 330
        s.blit(self.arte.imaxe("arbore0", 40, 46), (x, 12))
        b = self.bosque()
        colb = (140, 236, 140) if b >= 0.75 else C.AMARILLO if b >= 0.5 else C.ROJO
        x += 50 + tx.texto(s, f, f"{int(b * 100)}%", (x + 50, ty), colb) + 30
        pygame.draw.circle(s, C.BLANCO, (x + 16, 40), 16, 3)
        pygame.draw.line(s, C.BLANCO, (x + 16, 40), (x + 16, 30), 3)
        pygame.draw.line(s, C.BLANCO, (x + 16, 40), (x + 24, 40), 3)
        mm, ss = divmod(math.ceil(self.tempo), 60)
        x += 42 + tx.texto(s, f, f"{mm}:{ss:02d}", (x + 42, ty), C.ROJO if self.tempo < 15 else C.BLANCO) + 30
        tx.texto(s, f, f"{self.puntos:05d} puntos", (x, ty), C.AMARILLO)
        cx, cy = ANCHO - 190, 40
        tx.texto(s, f, "VENTO", (cx - 40 - f.size("VENTO")[0], ty), C.BLANCO)
        pygame.draw.circle(s, (30, 44, 90), (cx, cy), 30)
        pygame.draw.circle(s, C.HUD_BORDE, (cx, cy), 30, 3)
        colv = [C.GRIS, C.AMARILLO, C.ROJO][self.vento_f]
        if self.vento_f == 0:
            pygame.draw.circle(s, colv, (cx, cy), 6)
        else:
            dx, dy = self.vento
            punta = (cx + dx * 22, cy + dy * 22)
            pygame.draw.line(s, colv, (cx - dx * 18, cy - dy * 18), punta, 6)
            for ang in (2.5, -2.5):
                ca, sa = math.cos(ang), math.sin(ang)
                bx, by = dx * ca - dy * sa, dx * sa + dy * ca
                pygame.draw.line(s, colv, punta, (punta[0] + bx * 14, punta[1] + by * 14), 6)
        self.esquina.draw(s)

    def _debuxar_toast(self, s):
        if not self.toasts:
            return
        f = self.f.m
        lineas = tx.envolver(f, self.toasts[0][0], ANCHO - 120)
        lh = f.get_linesize()
        h = 28 + len(lineas) * lh
        y = HUD_ALTO + 10 if self.gy > ALTO - 160 else ALTO - h - 12
        tx.caja(s, (30, y, ANCHO - 60, h))
        for i, l in enumerate(lineas):
            tx.texto(s, f, l, (56, y + 14 + i * lh))
