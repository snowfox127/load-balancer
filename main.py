import socket
import sys
import select
import random
from itertools import cycle

servers = [('localhost', 8080),('localhost', 8081), ('localhost',8082)]


ITER = cycle(servers)
def RoundRobinLoadBalancer(iter):
    return next(iter)
    
class LoadBalancer(object):
   
    flow_table = dict()
    sockets = list()

    def __init__(self, ip, port, algorithm='random'):
        self.ip = ip
        self.port = port
        self.algorithm = algorithm

        self.cs_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       
        self.cs_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.cs_socket.bind((self.ip, self.port))
        print('init client-side socket: %s' % (self.cs_socket.getsockname(),)) 
        self.cs_socket.listen(10)
        self.sockets.append(self.cs_socket)

    def start(self):
        while True:
            read_list, write_list, exception_list = select.select(self.sockets, [], [])
            for sock in read_list:
                
                if sock == self.cs_socket:
                    print ('='*40+'flow start'+'='*40)
                    self.on_accept()
                    break
                
                else:
                    try:
                    
                        data = sock.recv(4096) 
                        if data:
                            self.on_recv(sock, data)
                        else:
                            self.on_close(sock)
                            break
                    except:
                        sock.on_close(sock)
                        break

    def on_accept(self):
        client_socket, client_addr = self.cs_socket.accept()
        print ('client connected: %s <==> %s' % (client_addr, self.cs_socket.getsockname()))

        
        server_ip, server_port = self.select_server(servers, self.algorithm)
        print(server_ip,server_port)
        
        ss_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            ss_socket.connect((server_ip, server_port))
            print ('init server-side socket: %s' % (ss_socket.getsockname(),))
            print ('server connected: %s <==> %s' % (ss_socket.getsockname(),(socket.gethostbyname(server_ip), server_port)))
        except:
            print ("Can't establish connection with remote server, err: %s" % sys.exc_info()[0])
            print ("Closing connection with client socket %s" % (client_addr,))
            client_socket.close()
            return

        self.sockets.append(client_socket)
        self.sockets.append(ss_socket)

        self.flow_table[client_socket] = ss_socket
        self.flow_table[ss_socket] = client_socket

    def on_recv(self, sock, data):
        print ('recving packets: %-20s ==> %-20s, data: %s' % (sock.getpeername(), sock.getsockname(), [data]))
        
        remote_socket = self.flow_table[sock]
        remote_socket.send(data)
        print ('sending packets: %-20s ==> %-20s, data: %s' % (remote_socket.getsockname(), remote_socket.getpeername(), [data]))

    def on_close(self, sock):
        print ('client %s has disconnected' % (sock.getpeername(),))
        print ('='*41+'flow end'+'='*40)

        ss_socket = self.flow_table[sock]

        self.sockets.remove(sock)
        self.sockets.remove(ss_socket)

        sock.close()  
        ss_socket.close()  

        del self.flow_table[sock]
        del self.flow_table[ss_socket]

    def select_server(self, server_list, algorithm):
        if algorithm == 'random':
            return random.choice(server_list)
        elif algorithm == 'round robin':
            return RoundRobinLoadBalancer(ITER)
        else:
            raise Exception('unknown algorithm: %s' % algorithm)


if __name__ == '__main__':
    try:
        LoadBalancer('localhost', 5555, 'round robin').start()
    except KeyboardInterrupt:
        print ("Ctrl C - Stopping load_balancer")
        sys.exit(1)
