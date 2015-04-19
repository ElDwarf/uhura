# -*- coding: utf-8 -*-
from socket import error
from threading import Thread
from client.core import getTerminalSize, print_there


class Recive(Thread):

    def __init__(self, socket, connected, history):
        # Inicializar clase padre.
        Thread.__init__(self)

        self.socket = socket
        self.connected = connected
        self.history = history
        for x in range(getTerminalSize()[1]-1):
            self.history.append(' ')
        print self.history

    def run(self):
        while len(self.connected) == 0:
            try:
                input_data = self.socket.recv(1024)
            except:
                break
            else:
                if input_data:
                    self.history.append(input_data)
                    pos_temp = len(self.history) - getTerminalSize()[1]
                    history_tmp = self.history[pos_temp:]
                    for x in range(getTerminalSize()[1]):
                        for y in range(getTerminalSize()[0]):
                            print_there(x, y, ' ')
                    acumulador = 0
                    for x in history_tmp:
                        print_there(acumulador, 0, x)
                        acumulador += 1


class Envia(Thread):

    def __init__(self, socket, connected, history):
        # Inicializar clase padre.
        Thread.__init__(self)

        self.socket = socket
        self.connected = connected
        self.history = history
        self.promt = '> '

    def run(self):
        print "\n"*80
        while len(self.connected) == 0:
            output_data = raw_input(self.promt)
            if output_data:
                try:
                    #Envia la informacion
                    self.socket.send(output_data)
                except TypeError:
                    #En caso de dar error por caracteres se hace una convercion
                    self.socket.send(bytes(output_data, "utf-8"))
                if output_data[:6] == '\\nick ':
                    self.promt = '[' + output_data[6:] + ']: '
                if output_data == '\quit':
                    print 'Te has desconectado'
                    self.socket.close()
                    break

