from socket import socket, AF_INET, SOCK_STREAM, gethostbyname, gethostname
from threading import Thread
import datetime

from person import Person

# HOST = "192.168.1.34"
HOST = gethostbyname(gethostname())
PORT = 5500
BUFFZISE = 512
ADDR = (HOST, PORT)
FORMAT = "utf-8"
MAX_CONNECTIONS = 10
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR) # set up server

persons = []


def broadcast(msg, name):
    """
    Send messages of all clients
    :params msg: bytes["utf8"]
    :params name: str
    :return:
    """

    for person in persons:
        client = person.client
        client.send(bytes(name, 'utf8') + msg)


def client_communication(person: Person):
    """
    Thread to handle all messages from client
    :params user: User
    :return: None
    """

    client = person.client
    # get users name
    name = client.recv(BUFFZISE).decode("utf8")
    person.set_name(name)
    welcome_msg = bytes(f"{name} has joined the chat!", 'utf8')
    broadcast(welcome_msg, "") # broadcast welcome message

    run = True
    while run:
        try:
            msg = client.recv(BUFFZISE)
            print(f"{name}: ", msg.decode("utf8"))

            if msg == bytes("{quit}", "utf8"):
                client.send(msg)
                client.close()
                persons.remove(person)
                broadcast(bytes(f"{name} has left the chat...", "utf8"), "")
                print(f"[DISCONNECTED] {name}")
                run = False

            else:
                broadcast(msg, name+": ")

        except Exception as e:
            print("[EXCEPTION]", e)
            run = False


def wait_for_connection():
    """
    wait for connection of a new client...
    """

    run = True
    while run:
        try:
            client, addr = SERVER.accept()
            person = Person(client ,addr)
            persons.append(person)
            time = datetime.datetime.now().time()
            print(f"[CONNECTION] {addr} connected at {time}")
            Thread(target=client_communication, args=(person,)).start()

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