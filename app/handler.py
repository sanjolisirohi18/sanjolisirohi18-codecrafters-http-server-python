from pathlib import Path

from .models import HttpRequest, HttpResponse

# Handler Functions
def handle_root(request: HttpRequest) -> HttpResponse:
    """ Handler for GET / """
    return HttpResponse(status_code=200, body="")

def handle_echo(request: HttpRequest) -> HttpResponse:
    """ Handler for GET /echo/<message> """
    path_parts = request.path.split("/", 2)
    message = path_parts[2] if len(path_parts) > 2 else ""

    return HttpResponse(status_code=200, body=message)

def handle_user_agent(request: HttpRequest) -> HttpResponse:
    """ Handler for GET /user-agent """
    user_agent = request.headers.get("User-Agent", "")

    return HttpResponse(status_code=200, body=user_agent)

def handle_files(request: HttpRequest, directory: Path) -> HttpResponse:
    """ Handler for GET /files/<filename> """

    try:
        file_name = request.path.split("/", 2)[2]
        file_path = directory / file_name
        print(f"file path: {file_path}")
    except IndexError:
        return HttpResponse(status_code=400, body="Bad Request: Missing filename")
    
    if file_path.is_file():
        print(f"file_path exists: {file_path}")
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            return HttpResponse(status_code=200, body=content, content_type="application/octet-stream")
        except IOError:
            return HttpResponse(status_code=500, body="Internal Server Error")
    else:
        return HttpResponse(status_code=404, body="Not Found")