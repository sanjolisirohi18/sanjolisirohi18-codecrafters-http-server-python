import socket  # noqa: F401

def get_http_request(data: str) -> str:
    data_split = data.split("\n")
    print(f"data_split: {data_split} \n")

    # Request Line
    request_line = data_split[0].split(" ")
    method: str = request_line[0]
    print(f"method: {method} \n")
    request_target: str = request_line[1]
    print(f"request_target: {request_target} \n")

    status_code: int = 200
    reason_phrase: str = "OK"

    if request_target[-1] != "/":
        status_code = 404
        reason_phrase = "Not Found"
    
    return status_code, reason_phrase


def get_http_response(data: str) -> bytes:
    version: str = "HTTP/1.1"
    # status_code: int = request_status
    # reason_phrase: int = "OK"
    print(f"http request: {get_http_request(data)}")
    status_code: int, reason_phrase: str = get_http_request(data)

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
    #get_http_request(data)
    conn.sendall(get_http_response(data))


if __name__ == "__main__":
    main()
