# -*- coding: utf-8 -*-
from socket import error
from threading import Thread
from server.setting import *


class Client(Thread):
    """
    Servidor eco - reenvía todo lo recibido.
    """

    def __init__(self, conn, addr, client):
        # Inicializar clase padre.
        Thread.__init__(self)

        self.conn = conn
        self.addr = addr
        self.client = client
        self.input_data = ''

    def run(self):
        self.input_data = ''
        self.conn.send(MSG_WELCOME_CLIENTE)
        while True:
            try:
                self.input_data = self.conn.recv(1024)
            except error:
                print "[%s] Error de lectura." % self.name
                break
            else:
                if self.input_data:
                    if self.input_data == EXIT_OPTION:
                        self.conn.close()
                        print self.addr[0] + " se a desconectado."
                        self.client.remove(self)
                        print "--%s cliente conectados" % str(len(self.client))
                        break
                    else:
                        for x in self.client:
                            x.send_message(self.input_data)
        self.conn.close()

    def close(self):
        """Método para cerrar el socket."""
        self.conn.close()

    def send_message(self, message):
        msg_temp = str(self.addr[0]) + "[" + str(self.addr[1]) + "]: "
        msg_temp += message
        self.conn.send(
            msg_temp
        )
        print msg_temp
