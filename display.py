#coding:utf-8

import pygame as ga

class Display:

    """
    Classe permettant de gérer l'affichage de l'écran 64x32 du CHIP-8
    """

    def __init__(): 
        """
        Constructeur de la classe Display
        """
        # Initialisation de Pygame
        ga.init()

        # Création de la fenêtre
        self.window = ga.display.set_mode((640, 320))

        # Remplissage de la fenêtre avec du noir (les pixels étant noirs par défaut)
        Window.fill((0, 0, 0))

        # Création d'un tableau de 32x64 pour le buffer d'affichage
        Win_Buffer = [[0 for _ in range(64)] for _ in range(32)]