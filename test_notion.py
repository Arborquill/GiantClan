import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
EVENT_ID = "3c89cd66-e972-80f9-8036-c2858a8a140c"

notion = Client(auth=NOTION_TOKEN)

print("=" * 70)
print("FULL RELATIONSHIP PAYLOAD TEST")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

notion.users.me()
print("Connection successful.")
print()

event = notion.pages.retrieve(page_id=EVENT_ID)
properties = event["properties"]

title_property = properties.get("Event", {})
title_items = title_property.get("title", [])
event_title = title_items[0].get("plain_text", "") if title_items else ""

print("EVENT")
print("-" * 70)
print(event_title)
print()

relationship_property = properties.get("Relationship Type", {})
formula = relationship_property.get("formula", {})
relationship_string = formula.get("string", "")

print("RELATIONSHIP TYPE")
print("-" * 70)
print(repr(relationship_string))
print()

relationship_names = []
parts = relationship_string.split(" · ")

for part in parts:
name = part.strip()
if name:
relationship_names.append(name)

print("Detected relationships:")
print(relationship_names)
print()

subject_property = properties.get("Subject Cat", {})
related_property = properties.get("Related Cats", {})

subject_relation = subject_property.get("relation", [])
related_relation = related_property.get("relation", [])

subject_ids = [item["id"] for item in subject_relation]
related_ids = [item["id"] for item in related_relation]

participant_ids = subject_ids + related_ids
participant_ids = list(dict.fromkeys(participant_ids))

print("DIRECT PARTICIPANTS")
print("-" * 70)
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
print("PARTICIPANT NAMES")
print("=" * 70)

participant_names = {}

for cat_id in participant_ids:
cat_page = notion.pages.retrieve(page_id=cat_id)
cat_properties = cat_page["properties"]
name_property = cat_properties.get("Name", {})
name_items = name_property.get("title", [])
cat_name = name_items[0].get("plain_text", "") if name_items else cat_id
participant_names[cat_id] = cat_name
print(cat_name + " -> " + cat_id)

print()

print("=" * 70)
print("RELATIONSHIP ANALYSIS")
print("=" * 70)

relationship_results = {}

for relationship_name in relationship_names:
relationship_results[relationship_name] = []

print()

for cat_id in participant_ids:
cat_page = notion.pages.retrieve(page_id=cat_id)
cat_properties = cat_page["properties"]
cat_name = participant_names[cat_id]

```
print("-" * 70)
print(cat_name)
print("-" * 70)

for relationship_name in relationship_names:
    if relationship_name == "Kit":
        property_name = "Kits"
    elif relationship_name == "Parent":
        property_name = "Parents"
    elif relationship_name == "Sibling":
        property_name = "Siblings"
    elif relationship_name == "Cohort":
        property_name = "Cohort"
    elif relationship_name == "Mate":
        property_name = "Mate"
    elif relationship_name == "Mentor":
        property_name = "Mentor(s)"
    elif relationship_name == "Apprentice":
        property_name = "Apprentices"
    else:
        property_name = relationship_name

    relation_property = cat_properties.get(property_name, {})
    relation_value = relation_property.get("relation", [])

    related_ids_for_cat = [item["id"] for item in relation_value]

    matching_ids = []

    for other_id in related_ids_for_cat:
        if other_id in participant_ids:
            matching_ids.append(other_id)

    if matching_ids:
        print(relationship_name + ":")
        for matching_id in matching_ids:
            matching_name = participant_names.get(matching_id, matching_id)
            print("  " + cat_name + " <-> " + matching_name)

            if cat_id not in relationship_results[relationship_name]:
                relationship_results[relationship_name].append(cat_id)

            if matching_id not in relationship_results[relationship_name]:
                relationship_results[relationship_name].append(matching_id)
```

print()

print("=" * 70)
print("FINAL HYPOTHETICAL EVENT RELATIONS")
print("=" * 70)

for relationship_name in relationship_names:
print()
print(relationship_name + " Cats:")

```
result_ids = relationship_results[relationship_name]

if not result_ids:
    print("  EMPTY")
else:
    for result_id in result_ids:
        print("  - " + participant_names.get(result_id, result_id))
        print("    " + result_id)
```

print()

print("=" * 70)
print("HYPOTHETICAL UPDATE PAYLOADS")
print("=" * 70)
print()
print("These payloads WOULD be sent to the Event page.")
print("They are NOT being sent.")
print()

event_property_names = {
"Kit": "Kit Cats",
"Parent": "Parent Cats",
"Sibling": "Sibling Cats",
"Cohort": "Cohort Cats",
"Mate": "Mate Cats",
"Mentor": "Mentor Cats",
"Apprentice": "Apprentice Cats"
}

for relationship_name in relationship_names:
result_ids = relationship_results[relationship_name]
event_property_name = event_property_names.get(relationship_name, relationship_name + " Cats")

```
print(event_property_name + ":")

if not result_ids:
    print("  No relation IDs.")
else:
    payload = {
        "properties": {
            event_property_name: {
                "relation": [
                    {"id": result_id}
                    for result_id in result_ids
                ]
            }
        }
    }

    print("  " + repr(payload))
```

print()

print("=" * 70)
print("MAPLEPAW SAFETY CHECK")
print("=" * 70)

maplepaw_id = "3c09cd66-e972-80f9-9355-c0df84dd19ec"

print("Maplepaw direct participant:", maplepaw_id in participant_ids)

maplepaw_found = False

for relationship_name in relationship_names:
if maplepaw_id in relationship_results[relationship_name]:
maplepaw_found = True
print("ERROR: Maplepaw appeared in " + relationship_name + " Cats.")

if not maplepaw_found:
print("PASS: Maplepaw appears in no relationship-specific Event property.")

print()

print("=" * 70)
print("TEST COMPLETE")
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
print("=" * 70)
