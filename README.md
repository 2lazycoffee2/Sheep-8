# Sheep-8


## Introduction :
Dans le cadre de nos études, Victor ainsi que moi même sommes ammenés à construire tout un projet de programmation en python.  
Nos prénoms : 
- TortipOOF -> Victor
- 2lazycoffee2 -> Hicham
Le projet viens d'une passion et d'une nostalgie profonde pour les jeux rétros. Le projet est assez ambitieux mais, les défis ne nous font pas peur.  
Nous proposons un émulateur que nous avons batisé "Sheep 8". C'est un émulateur reproduisant le comportement du Chip-8 qui fut développer initialement dans le cadre du développement de jeux sur l'ordinateur COSMAC VIP en 1977. Nous proposons Dans ce projet, la reproduction du comportement du processeur RCA 1802. 

## GESTION DE PROJET : 

Le diagramme de Gantt ainsi que la modélisation réalisée sur Draw.io ont été créés sur un Drive. Ces documents nous ont permis d'assurer un bon suivi du projet.
## DÉPENDENCES :

Assurez-vous d'installer python3 ainsi que les libraires suivantes via pip3 :  
- pygame
- ttkbootstrap
- pypresence
- pillow

### Notes : 
L'émulateur ne tourne que sur des architectures x64-86. 
Il n'est donc pas encore possible de le faire fonctionner sur des architectures différentes de celles-ci. 


## Utilisateurs Windows : 

Pour les utilisateurs Windows, procédez aisni :
- Récupérez l'installer d'une des release stable windows depuis la [section release](https://github.com/2lazycoffee2/Python_Project/releases/tag/v1.1.1)  
- Exécutez l'installer.
- Suivre les étapes d'installation de l'installer.

Une fois ces étapes placé, votre installer est prêt et, vous pouvez maintenant profiter de l'émulateur.


## Utilisateurs Linux :

Pour les utilisateurs Linux, récupérez 
- Récupérez le fichier Sheep8, celui sans extension.
- Accordez les droits d'exécutions au fichier Sheep8 en utilisant la commande : `chmod +x Sheep8`
- Exécutez le fichier avec la commande : `./Sheep8` 

Ainsi, vous pourrez pleinement profiter de l'émulateur sous Linux.

## JEUX : 

Assurez vous que les jeux que vous crée ou récupéré soient compatible avec le CHIP 8 classique et, par préférence, ajoutez-y la l'extensions `.ch8`. Si vous avez un doute sur la compatibilité
de vos roms, nous vous renvoyons sur les documentations citées dans les remerciements pour s'assurer que vos roms fonctionnent bien avec notre émulateur. 

Pour une meilleure homogénéité dans vos fichiers, mettez les fichiers dans le dossier ROM

## REMERCIEMENTS : 

Nous remercions à l'avance les différents rédacteurs de documentation Chip-8 qui nous ont beaucoup aidé à la création du projet. Voici les ressources utilisées : 

- https://tobiasvl.github.io/blog/write-a-chip-8-emulator/
- http://devernay.free.fr/hacks/chip8/C8TECH10.HTM
- https://en.wikipedia.org/wiki/CHIP-8

Nous tenons aussi à remercier les "tests suites" qui nous ont beaucoup aidé : 
- https://github.com/corax89/chip8-test-rom
- https://github.com/Timendus/chip8-test-suite
