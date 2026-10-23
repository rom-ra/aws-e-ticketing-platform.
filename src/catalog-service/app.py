from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Steps 7-9: the ECS Fargate task answers "list events" requests behind the ALB.
EVENTS = [
    {"id": 1, "name": "Concert", "seats_left": 120},
    {"id": 2, "name": "Football match", "seats_left": 300},
]


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":  # used by the ALB health check
            self._send(200, {"status": "ok"})
        elif self.path == "/events":
            self._send(200, EVENTS)
        else:
            self._send(404, {"message": "Not found"})

    def _send(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
