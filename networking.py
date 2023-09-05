import socket
import threading


class Server:
    def __init__(self) -> None:
        self.hostname: str = "127.0.0.1"
        self.port: int = 8080
        self.max_connections: int = 2
        self.socket: socket = None
        self.clients: dict = {}
        print("Server initializing...")

    def init_socket(self, hostname: str, port: int, max_connections: int = 2) -> None:
        if hostname:
            self.hostname = hostname
        if port:
            self.port = port
        self.max_connections = max_connections
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        print(f"Server socket bound on {self.hostname}:{self.port}")

    def handle_client(self, client_socket: socket, current_client: int) -> None:
        clientid = current_client
        self.clients[clientid] = client_socket
        print(f"New client connected: {client_socket.getpeername()} ({clientid})")

        while True:
            recieved_data: str = client_socket.recv(1024).decode()
            split_data = recieved_data.split("EOM2101")[:-1]
            data: list[tuple] = []
            for item in split_data:
                data.append((str(item[:4]), str(item[4:])))
            for item in data:
                try:
                    match item[0]:
                        case "2400":  # disconnect
                            print(f"Recieved ({clientid}): ", data)  # TODO: REMOVE
                            self.send(clientid, 1400)
                            self.send_others(clientid, 1401, str(clientid))
                            del self.clients[clientid]
                            print(f"Client disconnected: {client_socket.getpeername()}")
                            client_socket.close()
                            return
                        case "2300":  # connect
                            print(f"Recieved ({clientid}): ", data)  # TODO: REMOVE
                            self.send(clientid, 1300, str(list(self.clients.keys()))[1:-1])
                            self.send_others(clientid, 1302, str(clientid))
                        case "2301":  # clientid
                            print(f"Recieved ({clientid}): ", data)  # TODO: REMOVE
                            self.send(clientid, 1301, str(clientid))
                        case "2500":
                            self.send_others(clientid, 1500, item[1])
                        case "2501":
                            self.send_others(clientid, 1501, str(clientid) + ", " + item[1])
                        case _:
                            print(f"Recieved ({clientid}): ", data)
                except Exception as e:
                    print(f"Error handling client: {e}")
                    return

    def start_listening(self) -> None:
        self.socket.listen(self.max_connections)
        print("Server is listening...")
        current_client: int = 1
        while True:
            client_soc, client_address = self.socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_soc, current_client,))
            client_thread.start()
            current_client += 1

    def send(self, clientid: int, code: int, message: str = "") -> None:
        full_message: str = str(code) + message + "EOM2101"
        self.clients[clientid].send(full_message.encode())
        if code != 1501:
            print(f"Sent ({clientid}): ", code, message)

    def send_others(self, clientid: int, code: int, message: str = "") -> None:
        for otherid, client in self.clients.items():
            if otherid != clientid:
                self.send(otherid, code, message)


class Client:
    def __init__(self) -> None:
        self.hostname: str = "127.0.0.1"
        self.port: int = 8080
        self.socket: socket = None
        self.client_id: int = 0
        self.receive_thread: threading.Thread = threading.Thread()
        self.current_data: list = []
        print("Client initializing...")

    def init_socket(self, hostname: str, port: int) -> bool:
        if hostname:
            self.hostname = hostname
        if port:
            self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.hostname, self.port))
        except socket.gaierror:
            print("Not a valid IP.")
            return False
        except ConnectionRefusedError:
            print("No server with said IP is online.")
            return False
        except TimeoutError:
            print("Timed out, server took too long to connect.")
            return False
        print(f"Client socket connected to {self.hostname}:{self.port}")
        self.send(2300)
        self.receive_thread = threading.Thread(target=self.receive_data)
        self.receive_thread.start()
        self.send(2301)
        return True

    def receive_data(self) -> None:
        while True:
            try:
                recieved_data: str = self.socket.recv(1024).decode()
                split_data = recieved_data.split("EOM2101")[:-1]
                data: list[tuple] = []
                for item in split_data:
                    data.append((str(item[:4]), str(item[4:])))
                for item in data:
                    match item[0]:
                        case "1300":  # connect + other ids
                            print(f"Recieved: ", data)  # TODO: REMOVE
                            self.current_data.append("1300" + item[1])
                        case "1301":  # client id
                            print(f"Recieved: ", data)  # TODO: REMOVE
                            self.client_id = int(item[1])
                            print("Client ID: ", self.client_id)
                        case "1302":  # other client connected
                            print(f"Recieved: ", data)  # TODO: REMOVE
                            self.current_data.append("1302" + item[1])
                        case "1400":  # disconnect
                            print(f"Recieved: ", data)  # TODO: REMOVE
                            return
                        case "1401":  # other client disconnected
                            print(f"Recieved: ", data)  # TODO: REMOVE
                            self.current_data.append("1401" + item[1])
                        case "1500":  # any game data
                            self.current_data.append("1500" + item[1])
                        case "1501":  # coordenates
                            self.current_data.append("1501" + item[1])
                        case _:
                            print(f"Recieved: ", data)  # TODO: REMOVE
                            pass
            # except ValueError as e:
            #     print(f"Error, a client sent wrong data: {e}")
            except Exception as e:
                print(f"Error: {e}")
                return

    def send(self, code: int, message: str = "") -> None:
        full_message: str = str(code) + message + "EOM2101"
        self.socket.send(full_message.encode())
        if code != 2501:
            print(f"Sent: ", code, message)

    def clear_data(self) -> None:
        self.current_data = []

# when client joins server it needs to know who is already connected


"""
                ==== 1 SERVER ====
1 Info
- 00 Send Connected Clients (SCC)
    - Replies with list of connected clients (name, id) except self
- 01 End Of Message (EOM)
    - Signals the end of a message

2 Error
- 00

3 Connect
- 00 Accept Connection (AC)
    - Replies with all connected client ids
- 01 Send Client ID (SCI)
    - Replies with client id
- 02 Other Client Connected (OCC)
    - Notifies every client that a client has joined and its id

4 Disconnect
- 00 Confirm Disconnection (CD)
    - Confirms the disconnection and stops the thread
- 01 Other Client Disconnected (OCD)
    - Notifies every client that a client has left and its id

5 Game
- 00 Send Echo (SE)
    - Sends previously recieved data to all other clients
- 01 Coordenate Change (CC)
    - Sends coordenates to all other clients and client id


                ==== 2 CLIENT ====
1 Info
- 00 Request Connected Clients (RCC)
    - Requests a list of connected clients (name, id) except self
- 01 End Of Message (EOM)
    - Signals the end of a message

2 Error
- 00

3 Connect
- 00 Request Connection (RC)
    - Requests connection and own client id
- 01 Request ID (RI)
    - Requests own client id

4 Disconnect
- 00 Inform Disconnection (ID)
    - Informs that the client will disconnect shortly

5 Game
- 00 Request Echo (RE)
    - Sends any data to all other clients
- 01 Coordenate Change (CC)
    - Sends coordenates to all other clients and own client id


Transmission Example:
== Server Start ==
2300  C RC
1301. S AC and SCI
2100  C RCC
1101. S SCC
"""