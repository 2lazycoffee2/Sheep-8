# Sheep-8


## Introduction :
Dans le cadre de nos études,mon collègue ainsi que moi même sommes ammenés à construire tout un projet de programmation en python.  
N

Le projet vient d'une passion et d'une nostalgie profonde pour les jeux rétros. Le projet est assez ambitieux mais les défis ne nous font pas peur.  
Nous proposons un émulateur que nous avons baptisé "Sheep 8", reproduisant le comportement du Chip-8 qui fut développé initialement dans le cadre du développement de jeux sur l'ordinateur COSMAC VIP en 1977. Nous proposons dans ce projet la reproduction du comportement du processeur RCA 1802. 

## GESTION DE PROJET : 

Le diagramme de Gantt ainsi que la modélisation réalisée sur Draw.io ont été créés sur un Drive partagé [dont voici le lien](https://drive.google.com/drive/folders/18R1xUCSLy8t2HY-SDTSvAYXqgMBrNfWm?usp=drive_link), accompagnés d'un [taiga.io](https://tree.taiga.io/project/tortipoof-projet-prog-2as2/kanban). Ces documents nous ont permis d'assurer un bon suivi du projet.

## DÉPENDANCES :

Assurez-vous d'installer python3 ainsi que les libraires suivantes via pip3 :  
- pygame
- ttkbootstrap
- pypresence
- pillow

### Notes : 
L'émulateur ne tourne que sur des architectures x64-86. 
Il n'est donc pas encore possible de le faire fonctionner sur des architectures différentes de celles-ci. 


## Utilisateurs Windows : 

Configuration minimale requise : Windows 8.1 ou supérieur

### Installation classique
Pour une installation classique sur votre machine, procédez aisni :
- Récupérez l'installer d'une des releases stables windows depuis la [section release](https://github.com/2lazycoffee2/Python_Project/releases/)  
- Exécutez l'installer.
- Suivre les étapes d'installation de l'installer.

### Installation portable :
Pour une installation portable sur un disque de stockage externe ou dans un dossier indépendant, téléchargez simplement le .zip du code source puis excéutez le .exe qu'il contient.
Veillez à ne pas l'isoler des sous-dossiers dont il dépend (assets, font, lang,...)


## Utilisateurs Linux :

Pour les utilisateurs Linux, récupérez 
- Récupérez le fichier Sheep8, celui sans extension.
- Accordez les droits d'exécutions au fichier Sheep8 en utilisant la commande : `chmod +x Sheep8`
- Exécutez le fichier avec la commande : `./Sheep8` 

Ainsi, vous pourrez pleinement profiter de l'émulateur sous Linux.

## JEUX : 

Assurez vous que les jeux que vous créez ou récupérez soient compatibles avec le CHIP 8 classique et, de préférence, ajoutez-y l'extension `.ch8` si ce n'est pas déjà fait. Les ROMs sans extensions seront lues, mais ne pourront apparaître dans la liste de l'interface. Ce comportement est voulu et vise à éviter l'apparition sur l'interface de fichiers sans extensions qui ne sont possiblement pas des ROMs CHIP-8. Si vous avez un doute sur la compatibilité de vos roms, nous vous renvoyons sur les documentations citées dans les remerciements pour s'assurer que vos roms fonctionnent bien avec notre émulateur. 

Pour une meilleure homogénéité dans vos fichiers, mettez les fichiers dans le dossier ROM

## REMERCIEMENTS : 

Nous remercions les différents rédacteurs de documentation Chip-8 qui nous ont beaucoup aidé à la création du projet. Voici les ressources utilisées : 

- https://tobiasvl.github.io/blog/write-a-chip-8-emulator/
- http://devernay.free.fr/hacks/chip8/C8TECH10.HTM
- https://en.wikipedia.org/wiki/CHIP-8

Nous tenons aussi à remercier les "tests suites" qui nous ont beaucoup aidé : 
- https://github.com/corax89/chip8-test-rom
- https://github.com/Timendus/chip8-test-suite
