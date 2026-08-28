import os
from notion_client import Client

notion = Client(auth=os.environ["NOTION_TOKEN"])

EVENTS = "3b79cd66-e972-8014-9954-000b6da417a8"

print("Connecting to Notion...")
print("Connection successful.")
print()
print("=" * 70)
print("HISTORICAL EVENTS RELATIONSHIP TEST")
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

event = events[0]
properties = event.get("properties", {})

print("FIRST EVENT")
print("-" * 70)
print("Event ID:", event.get("id"))
print()

print("Property names:")
print(list(properties.keys()))
print()

print("Subject Cat:")
print(properties.get("Subject Cat"))
print()

print("Related Cats:")
print(properties.get("Related Cats"))
print()

print("=" * 70)
print("RELATIONSHIP TEST COMPLETE")
print("No Notion pages or properties were modified.")
print("=" * 70)
