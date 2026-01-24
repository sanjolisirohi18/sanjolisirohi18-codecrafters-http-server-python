class HttpRequest:
    def __init__(self, method: str, path: str, headers: dict, body: str, accept_encoding: str):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body
        self.accept_encoding = accept_encoding
    
    @classmethod
    def from_raw_data(cls, raw_data:str) -> 'HttpRequest':
        lines = raw_data.split("\r\n")
        print(f"lines: {lines}\n")

        # Parse request line
        request_line_parts = lines[0].split(" ")
        method = request_line_parts[0]
        path = request_line_parts[1]

        # Parse headers
        headers = {}
        header_data = lines[2].split(":")
        print(f"header_data: {header_data}\n")
        accept_encoding = header_data[1].strip()
        print(f"accept_encoding: {accept_encoding}\n")

        if len(lines) > 1:
            if header_data[0] == "Accept-Encoding" and accept_encoding in ["gzip"]:
                headers = {
                    "Host": lines[1],
                    "Accept-Encoding": lines[2]
                }
            else:
                headers = {
                    "Host": lines[1],
                    #"User-Agent": lines[2].split(" ")[1] if len(lines[2]) > 0 else '',
                    "User-Agent": lines[2]
                }
        
        print(f"headers: {headers}\n")

        # Parse body
        body = lines[-1] if len(lines[-1]) > 0 else ""

        return cls(method=method, path=path, headers=headers, body=body, accept_encoding=accept_encoding)

class HttpResponse:
    """ Build and format the http response sent back to the client. """

    def __init__(self, status_code: int = 200, body: str = "", content_type: str = "text/plain"):
        self.status_code = status_code
        self.reason_phrase = {
            200: "OK",
            201: "Created",
            400: "Bad Request",
            404: "Not Found",
            405: "Method Not Allowed",
            500: "Internal Server Error",
            501: "Not Implemented"
        }.get(status_code, "Unknown")
        self.body = body
        self.content_type = content_type
        self.content_length = len(body)
        self.content_encoding = "gzip"
    
    def to_bytes(self) -> bytes:
        """ Generates the final, formatted and encoded HTTP Response."""

        status_line = f"HTTP/1.1 {self.status_code} {self.reason_phrase}\r\n"
        
        headers = ""
        print(f"body: {self.body}")
        if self.content_length > 0:
            headers += f"Content-Type: {self.content_type}\r\n"
            headers += f"Content-Length: {self.content_length}\r\n"
            headers += f"Content-Encoding: {self.content_encoding}\r\n"
        
        response_str = f"{status_line}{headers}\r\n{self.body}"
        return response_str.encode()