import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# SERVER = "192.168.1.34"
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

start = True
while start:
    msg = input()
    if msg == "q":
        send(DISCONNECT_MESSAGE)
    send(msg)

# cd Bureau/Documents/projets/chat