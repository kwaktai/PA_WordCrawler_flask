import os
import http.server
from urllib.parse import urlparse
from csv_to_html import csv_to_html_string


class CsvRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        query_components = {}
        if query:
            query_components = dict(qc.split("=") for qc in query.split("&"))
        file_path = query_components.get("file")

        if file_path:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(csv_to_html_string(file_path).encode())
        else:
            # Handle static file requests
            if self.path.endswith('.html') or self.path.endswith('.js'):
                self.send_static_file(self.path[1:])
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Error 404: File not found.')

    def send_static_file(self, filename):
        static_dir = os.path.join(os.path.dirname(__file__), "static")
        file_path = os.path.join(static_dir, filename)

        try:
            with open(file_path, 'rb') as file:
                self.send_response(200)
                if filename.endswith('.html'):
                    self.send_header('Content-Type', 'text/html')
                elif filename.endswith('.js'):
                    self.send_header('Content-Type', 'application/javascript')
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Error 404: File not found.')


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, CsvRequestHandler)
    print("CSV Viewer is running on port 8000...")
    httpd.serve_forever()


# http://localhost:8000/view_csv.html
