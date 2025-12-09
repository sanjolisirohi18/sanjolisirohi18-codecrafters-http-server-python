from pathlib import Path

from .models import HttpRequest, HttpResponse

# Handler Functions
def handle_root(request: HttpRequest) -> HttpResponse:
    """ Handler for GET / """
    print("handle root called")
    return HttpResponse(status_code=200, body="")

def handle_echo(request: HttpRequest) -> HttpResponse:
    """ Handler for GET /echo/<message> """
    print("handle echo called")
    path_parts = request.path.split("/", 2)
    message = path_parts[2] if len(path_parts) > 2 else ""

    return HttpResponse(status_code=200, body=message)

def handle_user_agent(request: HttpRequest) -> HttpResponse:
    """ Handler for GET /user-agent """
    print("handle user agent called")
    user_agent = request.headers.get("User-Agent", "")

    return HttpResponse(status_code=200, body=user_agent)

def handle_files(request: HttpRequest, directory: Path) -> HttpResponse:
    """ Handler for GET and POST /files/<filename> """
    print("handle files called")

    # Path extraction and validation
    try:
        print(f"request: {request}")
        file_name = request.path.split("/", 2)[2]
        file_path = Path(f"{directory}{file_name}")
    except IndexError:
        return HttpResponse(status_code=400, body="Bad Request: Missing filename")
    
    # Handle GET (read file)
    if request.method == "GET":
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
    elif request.method == "POST":
        if not request.body:
            return HttpResponse(status_code=400, body="Bad Request: Request body is empty")
        
        try:
            # Write content to file
            with open(file_path, 'w') as f:
                f.write(request.body)
            
            return HttpResponse(status_code=201, body="")
        except Exception:
            return HttpResponse(status_code=500, body="")
    
    return HttpResponse(status_code=405, body="")