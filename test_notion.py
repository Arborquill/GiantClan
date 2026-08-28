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
print()

event = notion.pages.retrieve(page_id=EVENT_ID)
properties = event["properties"]

print("=" * 70)
print("TARGET EVENT")
print("=" * 70)

print("Event ID:")
print(EVENT_ID)
print()

print("Event title:")
print(repr(properties.get("Event", {}).get("rich_text", [])))
print()

subject_property = properties.get("Subject Cat", {})
related_property = properties.get("Related Cats", {})

subject_relation = subject_property.get("relation", [])
related_relation = related_property.get("relation", [])

subject_ids = [x["id"] for x in subject_relation]
related_ids = [x["id"] for x in related_relation]

participant_ids = subject_ids + related_ids

print("=" * 70)
print("DIRECT EVENT PARTICIPANTS")
print("=" * 70)

print()
print("Subject Cat IDs:")
print(subject_ids)

print()
print("Related Cats IDs:")
print(related_ids)

print()
print("All direct participant IDs:")
print(participant_ids)

print()
print("=" * 70)
print("MAPLEPAW CHECK")
print("=" * 70)

print()
print("Maplepaw ID:")
print(MAPLEPAW_ID)

print()
print("Maplepaw in Subject Cat:")
print(MAPLEPAW_ID in subject_ids)

print()
print("Maplepaw in Related Cats:")
print(MAPLEPAW_ID in related_ids)

print()
print("Maplepaw is a direct event participant:")
print(MAPLEPAW_ID in participant_ids)

print()
print("=" * 70)
print("RELATIONSHIP PROPERTIES")
print("=" * 70)

relationship_names = [
"Sibling Cats",
"Parent Cats",
"Mate Cats",
"Cohort Cats",
"Mentor Cats",
"Apprentice Cats"
]

for_name_results = []

for relationship_name in relationship_names:
property_data = properties.get(relationship_name, {})
property_type = property_data.get("type")
relation_items = property_data.get("relation", [])
relation_ids = [x["id"] for x in relation_items]
for_name_results.append((relationship_name, property_type, relation_ids))

print()

for result in for_name_results:
print(result[0] + ":")
print("  Type:", result[1])
print("  IDs:", result[2])
print("  Maplepaw listed:", MAPLEPAW_ID in result[2])
print()

print("=" * 70)
print("EXPECTED RESULT")
print("=" * 70)

print()
print("Maplepaw should NOT appear in this event's cat-specific")
print("event view merely because he is related to participants.")
print()
print("He must be an actual participant through Subject Cat")
print("or Related Cats.")
print()

print("=" * 70)
print("TEST COMPLETE")
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
print("=" * 70)
