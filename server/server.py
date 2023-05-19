from socket import socket, AF_INET, SOCK_STREAM, gethostbyname, gethostname
from threading import Thread
import datetime

from client.person import Person

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
    # first message received is always the persons name.
    name = client.recv(BUFFZISE).decode("utf8")
    person.set_name(name)
    welcome_msg = bytes(f"{name} has joined the chat!", 'utf8')
    broadcast(welcome_msg, "") # broadcast welcome message

    while True: # wait fo any messages from person
        try:
            msg = client.recv(BUFFZISE)
            print(f"{name}: ", msg.decode("utf8"))

            if msg == bytes("{quit}", "utf8"): # if message is {quit} disconnect client
                client.send(msg)
                client.close()
                persons.remove(person)
                broadcast(bytes(f"{name} has left the chat...", "utf8"), "")
                print(f"[DISCONNECTED] {name}")
                break

            else: # otherwise send message to all other clients
                broadcast(msg, name+": ")

        except Exception as e:
            print("[EXCEPTION]", e)
            break


def wait_for_connection():
    """
    wait for connection of a new client...
    """

    while True:
        try:
            client, addr = SERVER.accept() # wait for any new connections
            person = Person(client ,addr) # create new person for connection
            persons.append(person)

            time = datetime.datetime.now().time()
            print(f"[CONNECTION] {addr} connected at {time}")
            Thread(target=client_communication, args=(person,)).start()

        except Exception  as e:
            print("[EXCEPTION]", e)
            break

    print("SERVER CRASHED")


if __name__ == '__main__':

    SERVER.listen(MAX_CONNECTIONS) # open server to listen for connections
    print("[STARTED] Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()