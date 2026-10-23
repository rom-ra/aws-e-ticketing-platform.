"""Steps 7-9: the catalog service. Reads events and seats from DynamoDB (through the VPC endpoint)."""
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

import boto3
from boto3.dynamodb.conditions import Attr, Key

table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])


def list_events():
    # Event details are stored as items whose sort key is "META"
    items = table.scan(FilterExpression=Attr("sk").eq("META"))["Items"]
    return [{"eventId": i["pk"], "name": i["name"], "date": i.get("date")} for i in items]


def list_seats(event_id):
    items = table.query(KeyConditionExpression=Key("pk").eq(event_id))["Items"]
    return [{"seatId": i["sk"], "status": i["status"]} for i in items if i["sk"] != "META"]


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parts = self.path.strip("/").split("/")
        if parts == ["health"]:  # ALB health check
            self._send(200, {"status": "ok"})
        elif parts == ["events"]:
            self._send(200, list_events())
        elif len(parts) == 3 and parts[0] == "events" and parts[2] == "seats":
            self._send(200, list_seats(parts[1]))
        else:
            self._send(404, {"message": "Not found"})

    def _send(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode())


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
