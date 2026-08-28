import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
EVENT_ID = "3c89cd66-e972-80f9-8036-c2858a8a140c"

notion = Client(auth=NOTION_TOKEN)

print("=" * 70)
print("RELATIONSHIP EVENT TEST")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

notion.users.me()
print("Connection successful.")
print()

event = notion.pages.retrieve(page_id=EVENT_ID)
properties = event["properties"]

event_title = properties["Event"]["title"][0]["plain_text"]

print("EVENT")
print("-" * 70)
print(event_title)
print()

relationship_type = properties["Relationship Type"]["formula"]["string"]

print("RELATIONSHIP TYPE")
print("-" * 70)
print(repr(relationship_type))
print()

relationships = relationship_type.split(" · ")

print("DETECTED RELATIONSHIPS")
print("-" * 70)
print(relationships)
print()

subject_ids = [item["id"] for item in properties["Subject Cat"]["relation"]]
related_ids = [item["id"] for item in properties["Related Cats"]["relation"]]

participant_ids = subject_ids + related_ids

print("DIRECT PARTICIPANTS")
print("-" * 70)
print("Subject:")
print(subject_ids)
print()
print("Related:")
print(related_ids)
print()
print("All participants:")
print(participant_ids)
print()

print("=" * 70)
print("RELATIONSHIP PROPERTY TYPES")
print("=" * 70)
print()

print("Kit Cats:", properties["Kit Cats"]["type"])
print("Parent Cats:", properties["Parent Cats"]["type"])
print("Sibling Cats:", properties["Sibling Cats"]["type"])
print("Cohort Cats:", properties["Cohort Cats"]["type"])
print("Mate Cats:", properties["Mate Cats"]["type"])
print("Mentor Cats:", properties["Mentor Cats"]["type"])
print("Apprentice Cats:", properties["Apprentice Cats"]["type"])
print()

print("=" * 70)
print("CURRENT FORMULA RELATIONSHIP VALUES")
print("=" * 70)
print()

print("Kit Cats formula:")
print(properties["Kit Cats"]["formula"])
print()

print("Parent Cats formula:")
print(properties["Parent Cats"]["formula"])
print()

print("Sibling Cats formula:")
print(properties["Sibling Cats"]["formula"])
print()

print("Cohort Cats formula:")
print(properties["Cohort Cats"]["formula"])
print()

print("Mate Cats formula:")
print(properties["Mate Cats"]["formula"])
print()

print("Mentor Cats formula:")
print(properties["Mentor Cats"]["formula"])
print()

print("Apprentice Cats formula:")
print(properties["Apprentice Cats"]["formula"])
print()

print("=" * 70)
print("MAPLEPAW SAFETY CHECK")
print("=" * 70)
print()

print("Maplepaw ID:")
print("3c09cd66-e972-80f9-9355-c0df84dd19ec")
print()

print("Maplepaw is a direct participant:")
print("3c09cd66-e972-80f9-9355-c0df84dd19ec" in participant_ids)
print()

print("=" * 70)
print("TEST COMPLETE")
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
print("=" * 70)
