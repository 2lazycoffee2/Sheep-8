#coding:utf-8
import pygame as ga
class Input : 
    """
    Classe qui sert d'entrées utilisateurs.
    """
    def __init__(self) :
        
        
        self.keypad = [0]*16            # Le pad du COSMAC VIP Utilise 16 touches. On le modélise par une matrice 1x16.
        self.key_map ={ 
        #  Chaque touches du clavier correspond à une valeur hexadécimal envoyé au cpu.  
           ga.K_1 :   0x0,
           ga.K_2 :   0x1, 
           ga.K_3 :   0x2, 
           ga.K_4 :   0x3,

           ga.K_a :   0x4, 
           ga.K_z :   0x5,
           ga.K_e :   0x6, 
           ga.K_r :   0x7, 
           
           ga.K_q :   0x8, 
           ga.K_s :   0x9, 
           ga.K_d :   0xa, 
           ga.K_f :   0xb, 
           
           ga.K_w :   0xc, 
           ga.K_x :   0xd, 
           ga.K_c :   0xe,
           ga.K_v :   0xf 
        }

   
   
    def update(self, events):
        """
        Mise à jour des touches
        sont-elles pressées ou non.
        """
        for event in events:                                            # Si une touche est pressée, on met le coefficient  de la matrice keypad correspondant à la touche pressée 1. 
            if event.type == ga.KEYDOWN:
                if event.key in self.key_map:
                    self.keypad[self.key_map[event.key]] = 1
            if event.type == ga.KEYUP:
                    if event.key in self.key_map:                       # Sinon, on laisse à 0.
                        self.keypad[self.key_map[event.key]] = 0
                    












    
        