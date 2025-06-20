#coding:utf8

import ttkbootstrap as tb
from ttkbootstrap.constants import *
import display as disp
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from pypresence import Presence  # Pour la présence Discord
import time
import json
import os
import sys
import CHIP_8 as C8
from PIL import Image, ImageTk
from toolbar import Toolbar
from settings import SettingsWindow

CONFIG_FILE = "config.json"
LANG_DIR = "lang"

class UI:
    def __init__(self, root):
        """
        Initialisation de l'interface utilisateur
        """
        self.root = root
        self.root.title("Sheep 8")  #Titre de la fenêtre
        config = self.load_config() #Chargement du fichier de config
        self.language = config['language'] #Chargement de la langue
        self.translations = {self.language: self.load_translations(self.language)}
        self.loaded_folders = config['folders'] #Liste des dossiers chargés précédemment
        self.rom_list = [] # Liste des ROMs
        self.rom_path = None # Initialisation du chemin de la ROM
        self.emulation_thread = None
        self.is_running = False #Statut de l'émulation
        self.rom_listbox = None
        self.stop_event = threading.Event() #Évènement d'arrêt
        self.toolbar = None
        self.toolbar_enabled = config.get('toolbar_enabled', True)  # Pour activer/désactiver la toolbar dynamiquement
        self.framerate = config['framerate']  #Vitesse d'émulation
        self.fullscreen_on_start = config.get('fullscreen_on_start', False) #Plein écran au démarrage
        self.bgcolor = config.get('bgcolor', (0, 0, 0)) #Couleur des pixels "éteints"
        self.spritecolor = config.get('spritecolor', (255, 255, 255)) #Couleur des pixels "allumés"
        self.theme = config.get('theme', 'superhero') #Thème de l'interface
        self.toolbar_layout = config.get('toolbar_layout', 'left') #Disposition de la toolbar
        self.set_theme(self.theme) #Définition du thème
        self.create_menu()
        if self.toolbar_enabled:
            self.create_toolbar()
        self.create_rom_listbox()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        # Charger les ROMs de tous les dossiers précédemment ouverts
        for folder in self.loaded_folders:
            if os.path.isdir(folder):
                self.rom_list += [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(('.ch8'))]
        self.update_rom_listbox()
        # Initialisation de la présence Discord
        self.discord_connected = False
        self.rpc = None
        self.discord_start_time = None
        self.discord_client_id = "1385527884923535433"  #ID de l'application Discord
        self._init_discord_rpc()

    def _init_discord_rpc(self):
        """
        Initialisation de la présence Discord
        """
        try:
            self.rpc = Presence(self.discord_client_id)
            self.rpc.connect()
            self.discord_connected = True
            self.discord_start_time = int(time.time())
            self.update_discord_presence()
        except Exception as e:
            print(f"[DEBUG] Erreur lors de l'initialisation de la présence Discord: {e}")
            self.discord_connected = False

    def update_discord_presence(self, state=None):
        """
        Mise à jour de la présence Discord
        """
        if not self.discord_connected or not self.rpc:
            return
        try:
            if self.is_running:
                state = "En cours d'émulation" if state is None else state
                details = f"Joue à {os.path.basename(self.rom_path)}" if self.rom_path else "Aucune ROM chargée"
            else:
                state = "En attente" if state is None else state
                details = "Aucune ROM chargée"
            self.rpc.update(
                state=state,
                details=details,
                start=self.discord_start_time,
                large_image="sheep",
                small_image="play"
            )
        except Exception as e:
            print(f"[DEBUG] Erreur lors de la mise à jour de la présence Discord: {e}")

    def clear_discord_presence(self):
        """
        Efface la présence Discord
        """
        if self.discord_connected and self.rpc:
            try:
                self.rpc.clear()
            except Exception as e:
                print(f"[DEBUG] Erreur lors de l'effacement de la présence Discord: {e}")
            finally:
                self.discord_connected = False

    def set_theme(self, theme):
        """
        Définit le thème de l'interface utilisateur et le sauvegarde
        """
        #print(f"[DEBUG] set_theme called with: {theme}")
        try:
            self.root.style.theme_use(theme) #Application du thème
            self.theme = theme #Synchronisation de l'attribut
            self.save_config()
        except Exception:
            self.root.style.theme_use("superhero") #Thème par défaut
            self.theme = "superhero"
            self.save_config()

    def load_translations(self, lang):
        """
        Chargement des traductions depuis le fichier JSON de la langue spécifiée
        """
        try:
            with open(os.path.join(LANG_DIR, f"{lang}.json"), 'r', encoding='utf-8') as f:
                data = json.load(f)
            #Conversion des types de fichiers en tuples pour la listbox
            if 'filetypes' in data:
                data['filetypes'] = [tuple(ft) for ft in data['filetypes']]
            return data
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement de la langue : {e}")
            return {}

    def set_language(self, lang):
        """
        Changement de la langue de l'interface utilisateur
        """
        self.language = lang
        self.save_config()
        if lang not in self.translations:
            self.translations[lang] = self.load_translations(lang)
        self.create_menu()
        if self.toolbar_enabled:
            self.create_toolbar()
        self.create_rom_listbox()  # Recréation de la listbox pour mettre à jour les headers

    def create_menu(self):
        """
        Création de la barre de menu
        """
        
        #Bouton Fichier
        t = self.translations[self.language]
        menubar = tb.Menu(self.root)
        file_menu = tb.Menu(menubar, tearoff=0)
        file_menu.add_command(label=t['open_rom'], command=self.open_file, accelerator="Ctrl+O")
        self.root.bind('<Control-o>', lambda event: self.open_file())
        file_menu.add_command(label=t['open_folder'], command=self.open_folder, accelerator="Ctrl+Shift+O")
        self.root.bind('<Control-Shift-O>', lambda event: self.open_folder())
        file_menu.add_separator()
        file_menu.add_command(label=t['quit'], command=self.root.quit, accelerator="Ctrl+Q")
        self.root.bind('<Control-q>', lambda event: self.root.quit())
        menubar.add_cascade(label=t['menu_file'], menu=file_menu)

        #Bouton Contrôle
        control_menu = tb.Menu(menubar, tearoff=0)
        control_menu.add_command(label=t['start'], command=self.play_emulation, accelerator="F5")
        self.root.bind('<F5>', lambda event: self.play_emulation())
        control_menu.add_command(label=t['stop'], command=self.stop_emulation, accelerator="F6")
        self.root.bind('<F6>', lambda event: self.stop_emulation())
        control_menu.add_command(label=t['reset'], command=self.reset_emulation, accelerator="F7")
        self.root.bind('<F7>', lambda event: self.reset_emulation())
        menubar.add_cascade(label=t['menu_control'], menu=control_menu)

        #Bouton Options
        settings_menu = tb.Menu(menubar, tearoff=0)
        settings_menu.add_command(label=t['fullscreen'], command=self.toggle_fullscreen, accelerator="F11")
        self.root.bind('<F11>', lambda event: self.toggle_fullscreen())
        settings_menu.add_separator()
        settings_menu.add_command(label=t['preferences'], command=self.show_settings, accelerator="Ctrl+P")
        self.root.bind('<Control-p>', lambda event: self.show_settings())
        menubar.add_cascade(label=t['menu_options'], menu=settings_menu)

        #Bouton Aide
        help_menu = tb.Menu(menubar, tearoff=0)
        help_menu.add_command(label=t['help'], command=self.show_help, accelerator="F1")
        self.root.bind('<F1>', lambda event: self.show_help())
        help_menu.add_command(label=t['about'], command=self.show_about, accelerator="F2")
        self.root.bind('<F2>', lambda event: self.show_about())
        help_menu.add_command(label=t['github'], command=lambda: os.startfile("https://github.com/2LazyCoffee2/Python_Project"))
        menubar.add_cascade(label=t['menu_help'], menu=help_menu)

        self.root.config(menu=menubar)


    def create_toolbar(self):
        """
        Affichage de la toolbar
        """
        # Détruit la toolbar si elle existe déjà
        if hasattr(self, 'toolbar') and self.toolbar is not None:
            self.toolbar.toolbar.pack_forget()
            self.toolbar.destroy()
        t = self.translations[self.language]
        actions = {
            'open_rom': self.open_file,
            'start': self.play_emulation,
            'stop': self.stop_emulation,
            'fullscreen': self.toggle_fullscreen,
            'preferences': self.show_settings,
            'help': self.show_help
        }
        font_path = "assets/fonts/Address Sans Pro SemiBold.ttf"
        # Création de la toolbar avec les actions et le thème
        self.toolbar = Toolbar(
            self.root,
            lambda: t,
            actions,
            is_running=lambda: self.is_running,
            theme_bg=self.root.cget('bg'),
            font_path=font_path,
            layout=self.toolbar_layout
        )
        self.toolbar.toolbar.pack_forget()
        self.toolbar.toolbar.pack(side=tb.TOP, fill=tb.X, before=self.rom_listbox if self.rom_listbox else None)

    def create_rom_listbox(self):
        """
        Création de la liste des ROMs
        """
        t = self.translations[self.language]
        columns = ('name', 'size')
        # Si la listbox existe déjà, on la détruit pour la recréer avec les bons headers
        if self.rom_listbox is not None:
            self.rom_listbox.destroy()
        self.rom_listbox = tb.Treeview(self.root, columns=columns, show='headings', bootstyle="info")
        self.rom_listbox.heading('name', text=t.get('name', 'Nom'))
        # Ajout de l'unité à la taille
        size_unit = t.get('size_unit', 'o')
        self.rom_listbox.heading('size', text=f"{t.get('size', 'Taille')} ({size_unit})")
        self.rom_listbox.column('name', width=300, anchor='w')
        self.rom_listbox.column('size', width=100, anchor='w')
        self.rom_listbox.pack(fill=tb.BOTH, expand=True) #Ajustement de la taille de la liste à la fenêtre
        self.rom_listbox.bind('<Double-1>', self.on_rom_double_click) #Double-clic pour charger la ROM
        self.rom_listbox.bind('<Return>', self.on_rom_double_click) #Appui sur Entrée pour charger la ROM
        self.update_rom_listbox()

    def open_file(self):
        """
        Ouverture de l'explorateur de fichiers pour sélectionner une ROM
        """
        t = self.translations[self.language]
        path = filedialog.askopenfilename(
            title=t['open_rom'],
            filetypes=t['filetypes'] #Tyes de fichiers acceptés
        )
        if path:
            self.rom_list = [path]
            self.update_rom_listbox()     #Mise à jour de la liste des ROMs pour afficher la ROM sélectionnée
            self.rom_path = path
            self.play_emulation()
            self.update_discord_presence(state="En jeu")

    def open_folder(self):
        """
        Ouverture de l'explorateur de fichiers pour sélectionner un dossier contenant des ROMs
        """
        t = self.translations[self.language]
        folder = filedialog.askdirectory(title=t['choose_folder'])
        if folder:
            if folder not in self.loaded_folders:
                self.loaded_folders.append(folder) #Ajout du dossier à la liste des dossiers chargés
            self.save_config()
            self.rom_list += [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(('.ch8'))] #Ajout des ROMs du dossier à la liste
            self.update_rom_listbox()   #Mise à jour de la liste des ROMs
            if not any(f.lower().endswith('.ch8') for f in os.listdir(folder)):
                messagebox.showinfo(t['help'], t['no_roms_in_folder'])

    def update_rom_listbox(self):
        """
        Mise à jour de la liste des ROMs dans la Listbox
        """
        t=self.translations[self.language]
        for item in self.rom_listbox.get_children(): #Effacement de la liste actuelle
            self.rom_listbox.delete(item)
        # Supprimer les doublons tout en conservant l'ordre
        seen = set()
        unique_roms = []
        for rom in self.rom_list:
            if rom not in seen:
                unique_roms.append(rom)
                seen.add(rom)
        size_unit = t['size_unit']
        for rom in unique_roms:
            size = os.path.getsize(rom)
            self.rom_listbox.insert('', 'end', values=(os.path.basename(rom), f"{size} {size_unit}"))
        self.rom_list = unique_roms
    
    def on_rom_double_click(self, event):
        """
        Chargement de la ROM sélectionnée au double-clic
        """
        selected = self.rom_listbox.selection()
        if selected:
            self.rom_path = self.rom_list[self.rom_listbox.index(selected[0])]
            self.play_emulation()
            self.update_discord_presence(state="En jeu")

    def play_emulation(self):
        """
        Démarrage de l'émulation
        """
        t = self.translations[self.language]
        if not self.rom_path:
            selection = self.rom_listbox.selection()
            if selection:
                self.rom_path = self.rom_list[self.rom_listbox.index(selection[0])]
        if not self.rom_path:
            messagebox.showwarning(t['help'], t['warning_no_rom'])
            return
        if not self.is_running:
            self.is_running = True
            self.stop_event.clear()
            self.emulation_thread = threading.Thread(target=self.run_emulator)
            self.emulation_thread.start()
            self.discord_start_time = int(time.time())
            self.update_discord_presence(state="En jeu")
        if self.toolbar:
            self.update_toolbar()

    def stop_emulation(self):
        """
        Arrêt de l'émulation
        """
        t = self.translations[self.language]
        if self.is_running:
            self.is_running = False
            self.stop_event.set()
            self.update_discord_presence(state="Menu principal - Aucune ROM chargée")
            #messagebox.showinfo(t['help'], t['info_stopped'])
            if self.toolbar:
                self.update_toolbar()

    def reset_emulation(self):
        """
        Réinitialisation de l'émulation
        """
        t = self.translations[self.language]
        if not self.rom_path:
            messagebox.showwarning(t['help'], t['warning_no_rom_reset'])
            return
        if self.is_running:
            self.is_running = False
            self.stop_event.set()
            if self.emulation_thread is not None:
                self.emulation_thread.join()
        self.stop_event.clear()
        self.is_running = True
        self.emulation_thread = threading.Thread(target=self.run_emulator)
        self.emulation_thread.start()
        if self.toolbar:
            self.update_toolbar()

    def _set_fullscreen_on_start_callback(self, enabled):
        """
        Callback pour sauvegarder l'option plein écran au lancement
        """
        self.fullscreen_on_start = enabled
        self.save_config()

    def _set_bgcolor_callback(self, rgb):
        """
        Callback pour changer la couleur de fond
        """
        self.bgcolor = rgb
        self.save_config()
        if hasattr(self, '_monitor') and self._monitor:
            self._monitor.bgcolor = rgb

    def _set_spritecolor_callback(self, rgb):
        """
        Callback pour changer la couleur des sprites
        """
        self.spritecolor = rgb
        self.save_config()
        if hasattr(self, '_monitor') and self._monitor:
            self._monitor.spritecolor = rgb

    def show_settings(self):
        """
        Affichage des paramètres de l'émulateur
        """
        settings_context = {
            'translations': self.translations,
            'language': self.language,
            'toolbar_enabled': self.toolbar_enabled,
            'framerate': self.framerate,
            'fullscreen_on_start': self.fullscreen_on_start,
            'bgcolor': getattr(self, 'bgcolor', (0, 0, 0)),
            'spritecolor': getattr(self, 'spritecolor', (255, 255, 255)),
            'theme': self.theme,
            'set_language_callback': self._set_language_callback,
            'set_framerate_callback': self._set_framerate_callback,
            'set_fullscreen_on_start_callback': self._set_fullscreen_on_start_callback,
            'set_bgcolor_callback': self._set_bgcolor_callback,
            'set_spritecolor_callback': self._set_spritecolor_callback,
            'set_theme_callback': self.set_theme,
            'save_config_callback': self.save_config,
            'save_toolbar_callback': self._save_toolbar_callback,
            'set_toolbar_layout_callback': self._set_toolbar_layout_callback,
            'toolbar_layout': self.toolbar_layout
        }
        SettingsWindow(self.root, settings_context)

    def _set_toolbar_layout_callback(self, layout):
        """
        Callback pour changer la disposition de la toolbar
        """
        self.toolbar_layout = layout
        if self.toolbar:
            self.create_toolbar()
        self.save_config()

    def _set_language_callback(self, lang_code):
        """
        Callback pour changer la langue
        """
        self.set_language(lang_code)

    def _set_framerate_callback(self, framerate):
        """
        Callback pour régler le framerate
        """
        self.framerate = framerate

    def _save_framerate_callback(self, framerate):
        """
        Callback pour sauvegarder le framerate
        """
        self.save_framerate(framerate)

    def _save_toolbar_callback(self, enabled):
        """
        Callback pour sauvegarder l'état de la toolbar
        """
        self.toolbar_enabled = enabled
        if enabled:
            self.create_toolbar()
        else:
            if self.toolbar:
                self.toolbar.destroy()
                self.toolbar = None

    def show_help(self):
        """
        Affichage de l'aide
        """
        t = self.translations[self.language]
        messagebox.showinfo(t['help'], t['help_msg'])

    def show_about(self):
        """
        Affichage des informations sur l'émulateur
        """
        t = self.translations[self.language]
        messagebox.showinfo(t['about'], t['about_msg'])

    def _monitor_factory(self):
        """
        Factory pour créer un objet Display
        """
        self._monitor = disp.Display()
        self._monitor.bgcolor = getattr(self, 'bgcolor', (0, 0, 0))
        self._monitor.spritecolor = getattr(self, 'spritecolor', (255, 255, 255))
        return self._monitor

    def run_emulator(self):
        """
        Exécution de l'émulateur
        """
        self._fullscreen_toggle_requested = threading.Event()
        C8.run(
            self.rom_path,
            self.stop_event,
            self.framerate,
            fullscreen=self.fullscreen_on_start,
            monitor_factory=self._monitor_factory,
            fullscreen_toggle_event=self._fullscreen_toggle_requested
        )
        self.is_running = False
        if self.toolbar:
            self.update_toolbar()

    def toggle_fullscreen(self):
        """
        Demande à l'émulateur de basculer en mode plein écran
        """
        if hasattr(self, '_fullscreen_toggle_requested') and self._fullscreen_toggle_requested is not None:
            self._fullscreen_toggle_requested.set()
        else:
            messagebox.showinfo("Info", "L'émulation doit être lancée pour activer le plein écran.")

    def save_config(self):
        """
        Sauvegarde centralisée de toutes les préférences utilisateur dans config.json
        """
        data = {
            'folders': self.loaded_folders,
            'language': self.language,
            'framerate': self.framerate,
            'fullscreen_on_start': getattr(self, 'fullscreen_on_start', False),
            'bgcolor': getattr(self, 'bgcolor', (0, 0, 0)),
            'spritecolor': getattr(self, 'spritecolor', (255, 255, 255)),
            'theme': getattr(self, 'theme', 'superhero'),
            'toolbar_layout': getattr(self, 'toolbar_layout', 'left'),
            'toolbar_enabled': self.toolbar_enabled
        }
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde de la configuration: {e}")

    def load_config(self):
        """
        Charge toutes les préférences utilisateur depuis config.json
        """
        config = {'folders': [], 'language': 'fr', 'framerate': 500, 'fullscreen_on_start': False, 'bgcolor': (0, 0, 0), 'spritecolor': (255, 255, 255), 'theme': 'superhero'}
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    config.update(data)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement de la configuration: {e}")
        return config

    def on_close(self):
        """
        Actions à réaliser lors de la fermeture
        """
        self.save_config()
        self.root.destroy()
        self.clear_discord_presence()
        if self.rpc:
            try:
                self.rpc.close()
            except Exception as e:
                pass

    def update_toolbar(self):
        """
        Mise à jour de la toolbar
        """
        if self.toolbar and hasattr(self.toolbar, 'toolbar'):
            self.toolbar.update()
            self.toolbar.toolbar.pack_forget()
            self.toolbar.toolbar.pack(side=tb.TOP, fill=tb.X, before=self.rom_listbox if self.rom_listbox else None)

if __name__ == "__main__":
    root = tb.Window(themename="superhero")
    if sys.platform.startswith('win'):
        root.iconbitmap("assets/icon/icon.ico")
    else:
        root.iconphoto(True, tk.PhotoImage(file="assets/icon/sheep-256.png"))
    ui = UI(root)
    root.mainloop()