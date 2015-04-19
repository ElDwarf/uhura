# -*- coding: utf-8 -*-
from socket import error
from threading import Thread
from server.setting import *
from datetime import datetime


class Client(Thread):

    def __init__(self, conn, addr, client, history):
        # Inicializar clase padre.
        Thread.__init__(self)

        self.conn = conn
        self.addr = addr
        self.client = client
        self.history = history

    def run(self):
        input_data = ''
        self.conn.send(MSG_WELCOME_CLIENTE)
        while True:
            try:
                input_data = self.conn.recv(1024)
                msg_temp = str(datetime.now().hour)
                msg_temp += ':'
                msg_temp += str(datetime.now().minute)
                msg_temp += ' <'
                msg_temp += str(self.client[self.addr[1]]['nick']) + "> "
                msg_temp += input_data
                if input_data:
                    if input_data == EXIT_OPTION:
                        for x in self.client.keys():
                            msg_temp = bcolors.FAIL
                            msg_temp += self.client[self.addr[1]]['nick']
                            msg_temp += " se a desconectado."
                            msg_temp += bcolors.ENDC
                            self.client[x]['client'].send_message(msg_temp)
                        self.conn.close()
                        self.history.append(
                            msg_temp
                        )
                        del self.client[self.addr[1]]
                        msg_temp = bcolors.WARNING
                        msg_temp += "--%s " % str(len(self.client))
                        msg_temp += " cliente conectados"
                        msg_temp += bcolors.ENDC
                        self.history.append(
                            msg_temp
                        )
                        self.history.printer()
                        break
                    elif input_data[:6] == '\\nick ':
                        old_nick = self.client[self.addr[1]]['nick']
                        self.client[self.addr[1]]['nick'] = input_data[6:]
                        msg_temp = bcolors.OKBLUE
                        msg_temp += old_nick + ' ahora es '
                        msg_temp += input_data[6:]
                        msg_temp += bcolors.ENDC
                        self.history.append(
                            msg_temp
                        )
                        for x in self.client.keys():
                            self.client[x]['client'].send_message(msg_temp)
                    else:
                        self.history.append(msg_temp)
                        self.history.printer()
                        for x in self.client.keys():
                            self.client[x]['client'].send_message(msg_temp)
            except error:
                self.history.append("[%s] Error de lectura." % self.name)
                break
        self.conn.close()

    def close(self):
        """Método para cerrar el socket."""
        self.conn.close()

    def send_message(self, message):
        self.conn.send(
            message
        )
