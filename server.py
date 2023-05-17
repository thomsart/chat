from threading import Thread
import datetime

from const import *
from user import User


users = []

def broadcast(msg, name):
    """
    Send messages to all clients
    :params msg: bytes["utf8"]
    :params name: str
    :return:
    """
    for user in users:
        client = user.client
        client.send(bytes(name + ": ", 'utf8') + msg)

def client_communication(user):
    """
    Thread to handle all messages from client
    :params user: User
    :return: None
    """

    client = user.client
    addr = user.addr

    # get users name
    name = client.recv(BUFFZISE).decode("utf8")
    msg = f"{name} has joined the chat!"
    broadcast(msg) # broadcast welcome message

    while True:
        try:
            msg = client.recv(BUFFZISE)
            print(f"{name}: ", msg.decode("utf8"))
            if msg == bytes("{quit}", "utf8"):
                broadcast(f"{name} has left the chat..." , name)
                client.send(bytes("{quit}", "utf8"))
                client.close()
                users.remove(user)
                break
            else:
                client.send(msg, name)

        except Exception as e:
            print("[EXCEPTION]", e)
            break

def wait_for_connection():
    """
    wait for connection of a new client...
    """
    run = True
    while run:
        try:
            client, addr = SERVER.accept()
            user = User(addr, client)
            users.append(user)
            print(f"[CONNECTION] {addr} connected ti the server at {datetime.datetime.now()}")
            Thread(target=client_communication, args=(client,)).start()
        except Exception  as e:
            print("[EXCEPTION]", e)
            run = False
    print("SERVER CRASHED")


if __name__ == '__main__':

    SERVER.listen(MAX_CONNECTIONS)
    print("[STARTED] Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()