import socket  # noqa: F401

#def get_http_request()

def get_http_response() -> bytes:
    version: str = "HTTP/1.1"
    status_code: int = 200
    reason_phrase: int = "OK"

    status_line: str = f"{version} {status_code} {reason_phrase}\r\n"

    header: str = ""
    headers: str = f"{header}\r\n"

    response: str = f"{status_line}{headers}"

    return response.encode()


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # TODO: Uncomment the code below to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept() # wait for client
    data = conn.recv(1024).decode()
    print(f"data: {data} \n")
    conn.sendall(get_http_response())


if __name__ == "__main__":
    main()
