
#coding:utf-8
"""
Ceci est la version POC de notre émulateur. Très basique, elle n'inclue que les opcodes nécessaire au décodage, 
à l'affichage, les allocations de mémoire. C'est sur cette base que nous partirons pour pousser l'émulation à 
son paroxysme :) .
"""


import pygame as ga


"""
----DISPLAY :
"""
ga.init()
window = ga.display.set_mode((640, 320)) #640x320 en pratique pour voir les pixels en plus gros.
window.fill((0,0,0))

Win_Buffer = [[0 for _ in range(64)] for _ in range(32)]

"""
----CPU
"""

memory = [0]*4096           # Mémoire : 4ko
VX = [0]*16                 # Registre
VX [0xF]= 0                 # le fameux Carry flag, je n'ai pas saisie comment le réutiliser dans mon code...


stack = [0]*16                # Pile


PC = 0x200                  #Program counter, pour passer d'instruction en instruction.

Delay_timmer = 0        # Pour le son et les délaies (vitesses d'émulation), je ne sais pas encore comment les utiliser 
Delay_sound = 0

# un pointeur pour les sprintes e mémoire (0x000 -> 0x200)

Index = 0


 
"""chargement du fond en mémoire : dans le main cpu.py"""

with open("chip48font.txt", "rb") as fontfile :
    font_data = fontfile.read()  
fontfile.close()

for j in range(len(font_data)):
    memory[j] = font_data[j]         #On charge la police depuis un fichier 
#    memory[j] = static_font[j]      # on charge depuis le tableau static_font, c'était pour des tests

"""Chargement de la data en mémoire : dans le main cpu.py"""
with open("ibm.ch8", "rb") as file:
    data_rom = file.read()

for i in range(len(data_rom)):
    memory[PC + i] = data_rom[i]
             

#print("-------------------------------------------LA MEMOIRE------------------------------------------------------\n {} \n--------------------------------------------FIN DE MEMOIRE------------------------------------------\n".format(memory))


""""nubble def and FETCH/DECODE/EXECUTE:"""     #définition de chaque demi octet et, de leurs gignotage. Permettra d'associer par exemple le X au registre VX
running = True
clock = ga.time.Clock()

while running:
    for _ in range(1):
        for _ in range(len(memory)):
            try:
                shiftleftbyte = (memory[PC] << 8) | memory[PC + 1]      # Comme les instructions sont encodés sur 2 octets, et qu'un octet est 2 caractères hexadécimaux, on décale le premier octet (deux premiers caractère hexa) que l'on décale vers la gauche d'un octet et, que l'on racolle à l'octet suivant (soit le pc + 1 ième) 
            except IndexError:
                print (f"erreur : pc = {PC} dépasse la mémoire.")
                running = False
                break

            # Ici, pour les demi octets (un caractère hexa) je le récupère avec un ET logique. C'est un masquage puis un décalage vers la droite. Explication
            Nug1 = (shiftleftbyte & 0xF000) >> 12       # l'exemple ici soit 0xABCD. On fait l'opération suivante : 0b 1010 1011 1100 1101 que l'on "mutliplie" par 0b 1111 0000 0000 0000, on récupère 0xA000 puis on décale de 12 bits vers la droite.
            Nug2 = (shiftleftbyte & 0x0F00) >> 8
            Nug3 = (shiftleftbyte & 0x00F0) >> 4
            Nug4 = (shiftleftbyte & 0x000F)


            # Un exemple pour bien comprendre : supposons que j'attrape l'instruction 0xABCD (Qui n'existe pas bien sure). Alors on a :

            X = Nug2   #A
            Y = Nug3   #B   
            N = Nug4   #C
            NN = Nug3 << 4 | Nug4 #CD
            NNN = (Nug2 << 4 | Nug3) << 4 | Nug4 # BCD



            """Traitement de ce qui a été capturé :"""

            if shiftleftbyte == 0x00e0:           
                Win_Buffer = [[0 for _ in range(64)] for _ in range(32)]         #coditionnement, pour réaliser toutes les instructions, nous procéderons ainsi, on regade le type d'instruction que c'est ensuite, ces nugbells (N1, N2...) et, on les implémentes selon la doc du CHIP-8.
                #print ("pixel de l'écran mis à 0")
                PC +=2
            elif shiftleftbyte == 0x00ee:
                #initier l'écran comme une matrice 64*32px contenant des 0
                PC = stack.pop()
                #print("depop la pile, retour à l'adresse contenue dans la stack")
                PC +=2
            elif Nug1 == 0x1:
                PC = NNN
                #print("Mise de PC à  |{}| | PROG COUNTER : {}".format(NNN, PC))


            elif Nug1 == 0x2:
                #appelle du sous programme. 
                stack.append(PC)                         # le append c'est comme un push en assembleur. (cf archi ordi)
                #print("PC poussé dans la pile, Appelle du sous programme à l'adresse : |{}| | STACK : {}".format(NNN, stack))
                PC +=2

            elif Nug1 == 0x6:
                VX[X] = NN
                #print("Mise de VX à |{}| | REGISTRE : ".format(NN, VX))
                PC +=2

            elif Nug1 == 0x7:
                VX[X] += NN
                #print("Somme de |{}| et VX | REGISTRE : {}".format(NN, VX))
                PC +=2

            elif Nug1 == 0xa:
                Index = NNN
                #print("Fixe l'index I (ou Pointeur, à voir) à l'adresse |{}| | INDEX : {}".format(NNN, Index))
                PC +=2

            elif Nug1 == 0xd:
                VX[0xF]=0


                for line in range(N):
                    Sprite_Byte = memory[Index + line] # on stocke le spryte courant dans une variable et on réitère N fois pour lire N sprytes. 
                    #print("/!\ -------------------------NORMALEMENT LE SPYTE EST CHARGE : \n{}\n ".format(hex(Sprite_Byte)))
                    for colone in range(8):                                 # on lit un octet
                        px = (Sprite_Byte >> (7 - colone)) & 1              #sur cet octer un récupère un bit.
                        X_pos = (VX[X] + colone) % 64                       # On prend les positions qu'on incrémente.
                        Y_pos = (VX[Y] + line) % 32                         
                        
                        if px == 1 :                                        # ce pixel est un 1 ? si oui, le mapper sur le buffer.
                            if Win_Buffer[Y_pos][X_pos] == 1:
                                VX[0xF] = 1                                 # Flag de collision activé

                            Win_Buffer[Y_pos][X_pos] ^= 1                   # Xoré pour rebouclé, si le pixel sors de l'image, il revient de l'autre coté.
                        if Win_Buffer[Y_pos][X_pos] == 1:
                            ga.draw.rect(window, (255, 255, 255), [X_pos*10, Y_pos*10, 10, 10], 0)
                        

                        else :
                            ga.draw.rect(window, (0, 0, 0), [X_pos*10, Y_pos*10, 10, 10], 0)
                        ga.display.update()            
                print("REGISTRE : ({}, {})".format(X_pos, Y_pos))

    
                PC +=2
        clock.tick(60)  # Limite à 60 FPS
    print("Win_Buffer :\n", Win_Buffer)
    #print("L'entièreté de la mémoire : \n{}".format(memory))



file.close()