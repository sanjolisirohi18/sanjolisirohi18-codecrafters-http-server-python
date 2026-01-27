from typing import Optional, Dict
import gzip

class HttpRequest:
    def __init__(self, method: str, path: str, headers: dict, body: str):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body
    
    @classmethod
    def from_raw_data(cls, raw_data:str) -> 'HttpRequest':
        lines = raw_data.split("\r\n")
        print(f"lines: {lines}\n")

        # Request line parsing
        if not lines or not lines[0]:
            return cls("", "", {}, "")
        
        parts = lines[0]. split(" ")
        method, path, version = parts[0], parts[1], parts[2]

        # Header parsing
        headers = {}
        header_end_index = 0

        for i, line in enumerate(lines[1:]):
            if not line: # Empty line marks end of headers
                header_end_index = i + 1
                break

            if ":" in line:
                key, value = line.split(":", 1)
                headers[key.strip().lower()] = value.strip()
        
        print(f"headers: {headers}\n")
        
        # Body parsing
        if "user-agent" in headers:
            body = headers["user-agent"]
        else:
            body = "\r\n".join(lines[header_end_index + 1:])

        print(f"body: {body}\n")

        return cls(method=method, path=path, headers=headers, body=body)

class HttpResponse:
    """ Build and format the http response sent back to the client. """

    def __init__(
            self, 
            status_code: int = 200, 
            body: str = "", 
            content_type: str = "text/plain", 
            content_encoding:Optional[str] = None
        ):
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
        self.content_encoding = content_encoding
        self.headers: Dict[str, str] = {
            "Content-Type": content_type
        }
    
    def to_bytes(self) -> bytes:
        """ Generates the final, formatted and encoded HTTP Response."""

        # Prepare the body content
        body_bytes = self.body.encode()

        if self.content_encoding == "gzip":
            body_bytes = gzip.compress(body_bytes)
            self.headers["Content-Encoding"] = self.content_encoding
        
        self.headers["Content-Length"] = str(len(body_bytes))

        # Build the status line
        status_line = f"HTTP/1.1 {self.status_code} {self.reason_phrase}\r\n"
        
        # Build headers
        header_lines = ""
        for key, value in self.headers.items():
            header_lines += f"{key}: {value}\r\n"

        print(f"body: {self.body}")

        return status_line.encode() + header_lines.encode() + b"\r\n" + body_bytes