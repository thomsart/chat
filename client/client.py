from socket import socket, AF_INET, SOCK_STREAM, gethostbyname, gethostname
from threading import Thread, Lock
import time



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


    def wait(self):
        return time.sleep(0.5)


    def receive_messages(self):
        """
        receive messages from server
        :return: msg
        """

        while True:
            try:
                msg = self.client_socket.recv(self.buffsize).decode()
                # make sure memory is safe to access
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
                print(msg)
            except Exception as e:
                print("[EXCEPTION]", e)
                break


    def send_message(self, msg):
        """
        Send message to the server
        :params msg: str
        :return: None
        """

        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.client_socket.close()
        self.wait()


    def get_messages(self):
        """
        Retruns a list of str messages.
        :return: list[str]
        """

        # make sure memory is safe to access
        messages_copy = self.messages[:]
        self.lock.acquire()
        self.messages = []
        self.lock.release()

        return messages_copy


    def disconnect(self):
        """
        Disconect from the server
        """

        self.send_message("{quit}")
        self.wait()