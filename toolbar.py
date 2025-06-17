import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

class Toolbar:
    def __init__(self, parent, get_translations, actions, theme_bg=None, font_path=None):
        """
        Constructeur de la classe Toolbar.

        parent: widget parent (ici forcément la fenêtre principale)
        get_translations: fonction qui retourne le dict de traduction courant
        actions: dict { 'open_rom': callback, 'preferences': callback, 'help': callback }
        theme_bg: couleur de fond (optionnel)
        font_path: chemin vers la police custom (optionnel)
        """
        self.parent = parent
        self.get_translations = get_translations
        self.actions = actions
        self.theme_bg = theme_bg or parent.cget('bg')
        self.font_path = font_path or os.path.join('assets', 'fonts', 'Address Sans Pro SemiBold.ttf')
        self.toolbar = None
        self.toolbar_images = {}
        self.toolbar_label_images = {}
        self._build_toolbar()

    def destroy(self):
        """
        Destruction de la toolbar
        """
        if self.toolbar is not None:
            self.toolbar.destroy()
            self.toolbar = None

    def _build_toolbar(self):
        """
        Construction de la toolbar
        """
        t = self.get_translations()
        if self.toolbar is not None:
            self.toolbar.destroy() #On détruit la toolbar existante avant de la reconstruire
        self.toolbar = tk.Frame(self.parent, bd=1, bg=self.theme_bg)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.toolbar_images = {}
        self.toolbar_label_images = {}
        buttons = [
            ('open_rom', 'openfile.png', self.actions.get('open_rom')),
            ('preferences', 'settings.png', self.actions.get('preferences')),
            ('help', 'help.png', self.actions.get('help'))
        ]
        for idx, (label_key, icon_file, command) in enumerate(buttons): #On fait une boucle for pour éviter d'avoir un code long et répétitif
            icon_path = os.path.join('assets', 'uielements', 'themelight', icon_file)
            img = None
            try:
                pil_img = Image.open(icon_path).convert('RGBA')
                pil_img = pil_img.resize((32, 32), Image.LANCZOS)
                img = ImageTk.PhotoImage(pil_img) 
            except Exception:
                img = None #On doit penser à un cas où l'image n'existe pas, si l'utilisateur implémente un thème personnalisé et veut le tester sans l'avoir fini
            self.toolbar_images[icon_file] = img
            label_text = t.get(label_key, label_key)
            try:
                font_size = 14
                font = ImageFont.truetype(self.font_path, font_size) #Utilisation police custom
                dummy_img = Image.new('RGBA', (1, 1)) # Création d'une image vide pour calculer la taille du texte
                draw = ImageDraw.Draw(dummy_img) 
                text_w, text_h = draw.textbbox((0,0), label_text, font=font)[2:]
                label_img = Image.new('RGBA', (max(32, text_w)+8, text_h+8), (255, 255, 255, 0))
                draw = ImageDraw.Draw(label_img) #On utilise ImageDraw pour dessiner le texte sous forme d'image (pour gérer les polices custom)
                x = (label_img.width - text_w) // 2
                y = (label_img.height - text_h) // 2
                draw.text((x, y), label_text, font=font, fill=(30, 30, 30, 255))
                tk_label_img = ImageTk.PhotoImage(label_img)
                self.toolbar_label_images[label_key] = tk_label_img
            except Exception:
                tk_label_img = None
            btn_frame = tk.Frame(self.toolbar, bg=self.theme_bg, bd=0, highlightthickness=0)
            btn_frame.grid(row=0, column=idx, padx=8, pady=2, rowspan=2, sticky='n')
            def on_enter(e, fr=btn_frame):
                fr.config(bg='#e0e0e0')
            def on_leave(e, fr=btn_frame):
                fr.config(bg=self.theme_bg)
            btn_frame.bind('<Button-1>', lambda e, cmd=command: cmd() if cmd else None)
            btn_frame.bind('<Enter>', on_enter)
            btn_frame.bind('<Leave>', on_leave)
            icon_lbl = tk.Label(btn_frame, image=img, bg=btn_frame.cget('bg'), bd=0)
            icon_lbl.pack(side=tk.TOP, pady=(0,0))
            icon_lbl.bind('<Button-1>', lambda e, cmd=command: cmd() if cmd else None)
            icon_lbl.bind('<Enter>', on_enter)
            icon_lbl.bind('<Leave>', on_leave)
            if tk_label_img:
                text_lbl = tk.Label(btn_frame, image=tk_label_img, bg=btn_frame.cget('bg'), bd=0)
            else:
                text_lbl = tk.Label(btn_frame, text=label_text, font=(None, 11, 'bold'), bg=btn_frame.cget('bg'))
            text_lbl.pack(side=tk.TOP, pady=(0,2))
            text_lbl.bind('<Button-1>', lambda e, cmd=command: cmd() if cmd else None)
            text_lbl.bind('<Enter>', on_enter)
            text_lbl.bind('<Leave>', on_leave)

    def update(self):
        self._build_toolbar()

    def pack(self, **kwargs):
        if self.toolbar is not None:
            self.toolbar.pack(**kwargs)

    def grid(self, **kwargs):
        if self.toolbar is not None:
            self.toolbar.grid(**kwargs)

    def place(self, **kwargs):
        if self.toolbar is not None:
            self.toolbar.place(**kwargs)
