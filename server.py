import socket
import sys
import select
import time


host = ''
port = 5550
buffer_size = 2048
sock_list = []
users = {}
MAX_USERS = 10

def chatserver():


    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host,port))
    server.listen(MAX_USERS)
    server_up = time.asctime()
    sock_list.append(server)
    print "Chat server started on port " + str(port)
    while 1:

        read, write, err = select.select(sock_list,[],[],0)

        for sock in read:

            if sock == server:

                client, addr = sock.accept()
                sock_list.append(client)

                print time.asctime() + " New Client Connected at (%s,%s)"%addr
                sendtoall(server,client,"\r"+"New Client Connected: (%s,%s)"%addr)
                nick = getnick(client)
                sendtoall(server,client,"\r"+"Client (%s,%s) chose nick "%addr + nick)

                print_online_clients(server,client)


            else:
                #one of the clients. Get data and send to the rest
                try:

                    data = sock.recv(buffer_size)

                    if data:
                        if data=="%info":
                            sendinfo(server,sock)
                            continue
                        if data =="%quit":
                            removeclient(sock)
                            continue

                        sendtoall(server,sock,"\r" + "[" + users[sock]["nick"] + "]:" + data)

                    else:
                        #consider as disconnection
                        if sock in sock_list:
                            removeclient(sock)
                except:
                    sendtoall(server,sock,"\r" + "Client " + users[sock]["nick"] + "(%s,%s) is now offline"%addr)
                    continue

    server.close()

def sendtoall(server,sock,data):

    for socket in sock_list:

        if socket!=server and socket!=sock:
            try:
                socket.send(data)
            except:
                socket.close()

                if socket in sock_list:
                    sock_list.remove(socket)

def print_online_clients(server,client):
    online = [users[i]["nick"]+"@"+str(i.getpeername())+" In: "+users[i]["in"] for i in sock_list if i!=server and i!=client]
    if not online:
        online = ["None"]
    client.send("\r"+"User currently online:\n"+"\n".join(online))


def getnick(client):
    nick = client.recv(1024)
    #TODO check for duplicate nicks
    users[client] = {"nick":nick,
                     "in":time.asctime()}
    print users[client]["in"] + ": New Client (%s,%s) chose nick "%client.getpeername() + nick

    return nick


def removeclient(sock):
    sock_list.remove(sock)
    print time.asctime() + ": "+  users[sock]["nick"] + " has disconnected"
    sendtoall(server,sock,"\r" + "Client " + users[sock]["nick"] + "(%s,%s) is now offline"%sock.getpeername())


def sendinfo(server,sock):
    print_online_clients(server,sock)


if __name__=="__main__":

    chatserver()
