import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

EVENT_ID = "3c89cd66-e972-80f9-8036-c2858a8a140c"

notion = Client(auth=NOTION_TOKEN)

RELATION_PROPERTIES = [
    "Kit Cats",
    "Parent Cats",
    "Sibling Cats",
    "Cohort Cats",
    "Mate Cats",
]

print("=" * 70)
print("EVENT RELATION READ-BACK TEST")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

print("Event ID:")
print(EVENT_ID)

print()
print("Retrieving Event...")

event = notion.pages.retrieve(
    page_id=EVENT_ID
)

print("Event retrieved successfully.")

print()
print("=" * 70)
print("RELATION VALUES STORED BY NOTION")
print("=" * 70)

properties = event.get("properties", {})

for property_name in RELATION_PROPERTIES:
    print()
    print(property_name)

    property_data = properties.get(property_name)

    if not property_data:
        print("ERROR: Property was not returned.")
        continue

    print("Property type:")
    print(property_data.get("type"))

    if property_data.get("type") != "relation":
        print("ERROR: Property is not a relation.")
        continue

    relation_ids = [
        item["id"]
        for item in property_data.get("relation", [])
        if item.get("id")
    ]

    print("Stored relation IDs:")
    print(relation_ids)

    if relation_ids:
        print("STATUS: NOTION STORED RELATIONS")
    else:
        print("STATUS: EMPTY")

print()
print("=" * 70)
print("END TEST")
print("=" * 70)
print()
print("READ ONLY - NO NOTION DATA WAS MODIFIED.")
