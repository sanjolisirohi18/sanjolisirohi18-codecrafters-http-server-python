from ast import Call
import gzip
from pathlib import Path
from typing import Dict, Callable

from .models import HttpRequest, HttpResponse
from .handler import (
    handle_root,
    handle_echo,
    handle_user_agent,
    handle_files
)

class Router:
    """ Maps requests to specific handler functions. """
    def __init__(self, directory: Path = None):
        self.directory = directory
        self.routes: Dict[str, Callable[[HttpRequest], HttpResponse]] = {
            "/": handle_root,
            "/user-agent": handle_user_agent,
            "/echo/": handle_echo,
            "/files/": lambda req: handle_files(req, self.directory)
        }
    
    def route(self, request: HttpRequest) -> HttpResponse:
        """ Dispatches the request to the correct handler based on the path."""

        accept_encoding = request.headers.get("accept-encoding", "")
        print(f"accept-encoding: {accept_encoding}\n")
        use_gzip = "gzip" in accept_encoding
        print(f"use_gzip: {use_gzip}\n")
        print(f"request.path: {request.path}\n")
        print(f"request.headers: {request.headers}\n")
        print(f"request.body: {request.body}\n")
        # 1. Check exact matches
        if request.path in self.routes and request.path != "/":
            print("check exact match")
            return self.routes[request.path](request)
        
        # 2. Check dynamic prefix matches
        for prefix, handler in self.routes.items():
            print("check dynamic prefix")

            if prefix != "/" and prefix.endswith("/") and request.path.startswith(prefix):
                response = handler(request)

                if use_gzip:
                    response.content_encoding = "gzip"

                return response
        
        # 4. Handle the Root Path
        if request.path == "/":
            print(f"check root match")
            return self.routes[request.path](request)
        
        # 3. Default 404 handler
        return HttpResponse(status_code=404, body="404 Not Found")