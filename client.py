import socket
import sys


s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)

host = '127.0.0.1'
port = int(sys.argv[1])

s.connect((host, port))

tm = s.recv(1024) 

#s.close()
print("Request from port %s" % tm.decode('ascii'))