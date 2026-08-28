import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

EVENT_ID = "3c89cd66-e972-80f9-8036-c2858a8a140c"

notion = Client(auth=NOTION_TOKEN)

print("=" * 70)
print("FULL LITTER RELATIONSHIP PROCESSING TEST")
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
print("EVENT")
print("=" * 70)
print()

title_data = properties.get("Event", {}).get("title", [])
event_title = title_data[0].get("plain_text", "") if title_data else ""

print("Event:")
print(event_title)
print()

print("=" * 70)
print("RELATIONSHIP TYPE")
print("=" * 70)
print()

relationship_property = properties.get("Relationship Type", {})
relationship_formula = relationship_property.get("formula", {})
relationship_string = relationship_formula.get("string", "")

relationships = [x.strip() for x in relationship_string.split("·") if x.strip()]

print("Formula value:")
print(repr(relationship_string))
print()

print("Detected relationships:")
print(relationships)
print()

print("=" * 70)
print("DIRECT EVENT PARTICIPANTS")
print("=" * 70)
print()

subject_property = properties.get("Subject Cat", {})
related_property = properties.get("Related Cats", {})

subject_ids = [x["id"] for x in subject_property.get("relation", [])]
related_ids = [x["id"] for x in related_property.get("relation", [])]

participant_ids = list(dict.fromkeys(subject_ids + related_ids))

print("Subject IDs:")
print(subject_ids)
print()

print("Related IDs:")
print(related_ids)
print()

print("ALL PARTICIPANT IDs:")
print(participant_ids)
print()

participant_pages = [
notion.pages.retrieve(page_id=x)
for x in participant_ids
]

participant_names = []

for page in participant_pages:
page_properties = page["properties"]
title_properties = [
value
for value in page_properties.values()
if value.get("type") == "title"
]
title_property = title_properties[0] if title_properties else {}
title_items = title_property.get("title", [])
name = title_items[0].get("plain_text", "UNKNOWN") if title_items else "UNKNOWN"
participant_names.append(name)

print("PARTICIPANTS:")
print()

for index in range(len(participant_ids)):
print(
str(index + 1)
+ ". "
+ participant_names[index]
+ " -> "
+ participant_ids[index]
)

print()
print("=" * 70)
print("RELATIONSHIP DATA")
print("=" * 70)
print()

for index in range(len(participant_ids)):
name = participant_names[index]
page = participant_pages[index]
page_properties = page["properties"]

```
print(name)
print("-" * 70)

siblings_property = page_properties.get("Siblings", {})
parents_property = page_properties.get("Parents", {})
kits_property = page_properties.get("Kits", {})
mate_property = page_properties.get("Mate", {})
cohort_property = page_properties.get("Cohort", {})

sibling_ids = [
    x["id"]
    for x in siblings_property.get("relation", [])
]

parent_ids = [
    x["id"]
    for x in parents_property.get("relation", [])
]

kit_ids = [
    x["id"]
    for x in kits_property.get("relation", [])
]

mate_ids = [
    x["id"]
    for x in mate_property.get("relation", [])
]

cohort_ids = [
    x["id"]
    for x in cohort_property.get("relation", [])
]

print("Sibling IDs:", sibling_ids)
print("Parent IDs:", parent_ids)
print("Kit IDs:", kit_ids)
print("Mate IDs:", mate_ids)
print("Cohort IDs:", cohort_ids)
print()
```

print("=" * 70)
print("PROPOSED EVENT RELATIONSHIP PROPERTIES")
print("=" * 70)
print()

print("Only direct event participants are eligible.")
print("A related cat outside the event is excluded.")
print()

print("=" * 70)
print("KIT RELATIONSHIP")
print("=" * 70)
print()

print("Checking participating cats against their Kits and Parents.")

for index in range(len(participant_ids)):
cat_id = participant_ids[index]
cat_name = participant_names[index]
page = participant_pages[index]
page_properties = page["properties"]

```
kits_property = page_properties.get("Kits", {})
parents_property = page_properties.get("Parents", {})

kit_ids = [
    x["id"]
    for x in kits_property.get("relation", [])
]

parent_ids = [
    x["id"]
    for x in parents_property.get("relation", [])
]

participating_kits = [
    participant_names[participant_ids.index(x)]
    for x in kit_ids
    if x in participant_ids
]

participating_parents = [
    participant_names[participant_ids.index(x)]
    for x in parent_ids
    if x in participant_ids
]

if participating_kits:
    print(cat_name + " -> participating Kits:")
    print(participating_kits)

if participating_parents:
    print(cat_name + " -> participating Parents:")
    print(participating_parents)
```

print()
print("=" * 70)
print("SIBLING RELATIONSHIP")
print("=" * 70)
print()

sibling_pairs = []

for a in range(len(participant_ids)):
cat_a_id = participant_ids[a]
cat_a_name = participant_names[a]
page_a = participant_pages[a]
sibling_property = page_a["properties"].get("Siblings", {})

```
sibling_ids = [
    x["id"]
    for x in sibling_property.get("relation", [])
]

for b in range(a + 1, len(participant_ids)):
    cat_b_id = participant_ids[b]
    cat_b_name = participant_names[b]

    if cat_b_id in sibling_ids:
        sibling_pairs.append(
            cat_a_name + " <-> " + cat_b_name
        )
```

print("Participating sibling pairs:")
print()

for pair in sibling_pairs:
print(pair)

print()
print("=" * 70)
print("MATE RELATIONSHIP")
print("=" * 70)
print()

mate_pairs = []

for a in range(len(participant_ids)):
cat_a_id = participant_ids[a]
cat_a_name = participant_names[a]
page_a = participant_pages[a]
mate_property = page_a["properties"].get("Mate", {})

```
mate_ids = [
    x["id"]
    for x in mate_property.get("relation", [])
]

for b in range(a + 1, len(participant_ids)):
    cat_b_id = participant_ids[b]
    cat_b_name = participant_names[b]

    if cat_b_id in mate_ids:
        mate_pairs.append(
            cat_a_name + " <-> " + cat_b_name
        )
```

print("Participating mate pairs:")
print()

for pair in mate_pairs:
print(pair)

print()
print("=" * 70)
print("COHORT RELATIONSHIP")
print("=" * 70)
print()

cohort_pairs = []

for a in range(len(participant_ids)):
cat_a_id = participant_ids[a]
cat_a_name = participant_names[a]
page_a = participant_pages[a]
cohort_property = page_a["properties"].get("Cohort", {})

```
cohort_ids = [
    x["id"]
    for x in cohort_property.get("relation", [])
]

for b in range(a + 1, len(participant_ids)):
    cat_b_id = participant_ids[b]
    cat_b_name = participant_names[b]

    if cat_b_id in cohort_ids:
        cohort_pairs.append(
            cat_a_name + " <-> " + cat_b_name
        )
```

print("Participating cohort pairs:")
print()

for pair in cohort_pairs:
print(pair)

print()
print("=" * 70)
print("MAPLEPAW SAFETY CHECK")
print("=" * 70)
print()

print("Maplepaw ID:")
print("3c09cd66-e972-80f9-9355-c0df84dd19ec")
print()

print("Maplepaw is a direct participant:")
print(
"3c09cd66-e972-80f9-9355-c0df84dd19ec"
in participant_ids
)

print()
print("Maplepaw must NOT be added to any event relationship")
print("property for this event unless he is a direct participant.")
print()

print("=" * 70)
print("TEST COMPLETE")
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
print("=" * 70)
