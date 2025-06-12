#coding:utf8

import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import json
import os
import CHIP_8 as C8

CONFIG_FILE = "config.json"

class UI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sheep 8")
        self.create_menu()
        self.rom_list = [] #Liste des ROMs
        self.rom_path = None #Initialisation du chemin de la ROM
        self.emulation_thread = None
        self.is_running = False #Statut de l'émulation
        self.rom_listbox = None
        self.stop_event = threading.Event()  # Ajout de l'événement d'arrêt
        self.loaded_folders = [] #Liste des dossiers chargés précédemment
        self.load_folders_history()
        self.create_rom_listbox()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        # Charger les ROMs de tous les dossiers précédemment ouverts
        for folder in self.loaded_folders:
            if os.path.isdir(folder):
                self.rom_list += [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(('.ch8'))]
        self.update_rom_listbox()

    def create_menu(self):
        """
        Création de la barre de menu
        """

        #Bouton Fichier
        menubar= tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Ouvrir ROM", command=self.open_file, accelerator="Ctrl+O")
        self.root.bind('<Control-o>', lambda event: self.open_file())
        file_menu.add_command(label="Ouvrir dossier", command=self.open_folder, accelerator="Ctrl+Shift+O")
        self.root.bind('<Control-Shift-O>', lambda event: self.open_folder())
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit, accelerator="Ctrl+Q")
        self.root.bind('<Control-q>', lambda event: self.root.quit())
        menubar.add_cascade(label="Fichier", menu=file_menu)

        #Bouton Contrôle
        control_menu = tk.Menu(menubar, tearoff=0)
        control_menu.add_command(label="Démarrer", command=self.play_emulation, accelerator="F5")
        self.root.bind('<F5>', lambda event: self.play_emulation())
        control_menu.add_command(label="Arrêter", command=self.stop_emulation, accelerator="F6")
        self.root.bind('<F6>', lambda event: self.stop_emulation())
        control_menu.add_command(label="Réinitialiser", command=self.reset_emulation, accelerator="F7")
        self.root.bind('<F7>', lambda event: self.reset_emulation())
        menubar.add_cascade(label="Contrôle", menu=control_menu)

        #Bouton Options
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Préférences", command=self.show_settings, accelerator="Ctrl+P")
        self.root.bind('<Control-p>', lambda event: self.show_settings())
        menubar.add_cascade(label="Options", menu=settings_menu)

        #Bouton Aide
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Aide", command=self.show_help, accelerator="F1")
        self.root.bind('<F1>', lambda event: self.show_help())
        help_menu.add_command(label="À propos", command=self.show_about, accelerator="F2")
        self.root.bind('<F2>', lambda event: self.show_about())
        menubar.add_cascade(label="Aide", menu=help_menu)

        self.root.config(menu=menubar)

    def create_rom_listbox(self):
        """
        Création de la liste des ROMs
        """
        self.rom_listbox = tk.Listbox(self.root, width=50)
        self.rom_listbox.pack(fill=tk.BOTH, expand=True) #Ajustement de la taille de la liste à la fenêtre
        self.rom_listbox.bind('<Double-1>', self.on_rom_double_click) #Double-clic pour charger la ROM

    def open_file(self):
        """
        Ouverture de l'explorateur de fichiers pour sélectionner une ROM
        """
        path = filedialog.askopenfilename(
            title="Ouvrir une ROM",
            filetypes=[("ROMs Chip-8", "*.ch8;*.chip8"),("All files", "*.*")] #Types de fichiers acceptés
        )
        if path:
            self.rom_list = [path]
            self.update_rom_listbox()     #Mise à jour de la liste des ROMs pour afficher la ROM sélectionnée
            self.rom_path = path
            self.play_emulation()

    def open_folder(self):
        """
        Ouverture de l'explorateur de fichiers pour sélectionner un dossier contenant des ROMs et l'ajouter à la liste
        """
        folder = filedialog.askdirectory(title="Choisir le dossier des ROMs")
        if folder:
            if folder not in self.loaded_folders:
                self.loaded_folders.append(folder) #Ajout du dossier à la liste des dossiers chargés
            self.save_folders_history()
            self.rom_list += [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(('.ch8'))] #Ajout des ROMs du dossier à la liste
            self.update_rom_listbox()   #Mise à jour de la liste des ROMs
            if not any(f.lower().endswith('.ch8') for f in os.listdir(folder)):
                messagebox.showinfo("Avertissement", "Aucune ROM .ch8 trouvée dans le dossier sélectionné. Vérifiez le dossier sélectionné ou son contenu.")

    def update_rom_listbox(self):
        """
        Mise à jour de la liste des ROMs dans la Listbox
        """
        self.rom_listbox.delete(0, tk.END) #Effacement de la liste actuelle
        # Supprimer les doublons tout en conservant l'ordre
        seen = set()
        unique_roms = []
        for rom in self.rom_list:
            if rom not in seen:
                unique_roms.append(rom)
                seen.add(rom)
        for rom in unique_roms:
            self.rom_listbox.insert(tk.END, os.path.basename(rom)) #Ajout des ROMs à la liste
        self.rom_list = unique_roms
    
    def on_rom_double_click(self, event):
        """
        Chargement de la ROM sélectionnée au double-clic
        """
        selection = self.rom_listbox.curselection()
        if selection:
            self.rom_path = self.rom_list[selection[0]]
            self.play_emulation()

    def play_emulation(self):
        """
        Démarrage de l'émulation
        """
        if not self.rom_path:
            selection = self.rom_listbox.curselection()
            if selection:
                self.rom_path = self.rom_list[selection[0]]
        if not self.rom_path:
            messagebox.showwarning("Avertissement", "Aucune ROM sélectionnée. L'émulation ne peut pas démarrer.")
            return
        if not self.is_running:
            self.is_running = True
            self.stop_event.clear() 
            self.emulation_thread = threading.Thread(target=self.run_emulator)
            self.emulation_thread.start()

    def stop_emulation(self):
        """
        Arrêt de l'émulation
        """
        if self.is_running:
            self.is_running = False
            self.stop_event.set()  
            if self.emulation_thread is not None:
                self.emulation_thread.join()
            messagebox.showinfo("Information", "L'émulation a été arrêtée. Fermez la fenêtre de jeu si nécessaire.")

    def reset_emulation(self):
        """
        Réinitialisation de l'émulation
        """
        if not self.rom_path:
            messagebox.showwarning("Avertissement", "Aucune ROM sélectionnée. Impossible de réinitialiser l'émulation.")
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

    def show_settings(self):
        """
        Affichage des paramètres de l'émulateur
        """
        messagebox.showinfo("Paramètres", "Aucune option configurable pour le moment. Restez à l'écoute des prochaines mises à jour :) !")

    def show_help(self):
        """
        Affichage de l'aide
        """
        messagebox.showinfo("Aide", "Bienvenue dans Sheep 8 !\n\n"
                                "Pour démarrer l'émulation, ouvrez une ROM en utilisant le menu Fichier.\n"
                                "Utilisez le menu Contrôle pour démarrer ou arrêter l'émulation.\n"
                                "Pour toute autre question, consultez la documentation.")
        
    def show_about(self):
        """
        Affichage des informations sur l'application
        """
        messagebox.showinfo("À propos", "Sheep 8 - Émulateur CHIP-8\n\n"
                                "Développé par 2LazyCoffee2 et TortipOOF\n"
                                "Version beta 0.2.0\n"
                                "Pour plus d'informations, consultez le dépôt GitHub.")
        
    def run_emulator(self):
        """
        Exécution de l'émulateur
        """
        C8.run(self.rom_path, self.stop_event)
        self.is_running = False # Quand la fenêtre de jeu se ferme, le statut de l'émulation est mis à jour

    def save_folders_history(self):
        """
        Sauvegarde de l'historique des dossiers chargés dans le fichier de config
        """
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump({'folders': self.loaded_folders}, f)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde des dossiers: {e}")

    def load_folders_history(self):
        """
        Chargement de l'historique des dossiers à partir du fichier de config
        """
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.loaded_folders = data.get('folders', [])
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des dossiers: {e}")

    def on_close(self):
        self.save_folders_history()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("assets/icon/icon.ico")
    ui = UI(root)
    root.mainloop()