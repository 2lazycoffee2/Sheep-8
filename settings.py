import tkinter as tk
from tkinter import ttk
import tkinter.colorchooser as cc
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import os
import json

class SettingsWindow(tb.Toplevel):
    """
    Fenêtre de paramètres
    """

    def __init__(self, parent, context):
        """
        Initialisation de la fenêtre de paramètres

        parent: widget parent (la fenêtre principale)
        context: dictionnaire de contexte contenant les paramètres et callbacks
        """

        super().__init__(parent)
        self.translations = context['translations'] #Dictionnaire de traductions
        self.language = context['language'] #Langue actuelle
        self.toolbar_enabled = context['toolbar_enabled'] #État de la toolbar
        self.framerate = context['framerate'] #Fréquence de rafraîchissement
        self.fullscreen_on_start = context.get('fullscreen_on_start', False)
        self.set_language_callback = context['set_language_callback'] #Callback pour changer la langue
        self.set_framerate_callback = context['set_framerate_callback'] # Callback pour synchroniser la fréquence de rafraîchissement
        self.save_config_callback = context['save_config_callback'] #Callback pour enregistrer les paramètres
        self.set_fullscreen_on_start_callback = context.get('set_fullscreen_on_start_callback', None)
        self.bgcolor = tuple(int(x) for x in context.get('bgcolor', (0, 0, 0)))
        self.spritecolor = tuple(int(x) for x in context.get('spritecolor', (255, 255, 255)))
        self.set_bgcolor_callback = context.get('set_bgcolor_callback', None) #Callback pour changer la couleur de fond
        self.set_spritecolor_callback = context.get('set_spritecolor_callback', None) #Callback pour changer la couleur des sprites
        self.set_theme_callback = context.get('set_theme_callback', None) #Callback pour changer le thème
        self.theme = context.get('theme', 'superhero') #Thème actuel
        self.set_toolbar_layout_callback = context.get('set_toolbar_layout_callback', None) #Callback pour la disposition de la toolbar
        self.save_toolbar_callback = context.get('save_toolbar_callback', None) #Callback pour afficher/masquer la toolbar
        self.title(self.translations[self.language]['settings']) #Titre de la fenêtre
        self.geometry('850x850') #Taille de la fenêtre
        self.widgets = {} #Dictionnaire pour stocker les widgets
        self._style = self.master.style if hasattr(self.master, 'style') else tb.Style()
        self.toolbar_layout = context.get('toolbar_layout', 'left')
        self._build_ui() #Construction de l'interface utilisateur

    def _toggle_toolbar(self):
        """
        Fonction pour activer/désactiver la toolbar
        """
        self.toolbar_enabled = self.widgets['var_toolbar'].get()
        if self.save_toolbar_callback:
            self.save_toolbar_callback(self.toolbar_enabled)
       # self.save_config_callback()

    def _toggle_fullscreen_on_start(self):
        """
        Fonction pour activer/désactiver le lancement en plein écran
        """
        self.fullscreen_on_start = self.widgets['var_fullscreen_on_start'].get()
        if hasattr(self, 'set_fullscreen_on_start_callback'):
            self.set_fullscreen_on_start_callback(self.fullscreen_on_start)
        self.save_config_callback()

    def _update_all_framerate(self, val):
        """
        Met à jour la fréquence de rafraîchissement
        """
        t = self._get_translations(self.language)
        try:
            framerate_value = int(float(val))
        except ValueError:
            return
        self.framerate = framerate_value
        if hasattr(self, 'set_framerate_callback'):  #Met à jour la valeur de la fréquence de rafraîchissement
            self.set_framerate_callback(framerate_value)
        self.widgets['fr_value_label'].config(text=f"{t['framerate_unlimited']}" if framerate_value < 0 else f"{framerate_value} Hz") #Label valeur fréq rafraîchissement
        if int(float(self.widgets['fr_slider'].get())) != framerate_value:
            self.widgets['fr_slider'].set(framerate_value)
        if self.widgets['fr_entry_var'].get() != str(framerate_value):
            self.widgets['fr_entry_var'].set(str(framerate_value))

    def _on_slider_change(self, val):
        """
        Fonction appelée lors du changement de la valeur du slider
        """
        self._update_all_framerate(val)

    def _on_slider_release(self, event):
        """
        Fonction appelée lors du relâchement du slider
        """
        self._update_all_framerate(self.widgets['fr_slider'].get())
        self.save_config_callback()

    def _on_entry_validate(self, *args):
        """
        Fonction appelée lors de la validation de l'entrée de texte pour la fréquence de rafraîchissement
        """
        val = self.widgets['fr_entry_var'].get()
        try:
            framerate_value = int(float(val))
            if -1 <= framerate_value <= 1000:
                self._update_all_framerate(framerate_value)
                self.save_config_callback()
        except ValueError:
            pass

    def _on_language_change(self, event=None):
        """
        Fonction appelée lors du changement de langue
        """
        lang_var = self.widgets['lang_var']
        label_to_code = self.widgets['label_to_code']
        selected_label = lang_var.get()
        lang_code = label_to_code[selected_label]
        if lang_code != self.language:
            self.language = lang_code
            self.set_language_callback(lang_code)
            self.save_config_callback()
            self._build_ui()

    def _choose_bgcolor(self):
        """
        Ouvre une boîte de dialogue pour choisir la couleur de fond
        """
        color = cc.askcolor(color=self.bgcolor, title="Choisir la couleur de fond")
        if color and color[0]:
            rgb = tuple(int(x) for x in color[0])
            self.bgcolor = rgb
            self.widgets['bgcolor_btn'].config(bg=self._rgb_to_hex(rgb))
            self.widgets['bgcolor_btn'].itemconfig(self.widgets['bgcolor_rect'], fill=self._rgb_to_hex(rgb))
            if hasattr(self, 'set_bgcolor_callback'):
                self.set_bgcolor_callback(rgb)
            self.save_config_callback()

    def _choose_spritecolor(self):
        """
        Ouvre une boîte de dialogue pour choisir la couleur des sprites
        """
        color = cc.askcolor(color=self.spritecolor, title="Choisir la couleur des sprites")
        if color and color[0]:
            rgb = tuple(int(x) for x in color[0])
            self.spritecolor = rgb
            self.widgets['spritecolor_btn'].config(bg=self._rgb_to_hex(rgb))
            self.widgets['spritecolor_btn'].itemconfig(self.widgets['spritecolor_rect'], fill=self._rgb_to_hex(rgb))
            if hasattr(self, 'set_spritecolor_callback'):
                self.set_spritecolor_callback(rgb)
            self.save_config_callback()

    def _rgb_to_hex(self, rgb):
        """
        Convertit une couleur RGB en format hexadécimal
        """
        return '#%02x%02x%02x' % rgb

    def _on_theme_change(self, event=None):
        theme_var = self.widgets['theme_var']
        selected_theme = theme_var.get()
        if hasattr(self, 'set_theme_callback'):
            self.set_theme_callback(selected_theme)
        try:
            self._style.theme_use(selected_theme)
        except Exception:
            pass
        self.save_config_callback()

    def _on_layout_change(self, event=None):
        layout_var = self.widgets['toolbar_layout_var']
        label_to_value = self.widgets['label_to_value']
        selected_label = layout_var.get()
        selected_layout = label_to_value.get(selected_label, 'left')
        if hasattr(self, 'set_toolbar_layout_callback'):
            self.set_toolbar_layout_callback(selected_layout)
        self.save_config_callback()

    def _build_ui(self):

        """
        Construction de l'interface utilisateur de la fenêtre de paramètres
        """

        t = self._get_translations(self.language)
        for widget in self.winfo_children():
            widget.destroy()

        # Cadre Interface
        lf_interface = tb.Labelframe(self, text=t.get('tab_interface', 'Interface'), bootstyle="info")
        lf_interface.pack(fill='x', padx=20, pady=(20, 10), anchor='n')

        # Toolbar checkbox
        var_toolbar = tb.BooleanVar(value=self.toolbar_enabled)
        self.widgets['var_toolbar'] = var_toolbar
        cb = tb.Checkbutton(lf_interface, text=t.get('show_toolbar', t['show_toolbar']), variable=var_toolbar, command=self._toggle_toolbar, bootstyle="success")
        cb.pack(pady=10, anchor='w', padx=20)
        self.widgets['cb'] = cb

        # Disposition de la toolbar
        layout_values = ['left', 'top']
        layout_labels = [t.get(f'toolbar_layout_{val}', val.capitalize()) for val in layout_values]
        value_to_label = dict(zip(layout_values, layout_labels))
        label_to_value = dict(zip(layout_labels, layout_values))
        self.widgets['label_to_value'] = label_to_value
        current_layout_value = getattr(self, 'toolbar_layout', 'left')
        current_layout_label = value_to_label.get(current_layout_value, current_layout_value)
        toolbar_layout_label = tb.Label(lf_interface, text=t['toolbar_layout'])
        toolbar_layout_label.pack(padx=20, pady=(10,0), anchor='w')
        self.widgets['toolbar_layout_label'] = toolbar_layout_label
        layout_var = tb.StringVar(value=current_layout_label)
        self.widgets['toolbar_layout_var'] = layout_var
        layout_combo = tb.Combobox(lf_interface, textvariable=layout_var, values=layout_labels, state="readonly")
        layout_combo.pack(padx=20, pady=10, anchor='w')
        self.widgets['toolbar_layout_combo'] = layout_combo
        layout_combo.bind('<<ComboboxSelected>>', self._on_layout_change)

        # Sélecteur de thème ttkbootstrap
        style = tb.Style()
        available_themes = style.theme_names()
        theme_label = tb.Label(lf_interface, text=t['theme'])
        theme_label.pack(padx=20, pady=(10,0), anchor='w')
        self.widgets['theme_label'] = theme_label
        current_theme = getattr(self, 'theme', None)
        if not current_theme:
            current_theme = self.master.theme if hasattr(self.master, 'theme') else None
        if not current_theme:
            current_theme = self.translations.get('theme', available_themes[0])
        if not current_theme or current_theme not in available_themes:
            current_theme = available_themes[0]
        theme_var = tb.StringVar(value=self.theme)
        self.widgets['theme_var'] = theme_var
        theme_combo = tb.Combobox(lf_interface, textvariable=theme_var, values=available_themes, state="readonly")
        theme_combo.pack(padx=20, pady=10, anchor='w')
        self.widgets['theme_combo'] = theme_combo
        theme_combo.bind('<<ComboboxSelected>>', self._on_theme_change)

        # Sélecteur de langue
        lang_files = [f for f in os.listdir('lang') if f.endswith('.json')]
        available_langs = [f[:-5] for f in lang_files]
        code_to_label = {}
        for code in available_langs:
            try:
                with open(os.path.join('lang', code + '.json'), 'r', encoding='utf-8') as f:
                    lang_data = json.load(f)
                code_to_label[code] = lang_data.get('language_name', code)
            except Exception:
                code_to_label[code] = code
        label_to_code = {v: k for k, v in code_to_label.items()}
        self.widgets['label_to_code'] = label_to_code
        labels = [code_to_label[code] for code in available_langs]
        current_label = code_to_label.get(self.language, self.language)
        lang_label = tb.Label(lf_interface, text=t['language'])
        lang_label.pack(padx=20, pady=(10,0), anchor='w')
        self.widgets['lang_label'] = lang_label
        lang_var = tb.StringVar(value=current_label)
        self.widgets['lang_var'] = lang_var
        lang_combo = tb.Combobox(lf_interface, textvariable=lang_var, values=labels, state="readonly")
        lang_combo.pack(padx=20, pady=10, anchor='w')
        self.widgets['lang_combo'] = lang_combo
        lang_combo.bind('<<ComboboxSelected>>', self._on_language_change)

        # Cadre Émulation
        lf_emu = tb.Labelframe(self, text=t.get('tab_emulation', 'Émulation'), bootstyle="primary")
        lf_emu.pack(fill='x', padx=20, pady=(10, 10), anchor='n')

        # Plein écran au lancement
        var_fullscreen_on_start = tb.BooleanVar(value=self.fullscreen_on_start)
        self.widgets['var_fullscreen_on_start'] = var_fullscreen_on_start
        cb_fullscreen = tb.Checkbutton(lf_emu, text=t.get('fullscreen_on_start', 'Lancer les jeux en plein écran'), variable=var_fullscreen_on_start, command=self._toggle_fullscreen_on_start, bootstyle="info")
        cb_fullscreen.pack(padx=20, pady=10, anchor='w')
        self.widgets['cb_fullscreen'] = cb_fullscreen

        # Slider + champ d'entrée pour la vitesse d'émulation
        fr_label = tb.Label(lf_emu, text=t['framerate'])
        fr_label.pack(padx=20, pady=(10,0), anchor='w')
        self.widgets['fr_label'] = fr_label
        fr_value_label = tb.Label(lf_emu, text=f"{t['framerate_unlimited']}" if self.framerate < 0 else f"{self.framerate} Hz")
        fr_value_label.pack(anchor='w', padx=20)
        self.widgets['fr_value_label'] = fr_value_label
        framerate_frame = tb.Frame(lf_emu)
        framerate_frame.pack(padx=20, pady=10, anchor='w')
        fr_slider = tb.Scale(framerate_frame, from_=-1, to=1000, orient='horizontal', length=220)
        fr_slider.grid(row=0, column=0, padx=(0,8))
        self.widgets['fr_slider'] = fr_slider
        fr_entry_var = tb.StringVar(value=str(self.framerate))
        self.widgets['fr_entry_var'] = fr_entry_var
        fr_entry = tb.Entry(framerate_frame, textvariable=fr_entry_var, width=7)
        fr_entry.grid(row=0, column=1)
        self.widgets['fr_entry'] = fr_entry
        fr_slider.config(command=self._on_slider_change)
        fr_slider.set(self.framerate)
        fr_slider.bind('<ButtonRelease-1>', self._on_slider_release)
        fr_entry_var.trace_add('write', self._on_entry_validate)

        # Couleurs de fond et des sprites
        color_frame = tb.Frame(lf_emu)
        color_frame.pack(padx=20, pady=(10,0), anchor='w')
        bg_label = tb.Label(color_frame, text=t['bgcolor'])
        bg_label.grid(row=0, column=0, padx=5)
        bgcolor_canvas = tk.Canvas(color_frame, width=40, height=32, highlightthickness=1, highlightbackground="#888")
        bgcolor_rect = bgcolor_canvas.create_rectangle(4, 4, 36, 28, fill=self._rgb_to_hex(self.bgcolor), outline="#444")
        bgcolor_canvas.grid(row=1, column=0, padx=5)
        bgcolor_canvas.bind("<Button-1>", lambda e: self._choose_bgcolor())
        self.widgets['bgcolor_btn'] = bgcolor_canvas
        self.widgets['bgcolor_rect'] = bgcolor_rect

        sprite_label = tb.Label(color_frame, text=t['spritecolor'])
        sprite_label.grid(row=0, column=1, padx=5)
        spritecolor_canvas = tk.Canvas(color_frame, width=40, height=32, highlightthickness=1, highlightbackground="#888")
        spritecolor_rect = spritecolor_canvas.create_rectangle(4, 4, 36, 28, fill=self._rgb_to_hex(self.spritecolor), outline="#444")
        spritecolor_canvas.grid(row=1, column=1, padx=5)
        spritecolor_canvas.bind("<Button-1>", lambda e: self._choose_spritecolor())
        self.widgets['spritecolor_btn'] = spritecolor_canvas
        self.widgets['spritecolor_rect'] = spritecolor_rect

        # Boutons en bas
        btn_frame = tb.Frame(self)
        btn_frame.pack(fill='x', pady=(0,10))
        restore_btn = tb.Button(btn_frame, text=t.get('restore_defaults', 'Restaurer les valeurs par défaut'), bootstyle="warning", command=self._restore_defaults)
        restore_btn.pack(side='left', padx=10)
        self.widgets['restore_btn'] = restore_btn
        ok_btn = tb.Button(btn_frame, text=t.get('ok', 'OK'), bootstyle="success", command=self.destroy)
        ok_btn.pack(side='right', padx=10)
        self.widgets['ok_btn'] = ok_btn



    def _get_translations(self, lang_code):
        """
        Récupère les traductions pour la langue spécifiée.
        """
        # Recharge le fichier de langue si besoin
        if lang_code in self.translations:
            return self.translations[lang_code]
        try:
            with open(os.path.join('lang', lang_code + '.json'), 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return self.translations[self.language]

    def _restore_defaults(self):
        """
        Restaure les valeurs par défaut des paramètres.
        """
        # Valeurs par défaut
        self.bgcolor = (0, 0, 0)
        self.spritecolor = (255, 255, 255)
        self.fullscreen_on_start = False
        self.toolbar_enabled = True
        self.framerate = 500
        # Met à jour les widgets
        self.widgets['bgcolor_btn'].config(bg=self._rgb_to_hex(self.bgcolor))
        self.widgets['bgcolor_btn'].itemconfig(self.widgets['bgcolor_rect'], fill=self._rgb_to_hex(self.bgcolor))
        self.widgets['spritecolor_btn'].config(bg=self._rgb_to_hex(self.spritecolor))
        self.widgets['spritecolor_btn'].itemconfig(self.widgets['spritecolor_rect'], fill=self._rgb_to_hex(self.spritecolor))
        self.widgets['var_fullscreen_on_start'].set(self.fullscreen_on_start)
        self.widgets['var_toolbar'].set(self.toolbar_enabled)
        self.widgets['fr_slider'].set(self.framerate)
        self.widgets['fr_entry_var'].set(str(self.framerate))
        self.widgets['fr_value_label'].config(text=f"{self._get_translations(self.language)['framerate_unlimited']}" if self.framerate < 0 else f"{self.framerate} Hz")
        # Appelle les callbacks pour synchroniser l'UI principale
        if hasattr(self, 'set_bgcolor_callback'):
            self.set_bgcolor_callback(self.bgcolor)
        if hasattr(self, 'set_spritecolor_callback'):
            self.set_spritecolor_callback(self.spritecolor)
        if hasattr(self, 'set_fullscreen_on_start_callback'):
            self.set_fullscreen_on_start_callback(self.fullscreen_on_start)
        if hasattr(self, 'set_framerate_callback'):
            self.set_framerate_callback(self.framerate)
        self.save_config_callback()
