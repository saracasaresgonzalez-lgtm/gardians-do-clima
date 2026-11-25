"""Efectos de sonido chiptune generados por código (onda cadrada e ruído).

O audio pode abrirse con formatos moi distintos (no ordenador adoita ser
22050 Hz; no navegador, 48000 ou 192000 Hz). Para que soe ben en todos:
1) os sons gárdanse como ficheiros WAV temporais e SDL adáptaos ao formato real;
2) se iso falla, xéranse directamente á frecuencia e canles do audio aberto.
No navegador o audio só se activa despois dun toque: se non está listo,
reinténtase ao tocar.
"""
import array
import os
import random
import struct
import tempfile

import pygame

SR = 22050

RECEITAS = {
    "texto": ([(1200, 0.015)], 0.05, "cadrada"),
    "blip": ([(880, 0.03), (1320, 0.04)], 0.12, "cadrada"),
    "confirmar": ([(990, 0.05), (1320, 0.05)], 0.15, "cadrada"),
    "apagar": ([(660, 0.05), (440, 0.05), (330, 0.08)], 0.15, "cadrada"),
    "chispa": ([(1, 0.12)], 0.12, "ruido"),
    "risa": ([(300, 0.08), (0, 0.03), (260, 0.08), (0, 0.03), (220, 0.14)], 0.15, "cadrada"),
    "bonus": ([(523, 0.06), (659, 0.06), (784, 0.06), (1046, 0.14)], 0.15, "cadrada"),
    "error": ([(220, 0.12), (160, 0.18)], 0.15, "cadrada"),
    "viento": ([(1, 0.3)], 0.06, "ruido"),
    "cuenta": ([(660, 0.1)], 0.15, "cadrada"),
    "ya": ([(990, 0.25)], 0.15, "cadrada"),
}


def _mostras(segmentos, vol, forma, sr, canles=1):
    """Mostras PCM de 16 bits (enteiros con signo) á frecuencia sr."""
    buf = array.array("h")
    for freq, dur in segmentos:
        n = int(sr * dur)
        for i in range(n):
            if freq <= 0:
                v = 0.0
            elif forma == "ruido":
                v = random.uniform(-1, 1)
            else:
                v = 1.0 if (i * freq / sr) % 1 < 0.5 else -1.0
            env = min(1.0, (n - i) / (sr * 0.02))
            m = int(v * env * vol * 32767)
            for _ in range(canles):
                buf.append(m)
    return buf


def _wav(segmentos, vol, forma):
    datos = _mostras(segmentos, vol, forma, SR).tobytes()
    return (b"RIFF" + struct.pack("<I", 36 + len(datos)) + b"WAVE" +
            b"fmt " + struct.pack("<IHHIIHH", 16, 1, 1, SR, SR * 2, 2, 16) +
            b"data" + struct.pack("<I", len(datos)) + datos)


class Sonidos:
    def __init__(self):
        self.s = {}
        self._ultimo = {}
        self._ultimo_intento = -99.0
        self._preparar()
        # diagnóstico na consola: "bonus" debe durar 0.32 s
        print("Audio:", pygame.mixer.get_init(), "sons:", len(self.s),
              "bonus:", round(self.s["bonus"].get_length(), 2) if self.s else None)

    def _preparar(self):
        """Inicia o mixer (se fai falta) e carga os sons. Devolve True se hai son."""
        self.s = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except Exception:
            return False
        # 1) ficheiros WAV temporais (SDL convérteos ao formato do audio)
        try:
            carpeta = tempfile.mkdtemp(prefix="sons_")
            for nome, receita in RECEITAS.items():
                ruta = os.path.join(carpeta, nome + ".wav")
                with open(ruta, "wb") as fh:
                    fh.write(_wav(*receita))
                self.s[nome] = pygame.mixer.Sound(ruta)
            return True
        except Exception:
            self.s = {}
        # 2) mostras xeradas directamente no formato do audio aberto
        try:
            freq, formato, canles = pygame.mixer.get_init()
            if formato == -16:
                for nome, (segs, vol, forma) in RECEITAS.items():
                    self.s[nome] = pygame.mixer.Sound(buffer=_mostras(segs, vol, forma, freq, canles).tobytes())
        except Exception:
            self.s = {}
        return bool(self.s)

    def play(self, nombre, min_intervalo=0.0):
        if not self.s:
            ahora = pygame.time.get_ticks() / 1000
            if ahora - self._ultimo_intento < 2:
                return
            self._ultimo_intento = ahora
            if not self._preparar():
                return
        snd = self.s.get(nombre)
        if not snd:
            return
        ahora = pygame.time.get_ticks() / 1000
        if ahora - self._ultimo.get(nombre, -99) < min_intervalo:
            return
        self._ultimo[nombre] = ahora
        try:
            snd.play()
        except Exception:
            pass
