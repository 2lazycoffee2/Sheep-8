    #coding:utf-8
import random as rand

class CPU: 
        """
        Classe définissant le coeur de la console : 
        """

        def __init__(self, rom_file, keypad):
            
            """
            Constructeur de la classe CPU
            """
            self.rom = rom_file

            self.PC = 0x200
            self.memory = [0]*4096
            self.VX = [0]*16
            self.stack = [0]*16
            self.Index = 0

            self.keypad = keypad
            # serviront à l'écran, le cpu en dépendera pour l'instant je n'ai pas trouver meilleure alternative
            self.Win_buffer = [[0 for _ in range(64)] for _ in range(32)]

            self.delay_timer = 0 # équivalent au 60HZ, valeur qui sera donné au cpu
            self.delay_sound = 0

        def load_font(self):
            """
            Fonction de chargement de la 
            police de caractère en mémoire.
            """
          
            font_data =[0xF0, 0x90, 0x90, 0x90, 0xF0, #// 0
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
                        0xF0, 0x80, 0xF0, 0x80, 0x80]  #// F}
            
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
            Nug1 = (Instruction & 0xF000) >> 12             # l'exemple ici soit 0xABCD. On fait un découpage où l'on récupère chaque caractère hexadécimal.
            Nug2 = (Instruction & 0x0F00) >> 8
            Nug3 = (Instruction & 0x00F0) >> 4
            Nug4 = (Instruction & 0x000F)
            # Un exemple pour bien comprendre : supposons que l'on attrape l'instruction 0xABCD : 

            X = Nug2   #A
            Y = Nug3   #B   
            N = Nug4   #C
            NN = Instruction & 0x00FF#(Nug3 << 4 | Nug4) #CD
            NNN = Instruction & 0x0FFF#(Nug2 << 4 | Nug3) << 4 | Nug4 # BCD

            # Pour plus de détail, lire la doc mais, ce découpage est nécessaire au bon fonctionnement de la console.
        
            return Instruction, Nug1, Nug2, Nug3, Nug4, X, Y, N, NN, NNN
        

        def Mapping(self, X, Y, N):
            
            """
            fonction qui servira à mapper
            le buffer et le renverra à 
            la class display qui s'occupe du reste.
            """
            self.VX[0xF] = 0

            for line in range(N):
                Sprite_Byte = self.memory[self.Index + line]
                for colone in range(8):

                    px = (Sprite_Byte >> (7 - colone)) & 1
                    x_pos = (self.VX[X] + colone) % 64
                    y_pos = (self.VX[Y] + line) % 32
            
                    if px ==1 :
                        if self.Win_buffer[y_pos][x_pos] == 1 : 
                            self.VX[0xF] = 1
                        self.Win_buffer[y_pos][x_pos] ^=1                   # On Xor les coordonnées afin d'éviter les dépassements dans le buffer.  
                
            return self.Win_buffer
        
        def Reset_Window_Buffer(self):
            """
            Raffraichit le buffer d'écran
            en remettant tout les coefficients 
            de la matrice à zéro.
            """
            self.Win_buffer = [[0 for _ in range(64)] for _ in range(32)]
            return self.Win_buffer

        def pipeline(self):
            """
            fonction fetch/decode/execute, 
            elle émule le pipeline de la 
            console.
            """
            
            Instruction, Nug1, Nug2, Nug3, Nug4, X, Y, N, NN, NNN = self.decode()
            
            if Instruction == 0x00e0 :
                self.Reset_Window_Buffer()
                self.PC += 2

            elif Instruction == 0x00ee:
                #depop la pile, retour à l'adresse contenue dans la stack 
                self.PC = self.stack.pop()
            

            elif Nug1 == 0x1:
                # mise de PC à NNN
                self.PC = NNN

            elif Nug1 == 0x2:
                #appelle du sous programme. Push la prochaine instruction  
                self.stack.append(self.PC + 2)                         
                self.PC = NNN

            elif Nug1 == 0x3: 
                # saut conditionnel
                if self.VX[X] == NN:
                    self.PC += 4
                else:
                    self.PC+=2             


            elif Nug1 == 0x4: 
                # saut conditionnel
                if self.VX[X] != NN:
                    self.PC += 4
                else: 
                    self.PC+=2



            elif Nug1 == 0x5 and Nug4 == 0x0:
                # saut conditionnel
                if self.VX[X] == self.VX[Y]:
                    self.PC+=4
                else:
                    self.PC +=2


            elif Nug1 == 0x6:
                # mise de VX à NN
                self.VX[X] = NN
                self.PC +=2

            elif Nug1 == 0x7:
                #addition sans dépassement
                self.VX[X] = (self.VX[X] + NN) % 256        #
                self.PC +=2
                



    #-------------------------------8XY_----------------------------------
            elif Nug1 == 0x8:

                if Nug4 == 0x0: #set 
                    self.VX[X] = self.VX[Y]

                elif Nug4 == 0x1: # or
                    self.VX[X] = (self.VX[X] | self.VX[Y])

                elif Nug4 == 0x2: # and
                    self.VX[X] = (self.VX[X] & self.VX[Y])     

                elif Nug4 == 0x3: #xor
                    self.VX[X] ^= self.VX[Y]                

                elif Nug4 == 0x4:  #sum       
                    
                    tmp_sum = self.VX[X] + self.VX[Y]

                    self.VX[X] = tmp_sum % 256
                    if tmp_sum > 255:
                        self.VX[0xF] = 1
                    else :
                        self.VX[0xF] = 0

                    #self.PC +=2

                elif Nug4 == 0x5:   #sub     
                    tempvx = self.VX[X] 
                    tempvy = self.VX[Y] 

                    self.VX[X] = (tempvx - tempvy) % 256    #pour rester sur 8bits sinon on fait un "overflow"

                    if tempvx >= tempvy : 
                        self.VX[0xF] = 1 
                    else :
                        self.VX[0xF] = 0
                    #self.PC +=2

                elif Nug4 == 0x6:   # shift right 
                    tempvx = self.VX[X]  
                    self.VX[X] = (tempvx >> 1) & 0xFF                    # et là on a le choix entre set vx à vy et shifté ou juste shifté vx. Selon la doc, la méthode moderne est de ne traité que vx (1990)

                    self.VX[0xF] = tempvx & 1             #ici on récupère le bit que l'on va perdre après être shifté vers la droite avec un bitwise and
                    

                elif Nug4 == 0x7:    #sub  
                    self.VX[X]  = (self.VX[Y] - self.VX[X]) % 256

                    if self.VX[Y] >= self.VX[X]:
                        self.VX[0xF] = 1
                    else : 
                        self.VX[0xF] = 0
                                        

                elif Nug4 == 0xe:    # shift left   
                    tempvx = self.VX[X]
                    self.VX[X] = (tempvx << 1 ) & 0xFF          

                    self.VX[0xF] = (tempvx & 0x80) >> 7         #on récupère le dernier bit que l'on va perdre après le shift que l'on décale vers la droite pour que ce soit un vrai bit

                    
                self.PC +=2
    #--------------------------------------------------------------------

            elif Nug1 == 0x9 and Nug4 == 0x0:
                if self.VX[X] != self.VX[Y] : 
                    self.PC +=4
                else:
                    self.PC+=2

            elif Nug1 == 0xa:
                self.Index = NNN
                self.PC +=2

            elif Nug1 == 0xb:                       
                self.PC = NNN + self.VX[0]


            elif Nug1 == 0xc:       
                self.VX[X] = rand.randint(0, 255) & NN
                self.PC += 2
                       

            elif Nug1 == 0xd:
                """
                instruction de dessin.
                met N bits à un ou à 
                zéro dans le buffer d'écran
                à la position (X, Y)
                """
                self.Mapping(X, Y, N)
                self.PC += 2




    #-------------//KEY IS PRESSED OR NOT------------------#
            elif Nug1 == 0xe and Nug3 == 0x9: 
                if  self.keypad[self.VX[X]] == 1:
                    self.PC+=4
                else :
                    self.PC+=2
              

            elif Nug1 == 0xe and Nug3 == 0xa and Nug4 == 0x1: 
                
                if self.keypad[self.VX[X]] == 0:
                    self.PC+=4
                else :
                    self.PC+=2
    #-------------------------------------------------------

            elif Nug1 == 0xf: 
                if Nug3 == 0x1 and Nug4 == 0xe:     #FX1E
                    self.Index = (self.VX[X] + self.Index) &  0x0FFF 
                    self.PC+=2

                elif Nug3 == 0x2 and Nug4 == 0x9:   #FX29 
                    self.Index = self.VX[X] * 5
                    self.PC +=2
                
                elif Nug3 == 0x3 and Nug4 == 0x3:

                    
                    """
                    ici, on utilisera la division entière, très pratique pour 
                    récupérer les valeurs dizaines et centaines, exemple :
                    123 // 100 = 1
                    """                    
                    decX = int(self.VX[X])

                    self.memory[self.Index]     = self.VX[X] // 100                    
                    self.memory[self.Index + 1] = (self.VX[X] // 10 )%10                     
                    self.memory[self.Index + 2] = self.VX[X]% 10                    
                    self.PC += 2
    #------------TIMERS :-------------------------------#

                elif Nug3 == 0x0 and Nug4 == 0x7:
                    self.VX[X] = self.delay_timer
                    self.PC+=2
                elif Nug3 == 0x1 and Nug4 == 0x5:
                    self.delay_timer = self.VX[X]
                    self.PC+=2
                elif Nug3 == 0x1 and Nug4 == 0x8:
                    self.delay_sound = self.VX[X]
                    self.PC+=2

    #-------------- DATA STORAGE------------------------#

                elif Nug3 == 0x5 and Nug4 == 5:
                   
                    for i in range(X + 1):
                        self.memory[self.Index + i] = self.VX[i ] 
                    self.PC+=2
                elif Nug3 == 0x6 and Nug4 == 0x5:             
                    
                    for i in range(X + 1):
                        self.VX[i] = self.memory[self.Index + i]                    
                    self.PC+= 2 
                elif Nug4 == 0xa :
                    key_is_pressed = False
                    for i in range(16):
                        if self.keypad[i]:
                            self.VX[X] = i
                            key_is_pressed = True
                            break
                    if not key_is_pressed:
                        return
                    self.PC+=2
