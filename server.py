import networking as net

HOST: str = input("IP (127.0.0.1): ")
PORT: str = input("Port (8080): ")
MAX_CONNECTIONS = 8

# server = net.Server()
# server.init_socket(HOST, PORT, MAX_CONNECTIONS)
# server.start_listening()

server = net.Server()
if not server.init_socket(HOST, PORT, MAX_CONNECTIONS):
    input("Press Enter to exit.")
else:
    server.start_listening()
