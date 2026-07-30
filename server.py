import http.server
import socketserver
import mimetypes

PORT = 8000

# Explicitly add/override MIME types to prevent Windows registry corruption issues
mimetypes.init()
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('image/svg+xml', '.svg')
mimetypes.add_type('application/pdf', '.pdf')

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Prevent caching during development/debugging
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

# Allow address reuse to restart the server without "Address already in use" errors
socketserver.TCPServer.allow_reuse_address = True

print(f"Iniciando servidor de desarrollo en http://localhost:{PORT}")
print("Tipos MIME configurados explícitamente para evitar bloqueos del navegador.")

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
