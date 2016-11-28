import socket
import sys
import select

buffer_size = 2048

def chatclient():

    host = socket.gethostname()
    port = int(raw_input("Enter Port:"))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try:
        s.connect((host,port))
    except:
        print "Unable to Connect"
        sys.exit()

    print "Connected successfully"
    nick = raw_input("Choose Nick:")
    s.send(nick)
    
    print "["+nick+"]: ",;sys.stdout.flush()



    while 1:

        sock_list = [sys.stdin,s]

        read,write,err = select.select(sock_list,[],[])

        for sock in read:

            if sock == s:

                data = s.recv(buffer_size)
                if not data:
                    print "\r"+"Disconnected"
                    sys.exit()

                print data
                print "["+nick+"]: ",;sys.stdout.flush()

            else:

                text = raw_input()
                s.send(text)
                print "\b["+nick+"]: ",;sys.stdout.flush()


if __name__=="__main__":
    chatclient()
