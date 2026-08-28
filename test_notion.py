import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

EVENT_ID = "3c89cd66-e972-80f9-8036-c2858a8a140c"
MAPLEPAW_ID = "3c09cd66-e972-80f9-9355-c0df84dd19ec"

notion = Client(auth=NOTION_TOKEN)

print("=" * 70)
print("LITTER EVENT RELATIONSHIP LOGIC TEST")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

print("Connecting to Notion...")
notion.users.me()
print("Connection successful.")
print()

event = notion.pages.retrieve(page_id=EVENT_ID)
event_properties = event["properties"]

print("=" * 70)
print("EVENT")
print("=" * 70)

print()
print("Event ID:")
print(EVENT_ID)

print()
print("Event title:")
print(event_properties.get("Event", {}))

print()
print("=" * 70)
print("RELATIONSHIP TYPE FORMULA")
print("=" * 70)

relationship_formula = event_properties.get("Relationship Type", {})
formula_data = relationship_formula.get("formula", {})
relationship_string = formula_data.get("string", "")

print()
print("Formula value:")
print(repr(relationship_string))

relationships = [x.strip() for x in relationship_string.split("·") if x.strip()]

print()
print("Detected relationships:")
print(relationships)

print()
print("=" * 70)
print("DIRECT EVENT PARTICIPANTS")
print("=" * 70)

subject_property = event_properties.get("Subject Cat", {})
related_property = event_properties.get("Related Cats", {})

subject_ids = [x["id"] for x in subject_property.get("relation", [])]
related_ids = [x["id"] for x in related_property.get("relation", [])]

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

participant_pages = [notion.pages.retrieve(page_id=x) for x in participant_ids]

participant_names = [
next(
(
item.get("plain_text", "")
for prop in page["properties"].values()
if prop.get("type") == "title"
for item in prop.get("title", [])
),
participant_ids[index]
)
for index, page in enumerate(participant_pages)
]

print()
print("PARTICIPANTS:")

participant_display = [
print_value
for print_value in [
f"{participant_names[index]} -> {participant_ids[index]}"
for index in range(len(participant_ids))
]
]

for value in participant_display:
print(value)

print()
print("=" * 70)
print("MAPLEPAW PARTICIPATION CHECK")
print("=" * 70)

print()
print("Maplepaw:")
print(MAPLEPAW_ID)

print()
print("Is Maplepaw a direct participant?")
print(MAPLEPAW_ID in participant_ids)

print()
print("=" * 70)
print("SIBLING RELATIONSHIP CHECK")
print("=" * 70)

sibling_relation_data = [
(
participant_names[index],
participant_ids[index],
[
x["id"]
for x in participant_pages[index]["properties"].get(
"Siblings", {}
).get("relation", [])
]
)
for index in range(len(participant_pages))
]

for name, cat_id, sibling_ids in sibling_relation_data:
print()
print(name)
print("ID:", cat_id)
print("Existing sibling IDs:", sibling_ids)
print("Maplepaw is sibling:", MAPLEPAW_ID in sibling_ids)

print()
print("=" * 70)
print("PARTICIPANT-ONLY SIBLING PAIRS")
print("=" * 70)

sibling_pairs = [
(
participant_names[a],
participant_names[b],
participant_ids[a],
participant_ids[b]
)
for a in range(len(participant_ids))
for b in range(a + 1, len(participant_ids))
if participant_ids[b] in sibling_relation_data[a][2]
or participant_ids[a] in sibling_relation_data[b][2]
]

print()

if sibling_pairs:
for pair in sibling_pairs:
print(f"{pair[0]} <-> {pair[1]}")
else:
print("No sibling pairs found among direct participants.")

print()
print("=" * 70)
print("MAPLEPAW EXCLUSION TEST")
print("=" * 70)

maplepaw_sibling_pairs = [
(
participant_names[index],
participant_ids[index]
)
for index in range(len(participant_ids))
if MAPLEPAW_ID in sibling_relation_data[index][2]
]

print()

if MAPLEPAW_ID in participant_ids:
print("Maplepaw IS a direct participant.")
print("Maplepaw may legitimately receive relationship-event data.")
else:
print("Maplepaw is NOT a direct participant.")

print()

if maplepaw_sibling_pairs:
print("Some direct participants have Maplepaw as a sibling:")
for pair in maplepaw_sibling_pairs:
print(f"  {pair[0]} <-> Maplepaw")
print()
print("IMPORTANT:")
print("These sibling relationships must NOT cause Maplepaw")
print("to be added to this event's Sibling Cats property.")
else:
print("No direct participant has Maplepaw listed as a sibling.")

print()
print("=" * 70)
print("EXPECTED EVENT-PROPERTY LOGIC")
print("=" * 70)

print()
print("The event relationship properties must be derived ONLY")
print("from cats who are direct participants in this event.")
print()
print("For Sibling Cats:")
print("  - Both cats must participate in the event.")
print("  - They must actually be siblings.")
print("  - A sibling who does not participate must be excluded.")
print()
print("Therefore:")
print("  Maplepaw must NOT appear in this event's Sibling Cats")
print("  simply because he is siblings with the kits who participated.")
print()
print("This is the same rule we will use for Cohort, Mate, Mentor,")
print("Apprentice, Parent, and the other relationship categories.")

print()
print("=" * 70)
print("TEST COMPLETE")
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
print("=" * 70)
