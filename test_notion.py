import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

EVENTS_DATABASE_ID = "3b79cd66-e972-80d0-aa83-de1c481c6ef6"

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
print("DATABASE RESPONSE KEYS")
print("=" * 70)

for key in database.keys():
    print(key)

print()
print("=" * 70)
print("DATA SOURCES")
print("=" * 70)

data_sources = database.get("data_sources", [])

print("Number of data sources:")
print(len(data_sources))

for data_source in data_sources:
    print()
    print("Data source:")
    print(data_source)

print()
print("=" * 70)
print("END TEST")
print("=" * 70)
