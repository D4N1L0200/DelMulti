import networking as net

HOST: str = input("IP: ")
PORT: int = 8080
MAX_CONNECTIONS = 8

server = net.Server()
server.init_socket(HOST, PORT, MAX_CONNECTIONS)
server.start_listening()
