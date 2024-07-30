from main import RoundRobinLoadBalancer
import time
import socket
import sys

def test_server():
        servers = ["server1","server2","server3"] 
        serverlist=[]
        
        load_balancer = RoundRobinLoadBalancer(servers)
    
        for i in range(10):
            server = load_balancer.next_server()
            serverlist.append(server)
            
            print(f"Request {i+1} routed to {server}")
       
        assert serverlist== ['server1','server2','server3','server1','server2','server3','server1','server2','server3','server1']
        
def serverTest():
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
        
serverTest()