import socket
import threading
from typing import Tuple
from pathlib import Path

from .router import Router
from .models import HttpRequest

class HttpServer:
    """ The main server orchestrator handling socket connections. """

    def __init__(self, host:str, port: int, directory: Path):
        self.host = host
        self.port = port
        self.directory = directory
        self.router = Router(directory=self.directory)

    def handle_client(self, conn: socket.socket, addr: Tuple[str, int]):
        """ Reads, processes and responds to a single client connection. """

        print(f"Accepted connection from {addr}")

        try:
            #Receive data from client
            raw_data = conn.recv(1024).decode()
            print("============================")

            if not raw_data: 
                print(f"No data received from {addr}")
                return
            
            print(f"data: {raw_data} \n")

            # 1. Parse Request
            request = HttpRequest.from_raw_data(raw_data)
            
            # 2. Route and Get Response
            response = self.router.route(request)
            print(f"response in http server: {response} \n")

            # 3. Send Response
            conn.sendall(response.to_bytes())
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            # Close connection when done
            conn.close()
            print(f"Connection with {addr} closed.")
    
    def start(self):
        """ Sets up and runs the main server loop. """

        server_address = ("localhost", 4221)
        server_socket = socket.create_server(server_address, reuse_port=True)
        print(f"Server listening on {server_address}")

        while True:
            try:
                conn, addr = server_socket.accept() # wait for client
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(conn, addr)
                )
                client_thread.start()
            except Exception as e:
                print(f"Error acception connection: {e}")
                break