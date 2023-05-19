from threading import Thread
from client.client import Client
import time


c1 = Client("George")
c2 = Client("John")

def update_messages():
    """
    Updates the local list of messages 
    :return: None
    """

    msgs = []
    run = True
    while run:
        time.sleep(0.1) # update every 1/10 of a second
        new_messages = c1.get_messages() # get any new messages from client
        msgs.extend(new_messages) # add to local list of messages

        for msg in new_messages: # display new messages
            print(msg)

            if msg == "{quit}":
                run = False
                break

Thread(target=update_messages).start()

c1.send_message('Hello')
c2.send_message('Hi, Whats up ?')
c1.send_message("Ho nothing much, and you ?")
c2.send_message("Ok, ho the same bro...")

c1.disconnect()
c2.disconnect()