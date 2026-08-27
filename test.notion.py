import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

ALL_CATS_ID = "9849cd66e9728390b14201cdd6b8b3a6"
EVENTS_ID = "3b79cd66e97280d0aa83de1c481c6ef6"

notion = Client(auth=NOTION_TOKEN)

print("Testing All Cats...")
cats = notion.databases.retrieve(database_id=ALL_CATS_ID)

print("All Cats database found:")
print(cats["title"])

print()
print("Testing Historical Events...")
events = notion.databases.retrieve(database_id=EVENTS_ID)

print("Historical Events database found:")
print(events["title"])

print()
print("Connection successful.")
