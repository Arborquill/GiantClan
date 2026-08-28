import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

CATS_DATABASE_ID = "9849cd66-e972-8390-b142-01cdd6b8b3a6"

notion = Client(auth=NOTION_TOKEN)

print("=" * 70)
print("ALL CATS DATA SOURCE TEST")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

print("All Cats Database ID:")
print(CATS_DATABASE_ID)

print()
print("Retrieving database...")

database = notion.databases.retrieve(
    database_id=CATS_DATABASE_ID
)

print("Database retrieved successfully.")

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
