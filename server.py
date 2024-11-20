import os
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

PORT = int(os.environ.get("PORT", 8000))  # Puerto dinámico de Heroku
DIRECTORY = "build/web"  # Carpeta generada por Pygbag

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

with TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
