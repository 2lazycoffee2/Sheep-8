#coding:utf-8

import pygame as ga

ga.init()


class Display:

    def __init__(self) : 
        
        """
        Constructeur de la classe Display : 
        """

        #Valeurs d'échelle et de taille
        self.scale = 10
        self.height = 64
        self.width = 32

        #Initialisation de la fenêtre
        self.Window = ga.display.set_mode((self.height*self.scale, self.width*self.scale))

        #Couleurs
        self.bgcolor =  (0, 0, 0)
        self.spritecolor = (255, 255, 255)

    

    def Draw_pixel(self, Win_buffer):

        """
        Methode de dessin des pixels :
        """

        for i in range(self.height):
            for j in range(self.width):             # Ces deux boucles parcourent toute les cellules de la matrice win_buffer
                if Win_buffer[j][i] == 1:
                    ga.draw.rect(self.Window, self.spritecolor, [i*self.scale,j*self.scale, self.scale, self.scale], 0) # Si un des coefficients de la matrice est à un, on allume un pixel de la couleur voulue) 
                else:
                    ga.draw.rect(self.Window, self.bgcolor, [i*self.scale,j*self.scale, self.scale, self.scale], 0)     # Sinon, on dessine un pixel noir.
        ga.display.update () # rafraichissement.

    def set_fullscreen(self, enabled: bool):
        """
        Active ou désactive le mode plein écran pour la fenêtre pygame, en adaptant l'affichage à la résolution de l'écran.
        """
        ga.display.quit()
        ga.display.init()
        flags = ga.FULLSCREEN | ga.SCALED if enabled else 0
        size = (self.height * self.scale, self.width * self.scale)
        self.Window = ga.display.set_mode(size, flags)
        self.fullscreen = enabled
