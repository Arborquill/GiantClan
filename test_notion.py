import os
import json
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

HISTORICAL_EVENTS_DATA_SOURCE_ID = "3b79cd66-e972-8014-9954-000b6da417a8"

def get_title(properties, property_name):
prop = properties.get(property_name, {})
title = prop.get("title", [])

```
if title:
    return "".join(
        item.get("plain_text", "")
        for item in title
    )

return "(untitled)"
```

def get_relation_names(properties, property_name):
prop = properties.get(property_name, {})
relations = prop.get("relation", [])

```
names = []

for relation in relations:
    page_id = relation.get("id")

    if page_id:
        try:
            page = notion.request(
                f"pages/{page_id}",
                "GET"
            )

            page_properties = page.get("properties", {})
            name = get_title(page_properties, "Name")

            if name != "(untitled)":
                names.append(name)
            else:
                names.append(page_id)

        except Exception as error:
            names.append(f"[Could not read {page_id}: {error}]")

return names
```

def query_events():
response = notion.request(
f"data_sources/{HISTORICAL_EVENTS_DATA_SOURCE_ID}/query",
"POST",
{}
)

```
return response
```

print("Connecting to Notion...")
notion = Client(auth=NOTION_TOKEN)
print("Connection successful.")
print()

print("=" * 70)
print("HISTORICAL EVENTS RELATIONSHIP TEST")
print("=" * 70)
print()
print("This test only reads events from Notion.")
print("No pages or properties will be modified.")
print()

try:
response = query_events()

```
events = response.get("results", [])

print(f"Events returned: {len(events)}")
print()

for number, event in enumerate(events, start=1):
    properties = event.get("properties", {})

    event_name = get_title(properties, "Name")
    subjects = get_relation_names(properties, "Subject Cat")
    related = get_relation_names(properties, "Related Cats")

    print("-" * 70)
    print(f"EVENT {number}")
    print(f"Name: {event_name}")
    print(
        "Subject Cat: "
        + (", ".join(subjects) if subjects else "(none)")
    )
    print(
        "Related Cats: "
        + (", ".join(related) if related else "(none)")
    )

print()
print("=" * 70)
print("Relationship test complete.")
print("No Notion pages or properties were modified.")
print("=" * 70)
```

except Exception as error:
print()
print("=" * 70)
print("ERROR")
print("=" * 70)
print(type(error).**name** + ": " + str(error))
raise
