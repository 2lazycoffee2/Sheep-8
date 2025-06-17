import tkinter as tk
from tkinter import ttk
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
        self.toolbar = None
        self.toolbar_images = {}
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
        self.toolbar = ttk.Frame(self.parent)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.toolbar_images = {}
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
            # Frame vertical pour chaque bouton (icône + label)
            btn_frame = ttk.Frame(self.toolbar)
            btn_frame.grid(row=0, column=idx, padx=12, pady=2, sticky='n')
            # Bouton icône
            btn = ttk.Button(btn_frame, image=img, command=command, style='Toolbutton')
            btn.pack(side=tk.TOP, pady=(0,2))
            # Label texte (police système)
            label_text = t.get(label_key, label_key)
            lbl = ttk.Label(btn_frame, text=label_text, font=(None, 10, 'bold'))
            lbl.pack(side=tk.TOP)

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
