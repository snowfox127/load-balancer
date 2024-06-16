import socket


s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)

host = socket.gethostname() 
port = 3000

s.connect((host, port))

tm = s.recv(1024) 

s.close()
print("Request from port %s" % tm.decode('ascii'))