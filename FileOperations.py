import sys

sys.path.append(r"C:\Users\Harshit\PycharmProjects\ImageCryptography")
from header import *

class FileOperations:


    def __init__(self):

        self.imageName = ""

    def OpenImage(self, root, path):
        # Selecting Image
        root.imageName = askopenfilename(initialdir=path)

        # Checking if any Image was selected
        if root.imageName != "":
            self.imageName = root.imageName
        else:
             root.imageName = self.imageName

        # Opening Image
        originalImage = Image.open(root.imageName)
        # Calculating Dimensions of the Image
        width, height = originalImage.size

        # Checking Dimensions of the Image
        if(width > 840):
            width = 840

        if(height > 500):
            height = 500

        # Setting the Dimensions of the Image
        resizedImage = originalImage.resize((width, height), Image.ANTIALIAS)

        # Opening Image in GUI
        root.imageName = ImageTk.PhotoImage(resizedImage)

        # Setting Labels for the Image
        label = Label(root, image=root.imageName)
        label.place(relx=0.5, rely=0.55, anchor="center")

        path = "C:/Users/Harshit/Desktop/SendFiles/"
        #self.SaveFile(path)

    # Function to Save File
    def SaveFile(self, path):
        # Opening Source File
        with open(self.imageName, "rb") as fpSrc:
            data = fpSrc.read()
            fpSrc.close()

        # Setting Destination for File
        destFile = path + (self.imageName.split('/')[-1])
        # Opening Destination File
        with open(destFile, "wb") as fpDest:
            fpDest.write(data)
            fpDest.close()

    # Function to Send File
    def SendFile(self, Conn):

        # Check if Image was Loaded
        if self.imageName == "":
            msg = "\nNo Image has been Loaded!\nLoad any Image First!\n"

            return msg

        # Check Connection Status
        if Conn.connStatus == "FALSE":
            msg = "\nDisconnected!\nEstablish Connection First!\n"

            return msg

        # Extracting Image Size
        imageSize = os.path.getsize(self.imageName)

        # Extracting Image Name
        self.imagename = self.imageName.split('/')[-1]

        # Concatinating Image Name with its Size
        imageData = str(imageSize) + "~" + self.imagename

        """msg = "\nSending Image!\nPlease Wait!\n"
        alert_window(msg)"""

        ack = 0
        i = 1
        while i <= 3:
            i = i + 1

            # Sending Image Meta-Data
            Conn.Socket.send((str(imageData)).encode('utf8'))

            # Get File Name to Send
            fileName = self.imageName

            # Opening File and Setting File Pointer
            with open(fileName, "rb") as fp:

                # Sending File
                Conn.Socket.sendall(fp.read())

                # Receiving Acknowledgement
                ack = Conn.Socket.recv(1024)

                # ack = ack.split("'")[-1]
                ack = str(ack)

                #if ack == "b'1'":
                    # Closing File
                fp.close()

                path = "C:/Users/Harshit/Desktop/SendFiles/"
                    #self.SaveFile(path)

                msg = "\nCongratulations!\nFile was successfully Send!\n"
                return msg

        # Checking Acknowledgement Status
        if ack == "b'0'":
            msg = "\nSorry!\nFile Could Not be Send!\nCheck Your Connection Status!\n"

            return msg

    # Function To Receive File
    def ReceiveFile(self, Conn):

        # Check Connection Status
        if Conn.conn == 0:
            msg = "\nDisconnected!\nEstablish Connection First!\n"
            return msg

        i = 1
        while True:
            i = i + 1

            # Receive File Meta-Data
            data = Conn.conn.recv(2048)

            # Separate File Size and File Name
            imageSize = str(data).split('~')[0]
            imageName = str(data).split('~')[1]

            # Checking Environment for further Splitting
            if (platform.system() != 'Linux'):
                image_size = imageSize.split("'")[1]

            # Retrieving File Size
            imageSize = int(imageSize)

            # Opening File
            fp = open(imageName, "wb")

            tempImageSize = 0
            while True:
                # Getting File Data Bytes
                data = Conn.conn.recv(4096)
                # Calculating File Data Received
                tempImageSize += len(data)

                # Checking if File Fully Received
                if (tempImageSize - imageSize == 0):
                    ack = 1
                    ack = str(ack)
                    Conn.conn.send(ack.encode("utf8"))

                    msg = "\nCongratulations!\nFile was successfully Received!\n"

                    path = ""
                    #self.SaveFile(path)

                    break

                # Write Data Bytes On File
                fp.write(data)

            # Closing File
            fp.close()

        if ((tempImageSize - imageSize != 0) and ( i >= 3)):
            msg = "\nSorry!\nFile was not Received Completely!\n"


        return msg