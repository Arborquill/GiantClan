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

for event in events:
properties = event.get("properties", {})

```
name_property = properties.get("Name", {})
name_items = name_property.get("title", [])

event_name = ""

for item in name_items:
    event_name = event_name + item.get("plain_text", "")

if not event_name:
    event_name = "(untitled)"

subject_property = properties.get("Subject Cat", {})
subject_relations = subject_property.get("relation", [])

related_property = properties.get("Related Cats", {})
related_relations = related_property.get("relation", [])

print("-" * 70)
print("EVENT:", event_name)
print("Event ID:", event.get("id"))
print("Subject Cat IDs:", subject_relations)
print("Related Cats IDs:", related_relations)
```

print()
print("=" * 70)
print("RELATIONSHIP TEST COMPLETE")
print("No Notion pages or properties were modified.")
print("=" * 70)
