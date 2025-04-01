#coding:utf-8

#import pygame


memory = [0]*4096           # Mémoire : 4ko
VX= [0]*16                  # Registre

stack = [16]                # Pile
SP = []                     # Pointeur de pile

PC = 0x200                  #Program counter, pour passer d'instruction en instruction.



Delay_timmer = [0]*8 
Delay_sound = [0] * 8

Pointer = [0] * 16          # un pointeur pour les sprintes e mémoire (0x000 -> 0x200)




# chargement de la rom, chargeé -> stocké dans une var, convertir, envoyé en mémoire boucle : 



with open("rom/IBM.ch8", "rb") as file:
    data_rom = file.read()
    #print("voici votre rom :\n{}".format(data_rom))
    print ("ici la taille de la rom :\n {}".format(len(data_rom)))


#affichage et sauvegarde de la rom : 
for i in range(len(data_rom)):
    memory[PC + i] = data_rom[i]
    print(memory[PC + i])              #lecture de la rom faites en décimale, reconversion en hexa ??



#while (true)
"""
ici se trouvera une boucle infini pour le fetch, decode, execute, la lecture a été faite précédement.
Etape suivante : décoder l'hexa reçue avec l'histoire des nibbles (demi-octets)

"""

file.close()
