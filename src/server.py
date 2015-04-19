# -*- coding: utf-8 -*-
from socket import socket
from server.setting import *
from server.tools import Client
from server.core import history as _history

clientes = {}
history = _history()


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
                msg_temp = bcolors.WARNING
                msg_temp += "--%s cliente conectados" % str(len(clientes) + 1)
                msg_temp += bcolors.ENDC
                history.append(msg_temp)
                history.printer()
                c = Client(conn, addr, clientes, history)
                c.start()
                clientes[addr[1]] = {
                    'nick': 'guess-%s' % addr[1],
                    'client': c
                }
                for x in clientes.keys():
                    if x != addr[1]:
                        msg_temp = bcolors.OKGREEN
                        msg_temp += clientes[x]['nick'] + " se ha conectado."
                        msg_temp += bcolors.ENDC
                        clientes[x]['client'].send_message(msg_temp)
                history.append(msg_temp)
                history.printer()
            else:
                conn, addr = s.accept()
                MSG_DENEGACION = "%s:%d Conexion rechazado." % addr
                print MSG_DENEGACION
                conn.send(MSG_DENEGADO_CLIENTE)
                conn.close()
        except KeyboardInterrupt:
            for cli in clientes.keys():
                clientes[cli]['client'].close()
            break
if __name__ == "__main__":
    main()
