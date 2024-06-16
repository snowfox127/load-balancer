import time
import socket

s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)

host = socket.gethostname() 
port = 3000


s.bind((host, port))


s.listen(5)

while True:
    
    clientSocket, addr = s.accept()
    print("got a connection from %s" % str(addr))
    currentTime = time.ctime(time.time()) + "\r\n"
    clientSocket.send(str(port).encode('ascii'))
    
    clientSocket.close()