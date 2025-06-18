import tkinter as tk
from tkinter import ttk
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
        self.set_language_callback = context['set_language_callback'] #Callback pour changer la langue
        self.save_framerate_callback = context['save_framerate_callback'] #Callback pour enregistrer la fréquence de rafraîchissement
        self.save_language_callback = context['save_language_callback'] #Callback pour enregistrer la langue
        self.save_toolbar_callback = context['save_toolbar_callback'] #Callback pour enregistrer l'état de la toolbar
        self.title(self.translations[self.language]['settings']) #Titre de la fenêtre
        self.geometry('350x300') #Taille de la fenêtre
        self.widgets = {} #Dictionnaire pour stocker les widgets
        self._build_ui() #Construction de l'interface utilisateur

    def _toggle_toolbar(self):
        """
        Fonction pour activer/désactiver la toolbar
        """
        self.toolbar_enabled = self.widgets['var_toolbar'].get()
        self.save_toolbar_callback(self.toolbar_enabled)

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
        self.save_framerate_callback(self.framerate)

    def _on_entry_validate(self, *args):
        """
        Fonction appelée lors de la validation de l'entrée de texte pour la fréquence de rafraîchissement
        """
        val = self.widgets['fr_entry_var'].get()
        try:
            framerate_value = int(float(val))
            if -1 <= framerate_value <= 1000:
                self._update_all_framerate(framerate_value)
                self.save_framerate_callback(framerate_value)
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
            self.save_language_callback(lang_code)
            self._build_ui()

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
        cb.pack(pady=20)
        self.widgets['cb'] = cb


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
