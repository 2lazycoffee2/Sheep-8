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

        self.window.fill(self.black)
        ga.display.update()

    def Draw_pixel(self, Win_Buffer):
        """
        Dessine un pixel à la position (x, y)
        """
        for y in range(self.height):
            for x in range(self.width):
                color = self.white if Win_Buffer[y][x] == 1 else self.black
                rect = ga.Rect(x * self.scale, y * self.scale, self.scale, self.scale)
                ga.draw.rect(self.window, color, rect)

        ga.display.update()
