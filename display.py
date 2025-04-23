#coding:utf-8

import pygame as ga

class Display:

    """
    Classe permettant de gérer l'affichage de l'écran 64x32 du CHIP-8
    """

    def __init__(self):
        """
        Constructeur de la classe Display
        """
        # Initialisation de Pygame
        ga.init()

        # Création de la fenêtre
        self.window = ga.display.set_mode((640, 320))

        # Remplissage de la fenêtre avec du noir (les pixels étant noirs par défaut)
        self.window.fill((0, 0, 0))

        # Création d'un tableau de 32x64 pour le buffer d'affichage
        self.Win_Buffer = [[0 for _ in range(64)] for _ in range(32)]

    def draw_px(self, X_pos, Y_pos, px):
        """
        Dessine un pixel à la position (x, y) avec une logique XOR.
        """
        if 0 <= X_pos < 64 and 0 <= Y_pos < 32:
            if px == 1:
                if self.Win_Buffer[Y_pos][X_pos] == 1:
                    self.Win_Buffer[Y_pos][X_pos] = 0
                else:
                    self.Win_Buffer[Y_pos][X_pos] = 1

            pixel_width = self.window.get_width() // 64
            pixel_height = self.window.get_height() // 32
            rect = ga.Rect(X_pos * pixel_width, Y_pos * pixel_height, pixel_width, pixel_height)
            color = (255, 255, 255) if self.Win_Buffer[Y_pos][X_pos] == 1 else (0, 0, 0)
            ga.draw.rect(self.window, color, rect)
            ga.display.update()