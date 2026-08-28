import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
EVENT_ID = "3c89cd66-e972-80f9-8036-c2858a8a140c"

notion = Client(auth=NOTION_TOKEN)

print("=" * 70)
print("RELATION PROPERTY REPLACEMENT TEST")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

notion.users.me()
print("Connection successful.")
print()

event = notion.pages.retrieve(page_id=EVENT_ID)
properties = event["properties"]

print("=" * 70)
print("EVENT")
print("=" * 70)

event_title = properties["Event"]["title"][0]["plain_text"]
print(event_title)
print()

relationship_string = properties["Relationship Type"]["formula"]["string"]

print("=" * 70)
print("RELATIONSHIP TYPES TO PROCESS")
print("=" * 70)
print(repr(relationship_string))
print()

relationship_names = relationship_string.split(" · ")
print(relationship_names)
print()

subject_ids = [x["id"] for x in properties["Subject Cat"]["relation"]]
related_ids = [x["id"] for x in properties["Related Cats"]["relation"]]

participant_ids = list(dict.fromkeys(subject_ids + related_ids))

print("=" * 70)
print("DIRECT EVENT PARTICIPANTS")
print("=" * 70)
print()

participant_names = {}

for cat_id in participant_ids:
cat_page = notion.pages.retrieve(page_id=cat_id)
cat_properties = cat_page["properties"]
name_data = cat_properties["Name"]["title"]
cat_name = name_data[0]["plain_text"]
participant_names[cat_id] = cat_name
print(cat_name)
print(cat_id)
print()

print("=" * 70)
print("RELATIONSHIP ANALYSIS")
print("=" * 70)
print()
print("Only relationships between direct Event participants count.")
print()

results = {}

for relationship_name in relationship_names:
results[relationship_name] = []

for cat_id in participant_ids:
cat_page = notion.pages.retrieve(page_id=cat_id)
cat_properties = cat_page["properties"]
cat_name = participant_names[cat_id]

```
print("-" * 70)
print(cat_name)
print("-" * 70)

for relationship_name in relationship_names:
    property_name = relationship_name

    if relationship_name == "Kit":
        property_name = "Kits"

    if relationship_name == "Parent":
        property_name = "Parents"

    if relationship_name == "Sibling":
        property_name = "Siblings"

    if relationship_name == "Cohort":
        property_name = "Cohort"

    if relationship_name == "Mate":
        property_name = "Mate"

    if relationship_name == "Mentor":
        property_name = "Mentor(s)"

    if relationship_name == "Apprentice":
        property_name = "Apprentices"

    relation_data = cat_properties.get(property_name)

    if relation_data is None:
        print(relationship_name + ": property not found")
        continue

    if relation_data["type"] != "relation":
        print(relationship_name + ": not a relation property")
        continue

    relation_ids = [x["id"] for x in relation_data["relation"]]

    matching_ids = []

    for other_id in relation_ids:
        if other_id in participant_ids:
            matching_ids.append(other_id)

    if len(matching_ids) == 0:
        continue

    print(relationship_name + ":")

    for other_id in matching_ids:
        other_name = participant_names[other_id]

        print("  " + cat_name + " <-> " + other_name)

        if cat_id not in results[relationship_name]:
            results[relationship_name].append(cat_id)

        if other_id not in results[relationship_name]:
            results[relationship_name].append(other_id)
```

print()

print("=" * 70)
print("PROPOSED NEW EVENT RELATIONS")
print("=" * 70)
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
event_property_name = event_property_names[relationship_name]
result_ids = results[relationship_name]

```
print(event_property_name + ":")

if len(result_ids) == 0:
    print("  EMPTY")
    print()
    continue

for result_id in result_ids:
    print("  - " + participant_names[result_id])

print()
```

print("=" * 70)
print("HYPOTHETICAL PAYLOADS")
print("=" * 70)
print()
print("These would be sent to the Event page.")
print("They are NOT being sent.")
print()

for relationship_name in relationship_names:
event_property_name = event_property_names[relationship_name]
result_ids = results[relationship_name]

```
if len(result_ids) == 0:
    print(event_property_name + ": EMPTY")
    print()
    continue

payload = {
    "properties": {
        event_property_name: {
            "relation": [{"id": x} for x in result_ids]
        }
    }
}

print(event_property_name)
print(payload)
print()
```

print("=" * 70)
print("MAPLEPAW SAFETY CHECK")
print("=" * 70)
print()

maplepaw_id = "3c09cd66-e972-80f9-9355-c0df84dd19ec"

print("Maplepaw is a direct participant:")
print(maplepaw_id in participant_ids)
print()

maplepaw_found = False

for relationship_name in relationship_names:
if maplepaw_id in results[relationship_name]:
maplepaw_found = True
print("ERROR: Maplepaw was added to " + relationship_name)

if maplepaw_found is False:
print("PASS: Maplepaw was not added to any Event relationship.")

print()

print("=" * 70)
print("TEST COMPLETE")
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
print("=" * 70)
