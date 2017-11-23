#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : client.py
# Author            : Kaushik S Kalmady
# Date              : 17.11.2017
# Last Modified Date: 17.11.2017
# Last Modified By  : Kaushik S Kalmady
import socket
import sys
import select

buffer_size = 2048


def chatclient():
    # host = socket.gethostname()
    host = 'localhost'
    port = int(raw_input("Enter Port:"))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    global nick
    try:
        s.connect((host, port))
    except:
        sys.stdout.write("Unable to Connect")
        sys.exit()

    sys.stdout.write("Connected successfully\n")
    nick = raw_input("Choose Nick:")
    s.send(nick)

    sys.stdout.write("[" + nick + "]:")
    sys.stdout.flush()
    flag = 1

    while 1:
        sock_list = [0, s]

        read, write, err = select.select(sock_list, [], [])

        for sock in read:
            if sock == 0:

                text = sys.stdin.readline().strip()
                if(text[:7] == "%change"):
                    nick = text.split()[-1]
                if text:
                    s.send(text)

                sys.stdout.write(" "*(len(nick) + 3))
                sys.stdout.flush()

            elif sock == s:

                data = s.recv(buffer_size)
                if not data:
                    sys.stdout.write("\r"+"Disconnected")
                    sys.exit()
                else:
                    sys.stdout.write(data + "\n")
                    sys.stdout.flush()
                    sys.stdout.write("[" + nick + "]:")
                    sys.stdout.flush()


if __name__ == "__main__":
    chatclient()
