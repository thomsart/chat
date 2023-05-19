from socket import socket, AF_INET, SOCK_STREAM, gethostbyname, gethostname
from threading import Thread, Lock
import time



# # HOST = "192.168.1.34"
# HOST = gethostbyname(gethostname())
# PORT = 5500
# BUFFZISE = 512
# ADDR = (HOST, PORT)

# client_socket = socket(AF_INET, SOCK_STREAM)
# client_socket.connect(ADDR) # set up server

# messages = []



# def receive_messages():
#     """
#     receive message from user
#     :return: msg
#     """

#     while True:
#         try:
#             msg = client_socket.recv(BUFFZISE).decode()
#             messages.append(msg)
#             print(msg)
#         except Exception as e:
#             print("[EXCEPTION]", e)
#             break


# def send_message(msg):
#     """
#     send mesage to the server
#     :params msg: str
#     :return: None
#     """

#     client_socket.send(bytes(msg, "utf8"))
#     if msg == "{quit}":
#         client_socket.close()


# receive_thread = Thread(target=receive_message)
# receive_thread.start()

# send_message('Pierre')
# time.sleep(1)
# send_message("Hello world!")
# time.sleep(1)
# send_message("Salut les gars!")
# time.sleep(1)
# send_message("Qui ici connait les dents de la mere ?")
# time.sleep(1)
# send_message("Bon ok je vois... Merci les gars.")
# time.sleep(1)
# send_message("{quit}")




class Client():
    """
    This class will use to communictae with the server

    """

    def __init__(self, name):
        """
        Init a Client and send the name to the server.
        :params name: str
        :return: Client
        """
        self.host = gethostbyname(gethostname())
        self.port = 5500
        self.buffsize = 512
        self.addr = (self.host, self.port)
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.addr)
        self.messages = []
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()
        self.send_message(name)
        self.lock = Lock()


    def receive_messages(self):
        """
        receive messages from server
        :return: msg
        """

        while True:
            try:
                msg = self.client_socket.recv(self.buffsize).decode()
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
                print(msg)
            except Exception as e:
                print("[EXCEPTION]", e)
                break


    def send_message(self, msg):
        """
        send mesage to the server
        :params msg: str
        :return: None
        """

        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.client_socket.close()
        time.sleep(0.5)


    def get_messages(self):
        """
        :retruns a list of str messages:
        :return: list[str]
        """
        self.lock.acquire()



new_client = Client('Thomas')
new_client.send_message("bougouuuuuur tout le monde, c'est Mickeline...")
new_client.send_message("{quit}")