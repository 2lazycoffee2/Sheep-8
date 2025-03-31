#coding:utf-8

#import pygame

memory = [0]*4096
VX= [0]*16
stack = [16]

# chargement de la rom, chargeé -> stocké dans une var, convertir, envoyé en mémoire boucle : 

with open("rom/IBM.ch8", "rb") as file:
    data_rom = file.readlines()
    print("voici votre rom :\n{}".format(data_rom))
file.close()


#with open("rom/IBM.ch8", "rb") as file0:
#    data0_rom = file.readlines().hex()
#    print("------------------------------------\nVoici maintenant la romm en hexa(test d'un deuxième affichage)\n{}".format([hex(i) for i in data0_rom]))
#file.close()
          
# pas besoin de transformation en hexa au final, les valeurs lu avvec l'argument rb permet de lire le binaire tel quel donc, récup les vals qui sont déjà en hexa :)
# Prochaine étape, sauvegarde de la data dans la mémoire memory.