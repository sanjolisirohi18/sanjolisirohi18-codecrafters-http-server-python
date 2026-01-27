import sys
from pathlib import Path

from .http_server import HttpServer

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    print(f"Input arguments: {sys.argv}\n")
    directory_path = Path(".")

    if len(sys.argv) > 2 and sys.argv[1] == "--directory":
        directory_path = sys.argv[2]
    
    print(f"Serving files from directory: {directory_path}")

    # Instantiate and start the server
    server = HttpServer(
        host="localhost",
        port=4221,
        directory=directory_path
    )
    server.start()

if __name__ == "__main__":
    main()
