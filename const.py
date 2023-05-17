from socket import socket, AF_INET, SOCK_STREAM, gethostbyname, gethostname

HOST = gethostbyname(gethostname())
PORT = 5500
BUFFZISE = 1024
ADDR = (HOST, PORT)
FORMAT = "utf-8"
MAX_CONNECTIONS = 10
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR) # set up server