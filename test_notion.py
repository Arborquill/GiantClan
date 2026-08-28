import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

EVENTS_DATABASE_ID = "3b79cd66-e972-80d0-aa83-de1c481c6ef6"

notion = Client(auth=NOTION_TOKEN)

print("=" * 70)
print("EVENT DATABASE API SCHEMA")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

database = notion.databases.retrieve(
    database_id=EVENTS_DATABASE_ID
)

print("Database ID:")
print(database["id"])

print()
print("Properties returned by Notion API:")
print()

for name, prop in database.get("properties", {}).items():
    print(f"{name}: {prop.get('type')}")

print()
print("=" * 70)
print("END SCHEMA")
print("=" * 70)
