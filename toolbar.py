import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import PhotoImage

class Toolbar:
    def __init__(self, parent, get_translations, actions, is_running=None, theme_bg=None, font_path=None, layout='left'):
        """
        Constructeur de la classe Toolbar.

        parent: widget parent (ici forcément la fenêtre principale)
        get_translations: fonction qui retourne le dict de traduction courant
        actions: dict { 'open_rom': callback, 'preferences': callback, 'help': callback }
        is_running: flag qui indique l'état de l'émulation (optionnel, par défaut False)
        theme_bg: couleur de fond (optionnel)
        font_path: chemin vers la police custom (optionnel)
        layout: 'left' (icônes à gauche) ou 'top' (icônes au-dessus)
        """
        self.parent = parent
        self.get_translations = get_translations
        self.actions = actions
        self.is_running = is_running or (lambda: False)
        self.theme_bg = theme_bg or parent.cget('bg')
        self.layout = layout
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
        self.toolbar = tb.Frame(self.parent, bootstyle="secondary")
        self.toolbar_images = {}
        buttons = [
            ('open_rom', 'openfile.png', self.actions.get('open_rom')),
        ]
        #Affichage conditionnel des boutons play/stop
        if not self.is_running():
            buttons.append(('start', 'play.png', self.actions.get('start')))
        else:
            buttons.append(('stop', 'stop.png', self.actions.get('stop')))
        buttons.append(('fullscreen', 'fullscreen.png', self.actions.get('fullscreen')))
        buttons += [
            ('preferences', 'settings.png', self.actions.get('preferences')),
            ('help', 'help.png', self.actions.get('help'))
        ]
        #Mapping des styles pour chaque action
        style_map = {
            'open_rom': 'info',
            'start': 'success',
            'stop': 'danger',
            'fullscreen': 'secondary',
            'preferences': 'secondary',
            'help': 'secondary',
        }
        # Détermination de la taille et de la disposition
        size = (48, 48) if self.layout == 'top' else (32, 32)
        compound = tb.TOP if self.layout == 'top' else tb.LEFT
        pack_side = tb.LEFT #if self.layout == 'left' else tb.TOP
        for idx, (label_key, icon_file, command) in enumerate(buttons): #On fait une boucle for pour éviter d'avoir un code long et répétitif
            icon_path = os.path.join('assets', 'uielements', 'themelight', icon_file)
            img = None
            try:
                pil_img = Image.open(icon_path).convert('RGBA')
                pil_img = pil_img.resize(size, Image.LANCZOS)
                img = ImageTk.PhotoImage(pil_img)
            except Exception:
                img = None #On doit penser à un cas où l'image n'existe pas, si l'utilisateur implémente un thème personnalisé et veut le tester sans l'avoir fini
            self.toolbar_images[icon_file] = img
            label_text = t.get(label_key, label_key)
            bootstyle = style_map.get(label_key, 'secondary')
            # Création du bouton
            btn = tb.Button(
                self.toolbar,
                text=label_text,
                command=command,
                bootstyle=bootstyle,
                width=12,
                image=img,
                compound=compound if img else None
            )
            btn.pack(side=pack_side, padx=2, pady=2)

    def update(self, layout=None):
        if layout is not None:
            self.layout = layout
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
