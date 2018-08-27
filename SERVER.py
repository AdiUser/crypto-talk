#Working code for receiving image
import socket
import sys
import platform

HOST = ""
PORT = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

print("Listening ...")

conn, addr = s.accept()
print("[+] Client connected: ", addr)

while True:
    
    data = conn.recv(2048)
    
    image_size = str(data).split('~')[0]
    image_name = str(data).split('~')[1]
    
    if (platform.system() != 'Linux'):
        image_size = image_size.split("'")[1]
    
    image_size = int(image_size)
    
    # get file name to download
    f = open("abc.png", "wb")

    sm = 0
    while True:
        # get file bytes
        data = conn.recv(4096)
        sm += len(data)
        print(sm)
        if(sm - image_size == 0):

            ack = 1
            ack = str(ack)
            conn.send(ack.encode("utf8"))
    
            break


        # write bytes on file
        f.write(data)
    f.close()
    print("[+] Download complete!")

    # close connection
    #conn.close()
    #print("[-] Client disconnected")
    #sys.exit(0)
