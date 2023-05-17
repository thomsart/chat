from threading import Thread

from const  import *

client = socket(AF_INET, SOCK_STREAM)
client.connect(ADDR)

messages = []

def receive_message():
    """
    receive mesage from user
    :return: msg
    """

    while True:
        try:
            msg = client.recv(BUFFZISE).decode()
            messages.append(msg)
            print(msg)
        except Exception as e:
            print("[EXCEPTION]", e)
            break

def send_message(msg):
    """
    send mesage from user
    :return: msg
    """

    client.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client.close()


start = True
while start:
    msg = input()
    if msg == "q":
        send(DISCONNECT_MESSAGE)
    send(msg)

# cd Bureau/Documents/projets/chat