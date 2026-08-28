import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

EVENTS_DATABASE_ID = "3b79cd66-e972-80d0-aa83-de1c481c6ef6"
ALL_CATS_DATABASE_ID = "9849cd66-e972-8390-b142-01cdd6b8b3a6"

EVENT_PROPERTIES = [
    "Kit Cats",
    "Parent Cats",
    "Sibling Cats",
    "Cohort Cats",
    "Mate Cats",
    "Mentor Cats",
    "Apprentice Cats",
]

notion = Client(auth=NOTION_TOKEN)

print("=" * 70)
print("EVENT RELATION PROPERTY SCHEMA TEST")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

print("Connecting to Notion...")
events_database = notion.databases.retrieve(
    database_id=EVENTS_DATABASE_ID
)
all_cats_database = notion.databases.retrieve(
    database_id=ALL_CATS_DATABASE_ID
)
print("Connection successful.")

print()
print("=" * 70)
print("ALL CATS DATABASE")
print("=" * 70)

print("Database ID:")
print(all_cats_database["id"])

print("Title:")
for prop in all_cats_database.get("title", []):
    if prop.get("type") == "text":
        print(prop["text"]["content"])

print()
print("=" * 70)
print("EVENT DATABASE")
print("=" * 70)

print("Database ID:")
print(events_database["id"])

print()
print("=" * 70)
print("EVENT RELATION PROPERTIES")
print("=" * 70)

properties = events_database.get("properties", {})

for property_name in EVENT_PROPERTIES:
    print()
    print(property_name)

    prop = properties.get(property_name)

    if prop is None:
        print("ERROR: Property does not exist.")
        continue

    print("Property type:")
    print(prop.get("type"))

    if prop.get("type") != "relation":
        print("ERROR: Property is not a relation.")
        continue

    relation = prop.get("relation", {})

    print("Relation database ID:")
    print(relation.get("database_id"))

    if relation.get("database_id") == ALL_CATS_DATABASE_ID:
        print("OK: Relation points to All Cats.")
    else:
        print("ERROR: Relation does not point to All Cats.")

print()
print("=" * 70)
print("SCHEMA TEST COMPLETE")
print("=" * 70)
print("READ ONLY - NO DATABASES, PAGES, OR PROPERTIES WERE MODIFIED.")
print("=" * 70)
