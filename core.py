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
    #print("here is your rom :\n{}".format(data_rom))
    #print ("length rom :\n {}".format(len(data_rom)))


#affichage et sauvegarde de la rom : 
for i in range(len(data_rom)):
    memory[PC + i] = data_rom[i]
    #print(memory[PC + i])            






shiftleftbyte = (memory[PC] << 8) | memory[PC + 1]      # Comme les instructions sont encodés sur 2 octets, et qu'un octet est 2 caractères hexadécimaux, on décale le premier octet(deux premiers caractère hexa) que l'on décale vers la gauche d'un octet et, que l'on racolle à l'octet suivant (soit le pc + 1 ième) 



print("catched instruct in decimal : {}\ncatched instruc in hexa : {} \n".format(shiftleftbyte, hex(shiftleftbyte)))

print("\n ALL DATA IN DECIMAL :\n {}". format(memory))


#while (true)
#if opcode == 00E0
    


"""
ici se trouvera une boucle infini pour le fetch, decode, execute, la lecture a été faite précédement.
Etape suivante : décoder l'hexa reçue avec l'histoire des nibbles (demi-octets)

"""

file.close()
