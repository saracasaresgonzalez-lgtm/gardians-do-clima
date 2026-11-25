"""Entrada táctil (pizarra dixital) e rato.

No ordenador, as pizarras táctiles envían os toques como clics do rato.
No navegador lense tamén os eventos de dedo (FINGER), que traen sempre a
posición exacta do toque.
"""
import pygame

from config import ANCHO, ALTO, WEB


class Entrada:
    def __init__(self):
        self.pos = (0, 0)        # posición actual do dedo/rato
        self.premido = False     # o dedo está apoiado
        self.clic = None         # posición onde se tocou neste fotograma
        self.soltar = None       # posición onde se levantou o dedo neste fotograma
        self.teclas = set()

    def procesar(self, eventos):
        self.clic = None
        self.soltar = None
        self.teclas = set()
        for e in eventos:
            if WEB and e.type in (pygame.FINGERDOWN, pygame.FINGERUP, pygame.FINGERMOTION):
                pos = (int(e.x * ANCHO), int(e.y * ALTO))
                if e.type == pygame.FINGERDOWN:
                    self.clic = self.pos = pos
                    self.premido = True
                elif e.type == pygame.FINGERUP:
                    self.soltar = self.pos = pos
                    self.premido = False
                else:
                    self.pos = pos
            elif WEB and getattr(e, "touch", False):
                continue   # rato simulado a partir dun toque: xa o lemos como dedo
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                self.clic = self.pos = e.pos
                self.premido = True
            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                self.soltar = self.pos = e.pos
                self.premido = False
            elif e.type == pygame.MOUSEMOTION:
                self.pos = e.pos
            elif e.type == pygame.KEYDOWN:
                self.teclas.add(e.key)
            elif e.type == pygame.WINDOWFOCUSLOST:
                self.premido = False

    def tecla(self, k):
        return k in self.teclas
