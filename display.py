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

        # Dimensions de l'écran CHIP-8
        self.width = 64
        self.height = 32
        self.scale = 10

        # Création de la fenêtre
        self.window = ga.display.set_mode((self.width * self.scale, self.height * self.scale))

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        self.Win_Buffer = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.window.fill(self.black)

    def draw_px(self, X_pos, Y_pos, px):
        """
        Dessine un pixel à la position (x, y) avec une logique XOR.
        """
        if 0 <= X_pos < self.width and 0 <= Y_pos < self.height:
            if px == 1:
                self.Win_Buffer[Y_pos][X_pos] ^= 1

            rect = ga.Rect(X_pos * self.scale, Y_pos * self.scale, self.scale, self.scale)
            color = self.white if self.Win_Buffer[Y_pos][X_pos] == 1 else self.black
            ga.draw.rect(self.window, color, rect)
            ga.display.update()
