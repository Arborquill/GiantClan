import os
from notion_client import Client

notion = Client(auth=os.environ["NOTION_TOKEN"])

EVENTS = "3b79cd66-e972-8014-9954-000b6da417a8"

print("Connecting to Notion...")
print("Connection successful.")
print()
print("=" * 70)
print("HISTORICAL EVENTS")
print("=" * 70)
print()
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

result = notion.request(
f"data_sources/{EVENTS}/query",
"POST",
{}
)

events = result.get("results", [])

print("Events returned:", len(events))
print()

for event in events:
print(event["id"])

print()
print("=" * 70)
print("TEST COMPLETE")
print("=" * 70)
