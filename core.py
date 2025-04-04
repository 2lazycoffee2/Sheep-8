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




""""nubble def and FETCH/DECODE/EXECUTE:"""     #définition de chaque demi octet et, de leurs gignotage. Permettra d'associer par exemple le X au registre VX

while PC < 0x200 + len(data_rom):
    shiftleftbyte = (memory[PC] << 8) | memory[PC + 1]      # Comme les instructions sont encodés sur 2 octets, et qu'un octet est 2 caractères hexadécimaux, on décale le premier octet(deux premiers caractère hexa) que l'on décale vers la gauche d'un octet et, que l'on racolle à l'octet suivant (soit le pc + 1 ième) 


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
    print("--------------------------OPCODE TRAITE :{}".format(hex(shiftleftbyte)))
    if shiftleftbyte == 0x00e0:                 #coditionnement, pour réaliser toutes les instructions, nous procéderons ainsi, on regade le type d'instruction que c'est ensuite, ces nugbells (N1, N2...) et, on les implémentes selon la doc du CHIP-8.
        print ("pixel de l'écran mis à 0")
    elif shiftleftbyte == 0x00ee:
        print("depop la pile, retour à l'adresse contenue dans la stack")
    elif Nug1 == 0x1:
        print("Mise de PC à  |{}| ".format(NNN))
    elif Nug1 == 0x2:
        print("PC poussé dans la pile, Appelle du sous programme à l'adresse : |{}|".format(NNN))
    elif Nug1 == 0x6:
        print("Mise de VX à |{}|".format(NN))
    elif Nug1 == 0x7:
        print("Somme de |{}| et VX ".format(NN))
    elif Nug1 == 0xa:
        print("Fixe l'index I (ou Pointeur, à voir) à l'adresse |{}| ".format(NNN))
    elif Nug1 == 0xd:
        print("Dessine |{}| pixels depuis l'emplacement Indexé par I (ou Pointeur)".format(N))
    else:
        print("\n/!\ INSTRUCTION NON TRAITEE, LE DEVELOPPEMENT EST EN COURS. MERCI DE VOTRE COMPREHENSION.")
    PC +=2


#print("concatenation : \n{}, {}, {}, {}, {}".format(X, Y, N, NN, NNN))
#print("HEXA concatenation : \n{}, {}, {}, {}, {}".format(hex(X), hex(Y), hex(N), hex(NN), hex(NNN)))




file.close()
