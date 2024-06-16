from main import RoundRobinLoadBalancer

def test_server():
        servers = ["server1","server2","server3"] 
        serverlist=[]
        
        load_balancer = RoundRobinLoadBalancer(servers)
    
        for i in range(10):
            server = load_balancer.next_server()
            serverlist.append(server)
            
            print(f"Request {i+1} routed to {server}")
       
        assert serverlist== ['server1','server2','server3','server1','server2','server3','server1','server2','server3','server1']
        
test_server()