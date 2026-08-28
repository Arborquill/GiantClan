import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
EVENT_ID = "3c89cd66-e972-80f9-8036-c2858a8a140c"

notion = Client(auth=NOTION_TOKEN)

print("=" * 70)
print("LITTER EVENT RELATIONSHIP TEST")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

notion.users.me()
print("Connection successful.")
print()

event = notion.pages.retrieve(page_id=EVENT_ID)
p = event["properties"]

print("EVENT")
print("-" * 70)
print(p["Event"]["title"][0]["plain_text"])
print()

print("RELATIONSHIP TYPE")
print("-" * 70)
relationship = p["Relationship Type"]["formula"]["string"]
print(repr(relationship))
print()

print("SUBJECT CAT")
print("-" * 70)
subject = p["Subject Cat"]["relation"]
print(subject)
print()

print("RELATED CATS")
print("-" * 70)
related = p["Related Cats"]["relation"]
print(related)
print()

print("DIRECT PARTICIPANT IDS")
print("-" * 70)
participants = subject + related
participant_ids = [x["id"] for x in participants]
print(participant_ids)
print()

print("PARTICIPANT COUNT")
print("-" * 70)
print(len(participant_ids))
print()

print("MAPLEPAW ID")
print("-" * 70)
print("3c09cd66-e972-80f9-9355-c0df84dd19ec")
print()

print("MAPLEPAW DIRECT PARTICIPANT CHECK")
print("-" * 70)
print("3c09cd66-e972-80f9-9355-c0df84dd19ec" in participant_ids)
print()

print("RELATIONSHIP PROPERTIES PRESENT ON EVENT")
print("-" * 70)
print("Sibling Cats:", p.get("Sibling Cats", {}).get("type"))
print("Parent Cats:", p.get("Parent Cats", {}).get("type"))
print("Kit Cats:", p.get("Kit Cats", {}).get("type"))
print("Cohort Cats:", p.get("Cohort Cats", {}).get("type"))
print("Mate Cats:", p.get("Mate Cats", {}).get("type"))
print("Mentor Cats:", p.get("Mentor Cats", {}).get("type"))
print("Apprentice Cats:", p.get("Apprentice Cats", {}).get("type"))
print()

print("=" * 70)
print("EXPECTED LOGIC")
print("=" * 70)
print()
print("Direct participants are ONLY Subject Cat + Related Cats.")
print()
print("Relationship properties must contain ONLY cats")
print("who are themselves direct participants.")
print()
print("Maplepaw is not a direct participant.")
print()
print("Therefore Maplepaw must not appear in any relationship")
print("property for this event.")
print()
print("This remains true even though Maplepaw is:")
print("  - Blackchirp's kit")
print("  - sibling to the five litter kits")
print()
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION DATA WAS MODIFIED.")
print("=" * 70)
