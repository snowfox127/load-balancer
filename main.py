class RoundRobinLoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.current_index = 0

    def next_server(self):
        if not self.servers:
            return None
        server = self.servers[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.servers)
        return server

# Example Usage:
if __name__ == "__main__":
    servers = ["server1","server2","server3"]  
    load_balancer = RoundRobinLoadBalancer(servers)
    
    # Simulate requests
    for i in range(10):
        server = load_balancer.next_server()
        print(f"Request {i+1} routed to {server}")