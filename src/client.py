# -*- coding: utf-8 -*-
from socket import error
from server.setting import *
from socket import socket
from client.tools import Recive, Envia

HOST = '201.235.199.203'
#HOST = 'localhost'
PORT = 6031

connected = []
history = []


def main():
    #Crea objeto socket
    s = socket()
    s.connect((HOST, PORT))
    print "\n"*80
    r = Recive(s, connected, history)
    e = Envia(s, connected, history)
    r.start()
    e.start()


if __name__ == "__main__":
    main()
