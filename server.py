import socket
import sys
import select


host = ''
port = 5550
buffer_size = 2048
sock_list = []

def chatserver():


    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host,port))
    server.listen(10)

    sock_list.append(server)
    print "Chat server started on port " + str(port)
    while 1:

        read, write, err = select.select(sock_list,[],[],0)

        for sock in read:

            if sock == server:

                client, addr = sock.accept()
                sock_list.append(client)

                sendtoall(server,client,"\r"+"Client Connected: (%s,%s)"%addr)
                #TODO ask for nick
                nick = client.recv(1024)
                print nick
                sendtoall(server,client,"\r"+"Client (%s,%s) chose nick "%addr + nick)

            else:
                #one of the clients. Get data and send to the rest
                try:

                    data = sock.recv(buffer_size)

                    if data:
                        sendtoall(server,sock,"\r"+str(sock.getpeername())+":"+data)

                    else:
                        #consider as disconnection
                        if sock in sock_list:
                            sock_list.remove(sock)
                            sendtoall(server,sock,"\r"+"Client (%s,%s) offline"%addr)
                except:
                    sendtoall(server,sock,"\r"+"Client (%s,%s) offline"%addr)
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


if __name__=="__main__":

    chatserver()
