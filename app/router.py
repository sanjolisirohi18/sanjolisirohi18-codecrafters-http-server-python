from ast import Call
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
        print(f"request path: {request.path}")
        # 1. Check exact matches
        if request.path in self.routes:
            print("check exact match")
            return self.routes[request.path](request)
        
        # 2. Check dynamic prefix matches
        for prefix, handler in self.routes.items():
            print("check dynamic prefix")
            print(f"prefix: {prefix}")
            print(f"handler: {handler}")
            if prefix.endswith("/") and request.path.startswith(prefix):
                return handler(request)
        
        # 3. Default 404 handler
        return HttpResponse(status_code=404, body="404 Not Found")