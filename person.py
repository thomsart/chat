

class Person:
    """ This class represente each one who connect to the server... """

    def __init__(self, client, addr):
        self.client = client
        self.addr = addr
        self.name = None

    def set_name(self, name):
        self.name= name

    def __repr__(self):
        return f"{self.addr} {self.name}"