import sys

sys.path.append(r"C:\Users\Harshit\PycharmProjects\ImageCryptography")
from header import *


class Connection:
    Socket = 0
    conn = 0
    connStatus = "FALSE"
    hostIP = ""
    portNumber = 9999

    # Default Constructor
    def __init__(self):

        # Creating SOCKET Object
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Function to Establish Connection
    def EstablishConnection(self, hostIP):

        self.hostIP = hostIP

        # Connecting To IP
        try:
            self.Socket.connect((self.hostIP, self.portNumber))

            self.connStatus = "TRUE"
            msg = "\nCongratulations!\nConnection Successfully Established With The Server!\n"

        except Exception as excep:
            msg = "\nSorry!\nError Establishing Connection!\n"
            print(excep)

        return msg

    # Function to Wait For Client
    def WaitForConnection(self):

        self.Socket.bind((self.hostIP, self.portNumber))
        self.Socket.listen(5)

        try:
            conn, addr = self.Socket.accept()
            msg = "\nCongratulations!\nConnection Established Successfully!\nClient Address ",addr

        except Exception as excep:
            msg = "\nSorry!\nError Connecting With Client!\n"

        return msg

    # Function to Terminate Established Connection
    def CloseConnection(self):

        # Checking Connection Status
        if self.connStatus == "TRUE":
            self.Socket.close()

            self.connStatus = "FALSE"
            msg = "\nServer Disconnected!\n"

        else:
            msg = "\nNo Connection Found!\n"

        return msg