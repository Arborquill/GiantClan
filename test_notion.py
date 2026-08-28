import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

EVENT_ID = "3c89cd66-e972-80f9-8036-c2858a8a140c"
MAPLEPAW_ID = "3c09cd66-e972-80f9-9355-c0df84dd19ec"

notion = Client(auth=NOTION_TOKEN)

print("=" * 70)
print("ACTUAL LITTER EVENT PARTICIPATION TEST")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

print("Connecting to Notion...")
notion.users.me()
print("Connection successful.")

event = notion.pages.retrieve(page_id=EVENT_ID)

print()
print("=" * 70)
print("TARGET EVENT")
print("=" * 70)

print("Event ID:")
print(EVENT_ID)

properties = event["properties"]

print()
print("Property names:")
print(list(properties.keys()))

print()
print("=" * 70)
print("DIRECT EVENT PARTICIPANTS")
print("=" * 70)

subject_ids = []
related_ids = []

if "Subject Cat" in properties:
subject_ids = [
item["id"]
for item in properties["Subject Cat"].get("relation", [])
]

if "Related Cats" in properties:
related_ids = [
item["id"]
for item in properties["Related Cats"].get("relation", [])
]

participant_ids = list(dict.fromkeys(subject_ids + related_ids))

print()
print("Subject Cat IDs:")
print(subject_ids)

print()
print("Related Cats IDs:")
print(related_ids)

print()
print("ALL DIRECT PARTICIPANT IDs:")
print(participant_ids)

print()
print("=" * 70)
print("MAPLEPAW PARTICIPATION")
print("=" * 70)

print()
print("Maplepaw ID:")
print(MAPLEPAW_ID)

if MAPLEPAW_ID in participant_ids:
print()
print("RESULT: Maplepaw IS a direct participant.")
else:
print()
print("RESULT: Maplepaw is NOT a direct participant.")

print()
print("=" * 70)
print("RELATIONSHIP-SPECIFIC EVENT PROPERTIES")
print("=" * 70)

relationship_properties = [
"Sibling Cats",
"Parent Cats",
"Mate Cats",
"Cohort Cats",
"Mentor Cats",
"Apprentice Cats"
]

for property_name in relationship_properties:
print()
print(property_name + ":")

```
if property_name not in properties:
    print("  PROPERTY NOT FOUND")
    continue

prop = properties[property_name]

print("  Property type:", prop.get("type"))

if prop.get("type") != "relation":
    print("  Not a relation property.")
    continue

ids = [
    item["id"]
    for item in prop.get("relation", [])
]

print("  IDs:", ids)

if MAPLEPAW_ID in ids:
    print("  MAPLEPAW IS LISTED HERE.")
else:
    print("  Maplepaw is not listed here.")
```

print()
print("=" * 70)
print("EXPECTED BEHAVIOR")
print("=" * 70)

print()
print("Maplepaw must NOT appear in this event merely because")
print("he is a sibling of kits who appear in the event.")
print()
print("Maplepaw should only be considered an event participant")
print("when his own page is represented in Subject Cat or Related Cats.")
print()

if MAPLEPAW_ID not in participant_ids:
print("PASS:")
print("Maplepaw is not a direct participant and should not")
print("appear in his event views.")
else:
print("WARNING:")
print("Maplepaw is directly participating in this event.")

print()
print("=" * 70)
print("TEST COMPLETE")
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
print("=" * 70)
