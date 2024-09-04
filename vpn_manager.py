import customtkinter as ctk
import os
import subprocess
import sys
import requests
import shutil
import time
from tkinter import messagebox
from PIL import Image
import base64
import winreg

class VPNManager(ctk.CTk):
    def __init__(self, torrent_software_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_path = self.get_vpn_config()
        self.torrent_software_path = torrent_software_path
        self.title("VPN Manager")
        self.geometry("400x200")
        self.configure(fg_color=["#121212", "#121212"])

        script_dir = os.path.dirname(__file__)
        icon_path = os.path.join(script_dir, 'Resources', 'vpn_icon.ico')
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        self.frame = ctk.CTkFrame(self, fg_color=["#121212", "#121212"])
        self.frame.pack(expand=True, fill='both', padx=20, pady=20)

        self.status_label = ctk.CTkLabel(self.frame, text="Starting VPN...", text_color=["#ffffff", "#ffffff"], bg_color="transparent")
        self.status_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.loading_label = ctk.CTkLabel(self.frame, text="", text_color=["#ffffff", "#ffffff"], bg_color="transparent")
        self.loading_label.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.check_openvpn_and_setup()
        self.after(100, self.start_vpn)

    def load_image(self, image_name, size):
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, 'Resources', image_name)
        if os.path.exists(image_path):
            image = Image.open(image_path)
            image = image.resize(size, Image.Resampling.LANCZOS)
            return ctk.CTkImage(light_image=image, dark_image=image, size=size)
        return None

    def get_vpn_config(self):
        url = "https://www.vpngate.net/api/iphone/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            ip = response.text.split('\n')[2].split(',')[1]
            country = response.text.split('\n')[2].split(',')[6]
            decode = base64.b64decode(response.text.split(',,')[1].split('\n')[0])
            filename = f"{country}_{ip}_{int(time.time())}.ovpn"
            config_path = os.path.join(os.path.dirname(__file__), "vpn_configs", filename)
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'wb') as f:
                f.write(decode)
            return config_path
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Network error: {e}")
            sys.exit(1)

    def check_openvpn_and_setup(self):
        openvpn_bin_path = r"C:\Program Files\OpenVPN\bin\openvpn.exe"
        if os.path.exists(openvpn_bin_path):
            self.status_label.configure(text="OpenVPN is already installed.")
            return

        openvpn_dir = os.path.join(os.path.dirname(__file__), "openvpn")
        openvpn_installer_url = "https://swupdate.openvpn.org/community/releases/openvpn-install-2.3.8-I601-x86_64.exe"
        openvpn_installer_path = os.path.join(openvpn_dir, "openvpn_installer.exe")

        if not os.path.exists(openvpn_dir):
            os.makedirs(openvpn_dir)

        if not os.path.exists(openvpn_installer_path):
            try:
                response = requests.get(openvpn_installer_url, stream=True)
                response.raise_for_status()
                with open(openvpn_installer_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                
                messagebox.showinfo("OpenVPN Installer", "OpenVPN is not installed. Please run the installer to complete the installation and configuration.")
                os.startfile(openvpn_installer_path)
                sys.exit(0)  

            except requests.RequestException as e:
                messagebox.showerror("Error", f"Error downloading OpenVPN: {e}")
                sys.exit(1)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Error installing OpenVPN: {e}")
                sys.exit(1)

        if not os.path.exists(openvpn_bin_path):
            messagebox.showerror("Error", "OpenVPN installation failed.")
            sys.exit(1)

        self.configure_openvpn()

    def configure_openvpn(self):
        try:
            config_dir = r"C:\Program Files\OpenVPN\config"
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
            shutil.copy(self.config_path, config_dir)

            reg_file_path = os.path.join(os.path.dirname(__file__), 'openvpn.reg')
            if os.path.exists(reg_file_path):
                subprocess.run(['regedit', '/s', reg_file_path], check=True)

            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\OpenVPNService", 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, "Start", 0, winreg.REG_DWORD, 2)
        except Exception as e:
            messagebox.showerror("Error", f"Error configuring OpenVPN: {e}")
            sys.exit(1)

    def start_vpn(self):
        self.status_label.configure(text="Connecting to VPN...")
        self.update_idletasks()
        self.vpn_process = subprocess.Popen([r"C:\Program Files\OpenVPN\bin\openvpn.exe", "--config", self.config_path], shell=True)
        self.after(2000, self.launch_torrent)

    def launch_torrent(self):
        try:
            self.torrent_process = subprocess.Popen([self.torrent_software_path], shell=True)
            self.torrent_process.wait()
        except Exception as e:
            messagebox.showerror("Error", f"Error launching torrent software: {e}")
        finally:
            self.vpn_process.terminate()
            self.destroy()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: vpn_manager.py start|stop <path_to_torrent_software>")
        input("Press Enter to exit...")
        sys.exit(1)

    action = sys.argv[1]
    torrent_software_path = sys.argv[2]

    if action == "start":
        app = VPNManager(torrent_software_path)
        app.mainloop()
    elif action == "stop":
        pass
    else:
        print("Invalid action. Use 'start' or 'stop'.")
        input("Press Enter to exit...")
