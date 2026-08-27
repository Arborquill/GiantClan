import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
HISTORICAL_EVENTS_DATA_SOURCE_ID = "3b79cd66-e972-8014-9954-000b6da417a8"

print("Connecting to Notion...")

notion = Client(auth=NOTION_TOKEN)

print("Connection successful.")
print()

print("=" * 70)
print("HISTORICAL EVENTS RELATIONSHIP TEST")
print("=" * 70)
print()
print("READ ONLY - NOTHING WILL BE CHANGED IN NOTION")
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
print("-" * 70)
print(f"EVENT {number}")

name_property = properties.get("Name", {})
title_items = name_property.get("title", [])

event_name = ""

for item in title_items:
    event_name += item.get("plain_text", "")

if not event_name:
    event_name = "(untitled)"

print(f"Name: {event_name}")

subject_property = properties.get("Subject Cat", {})
subject_relations = subject_property.get("relation", [])

subject_names = []

for relation in subject_relations:
    page_id = relation.get("id")

    if page_id:
        page = notion.request(
            f"pages/{page_id}",
            "GET"
        )

        page_properties = page.get("properties", {})
        page_name_property = page_properties.get("Name", {})
        page_title_items = page_name_property.get("title", [])

        cat_name = ""

        for item in page_title_items:
            cat_name += item.get("plain_text", "")

        if cat_name:
            subject_names.append(cat_name)

if subject_names:
    print("Subject Cat: " + ", ".join(subject_names))
else:
    print("Subject Cat: (none)")

related_property = properties.get("Related Cats", {})
related_relations = related_property.get("relation", [])

related_names = []

for relation in related_relations:
    page_id = relation.get("id")

    if page_id:
        page = notion.request(
            f"pages/{page_id}",
            "GET"
        )

        page_properties = page.get("properties", {})
        page_name_property = page_properties.get("Name", {})
        page_title_items = page_name_property.get("title", [])

        cat_name = ""

        for item in page_title_items:
            cat_name += item.get("plain_text", "")

        if cat_name:
            related_names.append(cat_name)

if related_names:
    print("Related Cats: " + ", ".join(related_names))
else:
    print("Related Cats: (none)")
```

print()
print("=" * 70)
print("Relationship test complete.")
print("No Notion pages or properties were modified.")
print("=" * 70)
