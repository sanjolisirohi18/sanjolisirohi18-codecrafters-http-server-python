#from shutil import ExecError
import socket  # noqa: F401
import threading
import sys
from typing import Tuple


def get_request_user_agent(user_agent: str) -> Tuple[int, str]:
    """ Extracts User Agent from HTTP Request """
    try:
        user_agent_split = user_agent.split(" ")
        print(f"user_agent_split: {user_agent_split}")
        body: str = user_agent_split[1][:-1]
        print(f"body: {body}")

        return len(body), body
    except Exception as e:
        print(f"Error in extracting User Agent from HTTP Request: {e}")

def response_status_line(url_path: str, **kwargs) -> Tuple[int, str, int, str]:
    """ Creates HTTP REsponse - status code, reason phrase, content length and response body"""
    try:
        status_code: int = 0
        reason_phrase: str = ""
        content_length: int = 0
        body: str = ""
        user_agent: str = kwargs.get('user_agent', None)
        url_path_split = url_path.split("/")
        print(f"url path split: {url_path_split} \n")

        if url_path_split[-1] == "":
            status_code = 200
            reason_phrase = "OK"
        elif url_path_split[1] == "echo":
            status_code = 200
            reason_phrase = "OK"
            content_length = len(url_path_split[2])
            body = url_path_split[2]
        elif url_path_split[1] == "user-agent":
            status_code = 200
            reason_phrase = "OK"
            content_length, body = get_request_user_agent(user_agent)
        else:
            status_code = 404
            reason_phrase = "Not Found"
        
        return status_code, reason_phrase, content_length, body
    except Exception as e:
        print(f"Error in creating HTTP response - status code, reason phrase, content length and response body: {e}")

def get_http_request(data: str) -> Tuple[int, str, int]:
    """ Creates HTTP Request """

    try:
        data_split = data.split("\n")
        print(f"data_split: {data_split} \n")

        # Request Line
        request_line = data_split[0].split(" ")
        method: str = request_line[0]
        print(f"method: {method} \n")
        request_target: str = request_line[1]
        print(f"request_target: {request_target} \n")
        
        return response_status_line(request_target, user_agent=data_split[2])
    except Exception as e:
        print(f"Error in creating HTTP request: {e}")


def get_http_response(data: str) -> bytes:
    """ Creates HTTP Response """

    try:
        version: str = "HTTP/1.1"
        status_code, reason_phrase, content_length, body = get_http_request(data)

        status_line: str = f"{version} {status_code} {reason_phrase}"

        header: str = ""
        content_type: str = "text/plain"
        headers: str = f"{header}"

        if content_length > 0:
            headers = f"Content-Type: {content_type}\r\nContent-Length: {content_length}\r\n"
        
        response_body: str = f"{body}"

        response: str = f"{status_line}\r\n{headers}\r\n{response_body}\r\n"

        return response.encode()
    except Exception as e:
        print(f"Error in creating HTTP response: {e}")

def handle_client(conn, addr):
    print(f"Accepted connection from {addr}")

    try:
        #Receive data from client
        data = conn.recv(1024).decode()

        if not data: 
            print(f"No data received from {addr}")
            return
        
        print(f"data: {data} \n")

        conn.sendall(get_http_response(data))
        # conn.sendall(get_http_response(data))
        conn.close()
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        # Close connection when done
        conn.close()
        print(f"Connection with {addr} closed.")

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # TODO: Uncomment the code below to pass the first stage
    #
    print(f"Input arguments: {sys.argv}\n")
    server_address = ("localhost", 4221)
    server_socket = socket.create_server(server_address, reuse_port=True)
    print(f"Server listening on {server_address}")

    while True:
        try:
            conn, addr = server_socket.accept() # wait for client
            client_thread = threading.Thread(
                target=handle_client, 
                args=(conn, addr)
            )
            client_thread.start()
        except Exception as e:
            print(f"Error acception connection: {e}")
            break

    # data = conn.recv(1024).decode()
    # print(f"data: {data} \n")
    # conn.sendall(get_http_response(data))
    # conn.close()


if __name__ == "__main__":
    main()
