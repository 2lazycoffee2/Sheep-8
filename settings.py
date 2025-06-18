import tkinter as tk
from tkinter import ttk
import tkinter.colorchooser as cc
import os
import json

class SettingsWindow(tk.Toplevel):

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
        self.set_bgcolor_callback = context.get('set_bgcolor_callback', None)
        self.set_spritecolor_callback = context.get('set_spritecolor_callback', None)
        self.title(self.translations[self.language]['settings']) #Titre de la fenêtre
        self.geometry('420x420') #Taille de la fenêtre
        self.widgets = {} #Dictionnaire pour stocker les widgets
        self._build_ui() #Construction de l'interface utilisateur

    def _toggle_toolbar(self):
        """
        Fonction pour activer/désactiver la toolbar
        """
        self.toolbar_enabled = self.widgets['var_toolbar'].get()
        self.save_config_callback()

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

        if hasattr(self, 'set_framerate_callback'):  #Met à jour la valeur dans l'objet principal (UI)
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
            if hasattr(self, 'set_spritecolor_callback'):
                self.set_spritecolor_callback(rgb)
            self.save_config_callback()

    def _rgb_to_hex(self, rgb):
        """
        Convertit une couleur RGB en format hexadécimal
        """
        return '#%02x%02x%02x' % rgb

    def _build_ui(self):

        """
        Construction de l'interface utilisateur de la fenêtre de paramètres
        """

        t = self._get_translations(self.language)
        for widget in self.winfo_children():
            widget.destroy()


        # Toolbar checkbox
        var_toolbar = tk.BooleanVar(value=self.toolbar_enabled)
        self.widgets['var_toolbar'] = var_toolbar
        cb = ttk.Checkbutton(self, text=t.get('show_toolbar', t['show_toolbar']), variable=var_toolbar, command=self._toggle_toolbar)
        cb.pack(pady=10)
        self.widgets['cb'] = cb

        # Plein écran au lancement
        var_fullscreen_on_start = tk.BooleanVar(value=self.fullscreen_on_start)
        self.widgets['var_fullscreen_on_start'] = var_fullscreen_on_start
        cb_fullscreen = ttk.Checkbutton(self, text=t.get('fullscreen_on_start', 'Lancer les jeux en plein écran'), variable=var_fullscreen_on_start, command=self._toggle_fullscreen_on_start)
        cb_fullscreen.pack(pady=5)
        self.widgets['cb_fullscreen'] = cb_fullscreen


        # Slider + champ d'entrée pour la vitesse d'émulation
        fr_label = tk.Label(self, text=t['framerate'])
        fr_label.pack(pady=(5,0))
        self.widgets['fr_label'] = fr_label
        fr_value_label = tk.Label(self, text=f"{t['framerate_unlimited']}" if self.framerate < 0 else f"{self.framerate} Hz")
        fr_value_label.pack()
        self.widgets['fr_value_label'] = fr_value_label
        framerate_frame = tk.Frame(self)
        framerate_frame.pack(pady=5)
        fr_slider = ttk.Scale(framerate_frame, from_=-1, to=1000, orient='horizontal', length=220)
        fr_slider.grid(row=0, column=0, padx=(0,8))
        self.widgets['fr_slider'] = fr_slider
        fr_entry_var = tk.StringVar(value=str(self.framerate))
        self.widgets['fr_entry_var'] = fr_entry_var
        fr_entry = ttk.Entry(framerate_frame, textvariable=fr_entry_var, width=7)
        fr_entry.grid(row=0, column=1)
        self.widgets['fr_entry'] = fr_entry
        fr_slider.config(command=self._on_slider_change)
        fr_slider.set(self.framerate)
        fr_slider.bind('<ButtonRelease-1>', self._on_slider_release)
        fr_entry_var.trace_add('write', self._on_entry_validate)


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
        lang_label = tk.Label(self, text=t['language'])
        lang_label.pack(pady=(5,0))
        self.widgets['lang_label'] = lang_label
        lang_var = tk.StringVar(value=current_label)
        self.widgets['lang_var'] = lang_var
        lang_combo = ttk.Combobox(self, textvariable=lang_var, values=labels, state="readonly")
        lang_combo.pack(pady=5)
        self.widgets['lang_combo'] = lang_combo
        lang_combo.bind('<<ComboboxSelected>>', self._on_language_change)

        # Couleurs de fond et des sprites
        color_frame = tk.Frame(self)
        color_frame.pack(pady=(10,0))
        t = self._get_translations(self.language)
        bg_label = tk.Label(color_frame, text=t.get('bgcolor', 'Couleur de fond'))
        bg_label.grid(row=0, column=0, padx=5)
        bgcolor_btn = tk.Button(color_frame, bg=self._rgb_to_hex(self.bgcolor), width=8, command=self._choose_bgcolor)
        bgcolor_btn.grid(row=1, column=0, padx=5)
        self.widgets['bg_label'] = bg_label
        self.widgets['bgcolor_btn'] = bgcolor_btn
        sprite_label = tk.Label(color_frame, text=t.get('spritecolor', 'Couleur des sprites'))
        sprite_label.grid(row=0, column=1, padx=5)
        spritecolor_btn = tk.Button(color_frame, bg=self._rgb_to_hex(self.spritecolor), width=8, command=self._choose_spritecolor)
        spritecolor_btn.grid(row=1, column=1, padx=5)
        self.widgets['sprite_label'] = sprite_label
        self.widgets['spritecolor_btn'] = spritecolor_btn

        # Bouton Restaurer les valeurs par défaut
        restore_btn = ttk.Button(self, text=t.get('restore_defaults', 'Restaurer les valeurs par défaut'), command=self._restore_defaults)
        restore_btn.pack(pady=8)
        self.widgets['restore_btn'] = restore_btn

        # Bouton OK
        ok_btn = ttk.Button(self, text=t.get('ok', 'OK'), command=self.destroy)
        ok_btn.pack(pady=10)
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
        self.widgets['spritecolor_btn'].config(bg=self._rgb_to_hex(self.spritecolor))
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
