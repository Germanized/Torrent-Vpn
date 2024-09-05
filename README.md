# Torrent VPN Installer and VPN Manager

## Overview

This project includes two scripts: one for creating batch files to run a VPN before starting various torrent software, and another for managing the VPN connection. The goal is to ensure your torrenting activities are protected by a VPN.

## Scripts

### `installer.py`

This script creates batch files that run a VPN script before starting selected torrent software. It generates shortcuts with these batch files on your desktop and OneDrive desktop.

#### Features
- Detects installed torrent software.
- Creates batch files with administrative privileges to run a VPN script.
- Creates shortcuts with custom icons.

#### Usage
1. Run the `installer.py` script.
2. The application will display a list of detected torrent software.
3. Edit paths if necessary and click "Install" to create batch files and shortcuts.

### `vpn_manager.py`

This script handles VPN management, including downloading and installing OpenVPN, configuring it, and starting the VPN connection before launching the torrent software.

#### Features
- Downloads and installs OpenVPN if not already installed.
- Configures OpenVPN with a VPN configuration file.
- Starts the VPN and launches the torrent software.

#### Usage
1. Run the shortcut it generates
2. it should install openvpn and configure it if you havent already
3. then close the shortcut thing then reopen the shortcut
4. them boom it works

## Requirements

- Python 3.x
- `customtkinter` library
- `PIL` library
- `requests` library
- `win32com.client` and `winreg` for Windows-specific operations

Install the required Python libraries using pip:
pip install customtkinter pillow requests pywin32

## Video Tutorial

For a detailed tutorial on how to use these scripts, watch the video below:

[![Video Tutorial](https://drive.google.com/file/d/14I2raZphxH6ge36CaAzoK0Uvm8bUgKzY/view?usp=sharing)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Feel free to contribute to this project by opening issues or pull requests.

## Contact

For any questions, you can reach out to [Your Name](mailto:darthsaint008@gmail.com).
or my discord @pronhubstar
