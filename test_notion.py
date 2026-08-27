import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

HISTORICAL_EVENTS_DATA_SOURCE_ID = "3b79cd66-e972-8014-9954-000b6da417a8"

notion = Client(auth=NOTION_TOKEN)

def get_title(properties):
prop = properties.get("Name", {})
title = prop.get("title", [])

```
if not title:
    return "(untitled)"

return "".join(
    item.get("plain_text", "")
    for item in title
)
```

def get_relation_names(properties, property_name):
prop = properties.get(property_name, {})
relation = prop.get("relation", [])

```
names = []

for item in relation:
    page_id = item.get("id")

    if not page_id:
        continue

    page = notion.request(
        f"pages/{page_id}",
        "GET"
    )

    name = get_title(page.get("properties", {}))
    names.append(name)

return names
```

print("Connecting to Notion...")
print("Connection successful.")
print()

print("=" * 70)
print("HISTORICAL EVENTS RELATIONSHIP TEST")
print("=" * 70)
print()
print("This test only reads information from Notion.")
print("No pages or properties will be modified.")
print()

response = notion.request(
f"data_sources/{HISTORICAL_EVENTS_DATA_SOURCE_ID}/query",
"POST",
{}
)

events = response.get("results", [])

print(f"Events returned: {len(events)}")
print()

for number, event in enumerate(events, start=1):
properties = event.get("properties", {})

```
event_name = get_title(properties)

subjects = get_relation_names(
    properties,
    "Subject Cat"
)

related = get_relation_names(
    properties,
    "Related Cats"
)

print("-" * 70)
print(f"EVENT {number}")
print(f"Name: {event_name}")

if subjects:
    print("Subject Cat: " + ", ".join(subjects))
else:
    print("Subject Cat: (none)")

if related:
    print("Related Cats: " + ", ".join(related))
else:
    print("Related Cats: (none)")
```

print()
print("=" * 70)
print("Relationship test complete.")
print("No Notion pages or properties were modified.")
print("=" * 70)
