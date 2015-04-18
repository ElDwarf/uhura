# -*- coding: utf-8 -*-
from socket import socket
from server.setting import *
from server.tools import Client

clientes = []


def main():
    s = socket()
    print CLEAR_SCREEN
    print SEPARADOR
    print MSG_WELCOME_SERVER
    print SEPARADOR
    print MSG_EXPLICACION
    s.bind((HOST_SERVER, POST_SERVER))
    s.listen(0)
    while True:
        try:
            if len(clientes) < LIMIT_CONEXTION:
                conn, addr = s.accept()
                print "--%s cliente conectados" % str(len(clientes) + 1)
                print "%s:%d se a conectado." % addr
                c = Client(conn, addr, clientes)
                c.start()
                clientes.append(c)
                print "%s:%d se ha conectado." % addr
            else:
                conn, addr = s.accept()
                MSG_DENEGACION = "%s:%d Conexion rechazado." % addr
                print MSG_DENEGACION
                conn.send(MSG_DENEGADO_CLIENTE)
                conn.close()
        except KeyboardInterrupt:
            for cli in clientes:
                cli.close()
            break

if __name__ == "__main__":
    main()
