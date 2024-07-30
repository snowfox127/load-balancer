import time
import socket
import sys

s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)

host = socket.gethostname() 
port = int(sys.argv[1])


s.bind((host, port))

s.listen(5)

while True:
    
    clientSocket, addr = s.accept()
    print("received a message from port %s" % str(addr))
    currentTime = time.ctime(time.time()) + "\r\n"
    clientSocket.send(str(port).encode('ascii'))
    
    clientSocket.close()