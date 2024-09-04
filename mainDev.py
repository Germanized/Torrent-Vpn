import customtkinter as ctk
import os
import subprocess
from tkinter import filedialog, messagebox
from PIL import Image
import win32com.client

TORRENT_SOFTWARES = {
    "qBittorrent": "C:\\Program Files\\qBittorrent\\qbittorrent.exe",
    "BitTorrent": "C:\\Program Files\\BitTorrent\\bittorrent.exe",
    "Vuze": "C:\\Program Files\\Vuze\\azureus.exe",
    "Deluge": "C:\\Program Files\\Deluge\\deluge.exe",
    "Transmission": "C:\\Program Files\\Transmission\\transmission-qt.exe",
    "uTorrent": "C:\\Program Files\\uTorrent\\uTorrent.exe",
    "BitLord": "C:\\Program Files\\BitLord\\bitlord.exe",
    "Tixati": "C:\\Program Files\\Tixati\\tixati.exe",
    "BitComet": "C:\\Program Files\\BitComet\\BitComet.exe"
}

class SoftwareEntry(ctk.CTkFrame):
    def __init__(self, master, logo_name, software_name, path, edit_command):
        super().__init__(master, corner_radius=24, border_width=0, fg_color=["#c6ced8", "#121212"])
        self.edit_command = edit_command
        self.path = path
        self.configure(corner_radius=24, border_width=0, fg_color=["#c6ced8", "#121212"], border_color=["#586b78", "#586b78"])
        self.logo = ctk.CTkLabel(self, image=self.load_image(logo_name, (30, 30)), bg_color="transparent", text="")
        self.logo.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.name_label = ctk.CTkLabel(self, text=software_name, text_color=["#2b3449", "#c3cbd5"], fg_color="transparent")
        self.name_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.path_frame = ctk.CTkFrame(self, corner_radius=12, fg_color=["#a9b8c4", "#a9b8c4"], border_color=["#3d4956", "#141414"])
        self.path_frame.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
        self.path_label = ctk.CTkLabel(self.path_frame, text=path, text_color=["#2b3449", "#2b3449"], fg_color="transparent")
        self.path_label.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="w")
        self.edit_button = ctk.CTkButton(self.path_frame, text="✎", width=30, height=20, command=self.edit_command,
                                        corner_radius=16, fg_color=["#697b88", "#11202b"], hover_color=["#525e6b", "#404c59"],
                                        border_color=["#405366", "#405366"], text_color=["#ffffff", "#ffffff"])
        self.edit_button.grid(row=0, column=1, padx=(5, 10), pady=5, sticky="e")
    
    def load_image(self, image_name, size):
        script_dir = os.path.dirname(__file__)
        resource_path = os.path.join(script_dir, 'Resources', image_name)
        if os.path.exists(resource_path):
            light_image = Image.open(resource_path)
            dark_image = light_image
            my_image = ctk.CTkImage(light_image=light_image, dark_image=dark_image, size=size)
            return my_image
        return None

    def update_path(self, new_path):
        self.path = new_path
        self.path_label.configure(text=new_path)

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Torrent VPN Installer By Guns.lol/germanized")
        self.geometry("826x526")
        script_dir = os.path.dirname(__file__)
        self.iconbitmap(os.path.join(script_dir, 'Resources', 'vpn_icon.ico'))
        self.configure(fg_color=["#9ea6b0", "#0f0f0f"])
        self.entries_frame = ctk.CTkScrollableFrame(self, width=802, height=400, corner_radius=24, fg_color=["#c6ced8", "#121212"])
        self.entries_frame.pack(pady=10, padx=10, fill="both", expand=True)
        self.add_installed_software_entries()
        self.install_button = ctk.CTkButton(self, text="Install", command=self.install_process, corner_radius=16, 
                                          fg_color=["#697b88", "#11202b"], hover_color=["#525e6b", "#404c59"],
                                          border_color=["#405366", "#405366"], text_color=["#ffffff", "#ffffff"])
        self.install_button.pack(pady=10)

    def add_installed_software_entries(self):
        for software_name, default_path in TORRENT_SOFTWARES.items():
            if os.path.exists(default_path):
                logo_name = f"{software_name.lower().replace(' ', '_')}.png"
                entry = SoftwareEntry(self.entries_frame, logo_name, software_name, default_path, lambda path=default_path: self.edit_path(path))
                entry.pack(pady=5, fill="x", padx=10)

    def edit_path(self, path):
        new_path = filedialog.askopenfilename(initialdir=os.path.dirname(path))
        if new_path:
            for widget in self.entries_frame.winfo_children():
                if isinstance(widget, SoftwareEntry) and widget.path == path:
                    widget.update_path(new_path)
                    break

    def install_process(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        one_drive_desktop_path = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
        if not os.path.exists(desktop_path):
            os.makedirs(desktop_path)
        if not os.path.exists(one_drive_desktop_path):
            os.makedirs(one_drive_desktop_path)
        
        selected_paths = [widget.path for widget in self.entries_frame.winfo_children() if isinstance(widget, SoftwareEntry)]
        for path in selected_paths:
            if os.path.exists(path):
                self.create_batch_file_with_vpn(path, desktop_path)
                self.create_batch_file_with_vpn(path, one_drive_desktop_path)
            else:
                print(f"Software path not found: {path}")

        messagebox.showinfo("Installation Complete", "Batch files have been created on your desktop and OneDrive desktop.")

    def create_batch_file_with_vpn(self, target_path, desktop_path):
        batch_file_path = os.path.join(desktop_path, f"VPN_{os.path.basename(target_path).replace('.exe', '')}.bat")
        vpn_script_path = os.path.join(os.path.dirname(__file__), 'vpn_manager.py')
        icon_path = os.path.join(os.path.dirname(__file__), 'Resources', 'vpn_icon.ico')

        with open(batch_file_path, 'w') as batch_file:
            batch_file.write('@echo off\n')
            batch_file.write(':: Check if the script is running as administrator\n')
            batch_file.write('net session >nul 2>&1\n')
            batch_file.write('if %errorlevel% neq 0 (\n')
            batch_file.write('    echo Requesting administrative privileges...\n')
            batch_file.write('    powershell -Command "Start-Process \'%~f0\' -Verb RunAs"\n')
            batch_file.write('    exit /b\n')
            batch_file.write(')\n\n')
            
            batch_file.write(f'python "{vpn_script_path}" start "{target_path}"\n')
            batch_file.write('pause\n')
            batch_file.write('exit\n')

        self.create_shortcut_with_icon(batch_file_path, icon_path)

        return batch_file_path

    def create_shortcut_with_icon(self, batch_file_path, icon_path):
        shell = win32com.client.Dispatch('WScript.Shell')
        shortcut_path = os.path.splitext(batch_file_path)[0] + ".lnk"
        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.TargetPath = batch_file_path
        shortcut.IconLocation = icon_path
        shortcut.WorkingDirectory = os.path.dirname(batch_file_path)
        shortcut.save()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
