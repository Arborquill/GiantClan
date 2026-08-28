import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

EVENTS_DATABASE_ID = "3b79cd66-e972-80d0-aa83-de1c481c6ef6"
EVENTS_DATA_SOURCE_ID = "3b79cd66-e972-8014-9954-000b6da417a8"

notion = Client(auth=NOTION_TOKEN)

print("=" * 70)
print("EVENT DATABASE DATA SOURCE TEST")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

print("Database ID:")
print(EVENTS_DATABASE_ID)

print()
print("Retrieving database...")

database = notion.databases.retrieve(
    database_id=EVENTS_DATABASE_ID
)

print("Database retrieved successfully.")

print()
print("=" * 70)
print("DATA SOURCE SCHEMA")
print("=" * 70)

data_source = notion.data_sources.retrieve(
    data_source_id=EVENTS_DATA_SOURCE_ID
)

print("Data source ID:")
print(EVENTS_DATA_SOURCE_ID)

print()
print("Data source name:")
print(data_source.get("name"))

print()
print("Properties returned by Notion API:")

properties = data_source.get("properties", {})

for property_name, property_data in properties.items():
    print()
    print(property_name)
    print("Property type:")
    print(property_data.get("type"))
    print("Property ID:")
    print(property_data.get("id"))

print()
print("=" * 70)
print("END SCHEMA")
print("=" * 70)

print()
print("READ ONLY - NO DATABASES, PAGES, OR PROPERTIES WERE MODIFIED.")
