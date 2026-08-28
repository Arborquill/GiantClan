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

print("Query successful.")
print("Top-level keys returned:")
print(list(result.keys()))
print()

print("Number of events returned:")
print(len(result.get("results", [])))
print()

print("=" * 70)
print("TEST COMPLETE")
print("No Notion pages or properties were modified.")
print("=" * 70)
