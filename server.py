#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : server.py
# Author            : Kaushik S Kalmady
# Date              : 17.11.2017
# Last Modified Date: 18.11.2017
# Last Modified By  : Kaushik S Kalmady
import socket
import sys
import select
import time


host = 'localhost'
port = 5550
buffer_size = 2048
sock_list = []
users = {}
MAX_USERS = 10

def chatserver():
    """Summary
    """
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host,port))
    server.listen(MAX_USERS)
    server_up = time.strftime("%d/%h/%Y %H:%M:%S")
    sock_list.append(server)
    print "Chat server started on port %s"%str(port)
    while 1:

        read, write, err = select.select(sock_list,[],[],0)

        for sock in read:

            if sock == server:

                client, addr = sock.accept()
                sock_list.append(client)

                print "["+time.strftime("%d/%h/%Y %H:%M:%S") + "] New Client Connected at (%s,%s)"%addr
                sendtoall(server,client,"\r"+"New Client Connected: (%s,%s) "%addr)
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
                        if data[:7] == "%change":
                            newnick = data.split()[-1]
                            changenick(sock,newnick)


                            sendtoall(server,sock,"\r"+"Client (%s,%s) changed nick to "%addr + newnick)

                            continue

                        sendtoall(server,sock,"\n" + "[" + users[sock]["nick"] + "]:" + data)

                    else:
                        #consider as disconnection
                        if sock in sock_list:
                            removeclient(sock)
                except:
                    sendtoall(server,sock,"\r" + "Client " + users[sock]["nick"] + "(%s,%s) is now offline"%addr)
                    continue

    server.close()

def sendtoall(server,sock,data):
    """Summary

    Args:
        server (TYPE): Description
        sock (TYPE): Description
        data (TYPE): Description
    """
    for socket in sock_list:

        if socket!=server and socket!=sock:
            try:
                socket.send(data)
            except:
                socket.close()

                if socket in sock_list:
                    sock_list.remove(socket)

def print_online_clients(server,client):
    """Summary

    Args:
        server (TYPE): Description
        client (TYPE): Description
    """
    online = [users[i]["nick"]+"@"+str(i.getpeername())+" In: "+users[i]["in"] + "\n" for i in sock_list if i!=server and i!=client]
    if not online:
        online = ["None"]
    client.send("\r"+"Users currently online:\n"+"\n".join(online))


def getnick(client):
    """Summary

    Args:
        client (TYPE): Description

    Returns:
        TYPE: Description
    """
    nick = client.recv(1024)
    #TODO check for duplicate nicks
    users[client] = {"nick":nick,
                     "in":time.strftime("%d/%h/%Y %H:%M:%S")}
    print users[client]["in"] + ": New Client (%s,%s) chose nick "%client.getpeername() + nick

    return nick


def removeclient(sock):
    """Summary

    Args:
        sock (TYPE): Description
    """
    sock_list.remove(sock)
    print time.strftime("%d/%h/%Y %H:%M:%S") + ": "+  users[sock]["nick"] + " has disconnected"
    sendtoall(server,sock,"\r" + "Client " + users[sock]["nick"] + "(%s,%s) is now offline"%sock.getpeername())


def sendinfo(server,sock):
    """Summary

    Args:
        server (TYPE): Description
        sock (TYPE): Description
    """
    print_online_clients(server,sock)


def changenick(client,newnick):
    """Summary

    Args:
        client (TYPE): Description
        newnick (TYPE): Description
    """
    users[client]["nick"] = newnick



if __name__=="__main__":

    chatserver()
