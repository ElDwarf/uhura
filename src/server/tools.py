# -*- coding: utf-8 -*-
from socket import error
from threading import Thread
from server.setting import *
from datetime import datetime


class Client(Thread):

    HELP_SERVER = {
        '\quit': 'Desconecta del servidor',
        '\user_list': 'Devuelve el listado de usuarios',
        '\\nick <nick_name>': 'Setea el <nick_name> del usuario',
        '\say <nick_name> <mensaje>': 'Envia mensaje privado'
    }

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
                if input_data:
                    self.process_message(input_data)
                    if input_data == EXIT_OPTION:
                        break
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

    def set_nick(self, nick):
        count_temp = 0
        for x in self.client:
            if nick == self.client[x]['nick']:
                count_temp += 1
        if count_temp == 0:
            old_nick = self.client[self.addr[1]]['nick']
            self.client[self.addr[1]]['nick'] = nick
            msg_temp = bcolors.OKBLUE
            msg_temp += old_nick + ' ahora es '
            msg_temp += nick
            msg_temp += bcolors.ENDC
            self.history.append(
                msg_temp
            )
            for x in self.client.keys():
                self.client[x]['client'].send_message(msg_temp)
        else:
            msg_temp = 'ERROR: El nick ta esta en uso.'
            for x in self.client.keys():
                self.client[self.addr[1]]['client'].send_message(msg_temp)

    def send_help(self):
        tmp_msg = '-' * 30
        tmp_msg += '\nHelp del Server UHURA\n'
        for x in self.HELP_SERVER:
            tmp_msg += x + ':\n'
            tmp_msg += '\t' + self.HELP_SERVER[x] + '\n'
        tmp_msg += '-' * 30
        self.send_message(tmp_msg)

    def say_to(self, user, message):
        hours = datetime.now().hour
        if hours < 10:
            hours = '0' + str(hours)
        else:
            hours = str(hours)
        minute = str(datetime.now().minute)
        if minute < 10:
            minute = '0' + str(minute)
        else:
            minute = str(minute)
        msg_temp = hours
        msg_temp += ':'
        msg_temp += minute
        msg_temp += bcolors.HEADER
        msg_temp += ' <'
        msg_temp_1 += str(self.client[self.addr[1]]['nick']) + "> "
        msg_temp_1 += bcolors.ENDC
        message_1 = msg_temp_1 + message
        for x in self.client:
            if self.client[x]['nick'] == user:
                self.client[x]['client'].send_message(message_1)
        msg_temp += str(self.client[self.addr[1]]['nick'])
        msg_temp += "--> "
        msg_temp += user
        msg_temp += " > "
        msg_temp += bcolors.ENDC
        message = msg_temp + message
        self.client[self.addr[1]]['client'].send_message(message)

    def process_message(self, input_data):
        hours = datetime.now().hour
        if hours < 10:
            hours = '0' + str(hours)
        else:
            hours = str(hours)
        minute = str(datetime.now().minute)
        if minute < 10:
            minute = '0' + str(minute)
        else:
            minute = str(minute)
        msg_temp = hours
        msg_temp += ':'
        msg_temp += minute
        msg_temp += ' <'
        msg_temp += str(self.client[self.addr[1]]['nick']) + "> "
        msg_temp += input_data
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
        elif input_data[:6] == '\\nick ':
            self.set_nick(input_data[6:])
        elif input_data == '\user_list':
            user_list = '['
            for x in self.client.keys():
                user_list += self.client[x]['nick'] + ', '
            user_list += ']'
            self.client[self.addr[1]]['client'].send_message(user_list)
        elif input_data[:5] == '\say ':
            msg_temp = input_data[5:]
            user_temp = msg_temp[:msg_temp.index(' ')]
            msg_temp = msg_temp[msg_temp.index(' ')+1:]
            self.say_to(user_temp, msg_temp)
        elif input_data == '\help':
            self.send_help()
        else:
            self.history.append(msg_temp)
            self.history.printer()
            for x in self.client.keys():
                self.client[x]['client'].send_message(msg_temp)
