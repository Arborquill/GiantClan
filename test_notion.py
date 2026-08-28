import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

EVENTS_DATABASE_ID = "3b79cd66-e972-80d0-aa83-de1c481c6ef6"
EVENTS_DATA_SOURCE_ID = "3b79cd66-e972-8014-9954-000b6da417a8"

notion = Client(auth=NOTION_TOKEN)

EXPECTED_PROPERTIES = [
    "Kit Cats",
    "Parent Cats",
    "Sibling Cats",
    "Cohort Cats",
    "Mate Cats",
    "Mentor Cats",
    "Apprentice Cats",
]

print("=" * 70)
print("EVENT RELATION PROPERTY SCHEMA TEST")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

print("Event Database ID:")
print(EVENTS_DATABASE_ID)

print()
print("Event Data Source ID:")
print(EVENTS_DATA_SOURCE_ID)

print()
print("Retrieving data source...")

data_source = notion.data_sources.retrieve(
    data_source_id=EVENTS_DATA_SOURCE_ID
)

print("Data source retrieved successfully.")

properties = data_source.get("properties", {})

print()
print("=" * 70)
print("RELATION PROPERTY CHECK")
print("=" * 70)

all_passed = True

for property_name in EXPECTED_PROPERTIES:
    print()
    print(property_name)

    property_data = properties.get(property_name)

    if not property_data:
        print("ERROR: Property does not exist.")
        all_passed = False
        continue

    property_type = property_data.get("type")

    print("Property type:")
    print(property_type)

    if property_type != "relation":
        print("ERROR: Property is not a relation.")
        all_passed = False
        continue

    relation_data = property_data.get("relation", {})

    print("Relation configuration:")
    print(relation_data)

    target = relation_data.get("database_id")

    if target:
        print("Target database ID:")
        print(target)
    else:
        print("Target database ID:")
        print("[NOT PROVIDED BY API]")

    print("PASS: Property is a relation.")

print()
print("=" * 70)
print("FINAL RESULT")
print("=" * 70)

if all_passed:
    print("ALL SEVEN EVENT PROPERTIES ARE RELATIONS.")
else:
    print("ONE OR MORE EVENT PROPERTIES FAILED THE RELATION CHECK.")

print()
print("READ ONLY - NO DATABASES, PAGES, OR PROPERTIES WERE MODIFIED.")
print("=" * 70)
