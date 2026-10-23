"""Loads two sample events with a few seats each. Usage: TABLE_NAME=ticketing-table python seed_events.py"""
import os

import boto3

table = boto3.resource("dynamodb").Table(os.environ.get("TABLE_NAME", "ticketing-table"))
events = {"concert-1": "Summer Concert", "match-1": "Football Match"}

with table.batch_writer() as batch:
    for event_id, name in events.items():
        batch.put_item(Item={"pk": event_id, "sk": "META", "name": name, "date": "2026-12-01"})
        for seat in ["A1", "A2", "A3", "B1", "B2"]:
            batch.put_item(Item={"pk": event_id, "sk": seat, "status": "FREE"})
print("Seeded", len(events), "events")
