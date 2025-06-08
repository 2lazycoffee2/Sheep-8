#coding:utf-8

import pygame as ga

ga.init()


class Display:

    def __init__(self) : #Win_buffer): #Window, scale, Win_buffer):
        
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
        self.Black =  (0, 0, 0)
        self.White = (255, 255, 255)

        #self.Win_buffer = Win_buffer

    

    def Draw_pixel(self, Win_buffer):

        """
        Methode de dessin des pixels :
        """

        for i in range(self.height):
            for j in range(self.width):
                if Win_buffer[j][i] == 1:
                    ga.draw.rect(self.Window, self.White, [i*self.scale,j*self.scale, self.scale, self.scale], 0)
                else:
                    ga.draw.rect(self.Window, self.Black, [i*self.scale,j*self.scale, self.scale, self.scale], 0)
        ga.display.update()
        