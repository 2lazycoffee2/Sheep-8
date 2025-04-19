#coding:utf-8

class CPU: 
    """
    Classe définissant le coeur de la console : 
    """

    def __init__(self, rom_file, font_file):

        self.rom = rom_file
        self.font = font_file

        self.PC = 0x200
        self.memory = [0]*4096
        self.VX = [0]*16
        self.stack = [0]*16
        self.Index = 0

    def load_font(self):

        with open(self.font, "rb") as font:
            font_data = font.read()
        font.close()

        for cells in range(len(font_data)) : 
            self.memory[cells] = font_data[cells]

    
    def load_rom(self) : 
        with open(self.rom, "rb") as rom:
            rom_data = rom.read()

        for cells in range(len(rom_data)):
            self.memory[self.PC + cells] = rom_data[cells]

    def decode(self):

        Instruction = (self.memory[self.PC] << 8) | self.memory[self.PC + 1]

        # Ici, pour les demi octets (un caractère hexa) je le récupère avec un ET logique.>
        Nug1 = (Instruction & 0xF000) >> 12             # l'exemple ici soit 0xABCD. On fa>
        Nug2 = (Instruction & 0x0F00) >> 8
        Nug3 = (Instruction & 0x00F0) >> 4
        Nug4 = (Instruction & 0x000F)
        print("Voici mes NUGBELLS : 1-{}, 2-{}, 3-{}, 4-{}".format(Nug1, Nug2, Nug3, Nug4))

        # Un exemple pour bien comprendre : supposons que j'attrape l'instruction 0xABCD (>

        X = Nug2   #A
        Y = Nug3   #B   
        N = Nug4   #C
        NN = Nug3 << 4 | Nug4 #CD
        NNN = (Nug2 << 4 | Nug3) << 4 | Nug4 # BCD

        print("Position : ({}, {})\nDécoupage : 1-{}, 2-{}, 3-{}".format(X,Y , N, NN, NNN))
        # Pour plus de détail, lire la doc mais, ce découpage est nécessaire au bon fonctionnement de la console.

        def pipeline(self):
            print("encours de développement...")


coreprocess = CPU("rom/IBM.ch8", "font/chip48font.txt")

coreprocess.load_font()
coreprocess.load_rom()