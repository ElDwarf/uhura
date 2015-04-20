# -*- coding: utf-8 -*-
from server.core import getTerminalSize

POSTITION = getTerminalSize()

HOST_SERVER = 'localhost'

POST_SERVER = 6031

SEPARADOR = "=" * POSTITION[1]

CLEAR_SCREEN = "\n" * 50

MSG_WELCOME_SERVER = "Bienvenidos al Server"

MSG_EXPLICACION = "Eschucando conexiones presione CRT-C para cerrar el proceso."

MSG_WELCOME_CLIENTE = "Bienvenido al server: Curso Python"

MSG_DENEGADO_CLIENTE = "El server se encuentra completo"

EXIT_OPTION = '\quit'

LIMIT_CONEXTION = 10


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
