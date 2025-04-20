#coding:utf-8

class CPU: 
    """
    Classe définissant le coeur de la console : 
    """

    def __init__(self, rom_file, font_file, display, Win_buffer):
        """
        Constructeur de la classe CPU
        """
        self.rom = rom_file
        self.font = font_file

        self.PC = 0x200
        self.memory = [0]*4096
        self.VX = [0]*16
        self.stack = [0]*16
        self.Index = 0
        
        # serviront à l'écran, le cpu en dépendera pour l'instant je n'ai pas trouver meilleure alternative
        
        self.display = display
        self.Win_buffer = Win_buffer



    def load_font(self):
        """
        Fonction de chargement de la 
        police de caractère en mémoire.
        """
        with open(self.font, "rb") as font:
            font_data = font.read()
        font.close()

        for cells in range(len(font_data)) : 
            self.memory[cells] = font_data[cells]

    
    def load_rom(self) : 
        """
        Fonction de chargement de la rom
        en mémoire.
        """
        with open(self.rom, "rb") as rom:
            rom_data = rom.read()

        for cells in range(len(rom_data)):
            self.memory[self.PC + cells] = rom_data[cells]


    def decode(self):
        """
        Fonction décodeur, elle lit ce qui 
        est récupéré en mémoire et le décode.
        Un découpage des caractères hexadécimaux,
        expliqué dans les commentaires est réalisé.
        """
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
       
        return Instruction, Nug1, Nug2, Nug3, Nug4, X, Y, N, NN, NNN
    
    


    def pipeline(self):
        """
        fonction fetch/decode/execute, 
        elle émule le pipeline de la 
        console.
        """
        Instruction, Nug1, Nug2, Nug3, Nug4, X, Y, N, NN, NNN = self.decode()
        
        if Instruction == 0x00e0 : 
            self.PC += 2

        elif Instruction == 0x00ee:
            #initier l'écran comme une matrice 64*32px contenant des 0
            self.PC = self.stack.pop()
            #print("depop la pile, retour à l'adresse contenue dans la stack")
            self.PC +=2

        elif Nug1 == 0x1:
            self.PC = NNN
            #print("Mise de PC à  |{}| | PROG COUNTER : {}".format(NNN, PC))

        elif Nug1 == 0x2:
            #appelle du sous programme. 
            self.stack.append(self.PC)                         # le append c'est comme un push en assembleur. (cf archi ordi)
            self.PC +=2

        elif Nug1 == 0x6:
            self.VX[X] = NN
            #print("Mise de VX à |{}| | REGISTRE : ".format(NN, VX))
            self.PC +=2

        elif Nug1 == 0x7:
            self.VX[X] += NN
            #print("Somme de |{}| et VX | REGISTRE : {}".format(NN, VX))
            self.PC +=2

        elif Nug1 == 0xa:
            self.Index = NNN
            self.PC +=2

        elif Nug1 == 0xd:
            self.VX[0xF]=0
            for line in range(N):
                Spryte_Byte = self.memory[self.Index +line]

                for colone in range(8):
                    px = (Spryte_Byte >> (7 - colone)) & 1     
                    X_pos = (self.VX[self.X] + colone) % 64
                    Y_pos = (self.VY[self.Y] + line) % 32

                    if px == 1:    
                        self.Win_buffer[Y_pos][X_pos] ^=1
                    
                    if self.Win_buffer[Y_pos][X_pos] == 1:
                            self.VX[0xF] = 1
                            self.display(Y_pos, X_pos)
            self.PC += 2
                      
        print("pipeline en cours de développement...")

"""
coreprocess = CPU("rom/IBM.ch8", "font/chip48font.txt")

coreprocess.load_font()
coreprocess.load_rom()
"""