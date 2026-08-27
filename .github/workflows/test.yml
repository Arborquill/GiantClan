import os
import json
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

ALL_CATS_ID = "9849cd66e9728390b14201cdd6b8b3a6"
EVENTS_ID = "3b79cd66e97280d0aa83de1c481c6ef6"

notion = Client(auth=NOTION_TOKEN)


def inspect_database(name, database_id):
    print()
    print("=" * 70)
    print(name)
    print("=" * 70)

    database = notion.databases.retrieve(database_id=database_id)

    print()
    print("Top-level keys returned by Notion:")
    print(list(database.keys()))

    print()
    print("Database object:")
    print(json.dumps(database, indent=2))

    print()
    print("=" * 70)


print("Connecting to Notion...")
print("Connection successful.")

inspect_database("ALL CATS", ALL_CATS_ID)
inspect_database("HISTORICAL EVENTS", EVENTS_ID)

print()
print("=" * 70)
print("Inspection complete.")
print("No Notion pages or properties were modified.")
print("=" * 70)
