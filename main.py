from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class TodoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/tasks':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            tasks = [{"id": 1, "title": "Вернуться в темп DevOps", "done": True}]
            self.wfile.write(json.dumps(tasks).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), TodoHandler)
    print("Приложение запущено на порту 8000...")
    server.serve_forever()
