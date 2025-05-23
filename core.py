#coding:utf-8

class CPU: 
    """
    Classe définissant le coeur de la console : 
    """

    def __init__(self, rom_file, font_file, keypad):
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
        
        self.Win_buffer =[[0 for _ in range(64)]  for _ in range(32)]

        self.keypad = keypad

        self.delay_timer = 0
        self.delay_sound = 0



    def load_font(self):
        """
        Fonction de chargement de la 
        police de caractère en mémoire.
        """
        #with open(self.font, "rb") as font:
        #    font_data = font.read()
        #font.close()
        font_data = [0xF0, 0x90, 0x90, 0x90, 0xF0,#// 0
                    0x20, 0x60, 0x20, 0x20, 0x70, #// 1
                    0xF0, 0x10, 0xF0, 0x80, 0xF0, #// 2
                    0xF0, 0x10, 0xF0, 0x10, 0xF0, #// 3
                    0x90, 0x90, 0xF0, 0x10, 0x10, #// 4
                    0xF0, 0x80, 0xF0, 0x10, 0xF0, #// 5
                    0xF0, 0x80, 0xF0, 0x90, 0xF0, #// 6
                    0xF0, 0x10, 0x20, 0x40, 0x40, #// 7
                    0xF0, 0x90, 0xF0, 0x90, 0xF0, #// 8
                    0xF0, 0x90, 0xF0, 0x10, 0xF0, #// 9
                    0xF0, 0x90, 0xF0, 0x90, 0x90, #// A
                    0xE0, 0x90, 0xE0, 0x90, 0xE0, #// B
                    0xF0, 0x80, 0x80, 0x80, 0xF0, #// C
                    0xE0, 0x90, 0x90, 0x90, 0xE0, #// D
                    0xF0, 0x80, 0xF0, 0x80, 0xF0, #// E
                    0xF0, 0x80, 0xF0, 0x80, 0x80] #// F


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

        # Ici, pour les demi octets (un caractère hexa) je le récupère avec un ET logique.
        Nug1 = (Instruction & 0xF000) >> 12             # l'exemple ici soit 0xABCD. On fait un décalage de 12 bits vers la droite pour récupérer le dernier caractère hexadécimal
        Nug2 = (Instruction & 0x0F00) >> 8
        Nug3 = (Instruction & 0x00F0) >> 4
        Nug4 = (Instruction & 0x000F)
        print("Voici mes NUGBELLS : 1-{}, 2-{}, 3-{}, 4-{}".format(Nug1, Nug2, Nug3, Nug4))

        # Un exemple pour bien comprendre : supposons que j'attrape l'instruction 0xABCD, on obtient le découpage suivant :

        X = Nug2   #A
        Y = Nug3   #B   
        N = Nug4   #C
        NN = Nug3 << 4 | Nug4 #CD
        NNN = (Nug2 << 4 | Nug3) << 4 | Nug4 # BCD

        return Instruction, Nug1, Nug2, Nug3, Nug4, X, Y, N, NN, NNN
    
    
    def Mapping(self, X, Y, N):
        """
        fonction qui servira à
        mapper le buffer et, le
        renvoie à la class display.
        """

        self.VX[0xF] = 0
        for line in range(N):
            Sprite_Byte = self.memory[self.Index + line]
            for colone in range(8) : 
                px = (Sprite_Byte >> (7 - colone) ) & 1
                x_pos = (self.VX[X] + colone) % 64
                y_pos = (self.VX[Y] + line) %32

                if px == 1:
                    if self.Win_buffer[y_pos][x_pos] == 1 :
                        self.VX[0xF] = 1
                    self.Win_buffer[y_pos][x_pos]^=1

        return self.Win_buffer
    

    def Reset_Window_Buffer(self):
        self.Win_buffer = [[0 for _ in range(64)] for _ in range 32]
        return self.Win_buffer

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
            #depop la pile, retour à l'adresse contenue dans la stack.
            self.PC = self.stack.pop()
            self.PC +=2

        elif Nug1 == 0x1:
            #saut inconditionnel, PC mis à l'adresse NNN
            self.PC = NNN

        elif Nug1 == 0x2:
            #appelle du sous programme. 
            self.stack.append(self.PC + 2)                         # le append c'est comme un push en assembleur. (cf archi ordi)
            self.PC +=2

        elif Nug1 == 0x3:
            #saut conditionnel
            if self.VX[X] == NN:
                self.PC+=4
            else :
                self.PC+=2


        elif Nug1 == 0x4:
            #saut conditionnel            
            if self.VX[X] != NNN:
                self.PC +=4
            else :
                self.PC +=2

        elif Nug1 == 0x5 and Nug4 == 0x0:
            if self.VX[X] == self.VX[Y] : 
                self.PC+=4
            else : 
                self.PC+=2


        elif Nug1 == 0x6:
            #stockage de l'adresse NN dans le registre VX.
            self.VX[X] = NN
            self.PC +=2

        elif Nug1 == 0x7:
            #addition sans dépassement. 
            self.VX[X] = (self.VX[X] +NN) %256
            self.PC +=2

#------------8xy_---------------
        elif Nug1 == 0x8;
            if Nug4 == 
            if Nug4 == 
            if Nug4 == 
            if Nug4 == 
            if Nug4 == 
            if Nug4 == 
            if Nug4 == 
            











             
                           


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