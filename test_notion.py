import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

# Exact event we identified from the previous test.

EVENT_ID = "3c89cd66-e972-80f9-8036-c2858a8a140c"

MAPLEPAW_ID = "3c09cd66-e972-80f9-9355-c0df84dd19ec"

notion = Client(auth=NOTION_TOKEN)

def get_title(page):
properties = page.get("properties", {})

```
for prop in properties.values():
    if prop.get("type") == "title":
        title_items = prop.get("title", [])
        if title_items:
            return "".join(
                item.get("plain_text", "")
                for item in title_items
            )

return ""
```

def get_relation_ids(page, property_name):
prop = page.get("properties", {}).get(property_name)

```
if not prop:
    return []

if prop.get("type") != "relation":
    return []

return [
    item["id"]
    for item in prop.get("relation", [])
    if "id" in item
]
```

def get_cat_name(cat_id):
try:
page = notion.pages.retrieve(page_id=cat_id)
return get_title(page) or cat_id
except Exception as e:
return f"{cat_id} (name lookup failed: {e})"

print("=" * 70)
print("ACTUAL LITTER EVENT PARTICIPATION TEST")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

print("Connecting to Notion...")
try:
notion.users.me()
print("Connection successful.")
except Exception as e:
print(f"Connection failed: {e}")
raise

print()
print("=" * 70)
print("TARGET EVENT")
print("=" * 70)

event = notion.pages.retrieve(page_id=EVENT_ID)

event_title = get_title(event)

print()
print("Event title:")
print(repr(event_title))

print()
print("Event ID:")
print(EVENT_ID)

print()
print("Property names:")
print(list(event.get("properties", {}).keys()))

print()
print("=" * 70)
print("DIRECT EVENT PARTICIPANTS")
print("=" * 70)

subject_ids = get_relation_ids(event, "Subject Cat")
related_ids = get_relation_ids(event, "Related Cats")

direct_participant_ids = list(dict.fromkeys(subject_ids + related_ids))

print()
print("Subject Cat IDs:")
print(subject_ids)

for cat_id in subject_ids:
print(f"  - {get_cat_name(cat_id)}")
print(f"    {cat_id}")

print()
print("Related Cats IDs:")
print(related_ids)

for cat_id in related_ids:
print(f"  - {get_cat_name(cat_id)}")
print(f"    {cat_id}")

print()
print("ALL DIRECT PARTICIPANT IDs:")
print(direct_participant_ids)

print()
print("ALL DIRECT PARTICIPANTS:")

for cat_id in direct_participant_ids:
print(f"  - {get_cat_name(cat_id)}")
print(f"    {cat_id}")

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
"Apprentice Cats",
]

for property_name in relationship_properties:
prop = event.get("properties", {}).get(property_name)

```
print()
print(property_name + ":")

if not prop:
    print("  PROPERTY NOT FOUND")
    continue

print(f"  Property type: {prop.get('type')}")

if prop.get("type") != "relation":
    print("  Not a relation property.")
    continue

ids = get_relation_ids(event, property_name)

if not ids:
    print("  EMPTY")
    continue

for cat_id in ids:
    print(f"  - {get_cat_name(cat_id)}")
    print(f"    {cat_id}")
```

print()
print("=" * 70)
print("MAPLEPAW PARTICIPATION CHECK")
print("=" * 70)

print()
print("Maplepaw ID:")
print(MAPLEPAW_ID)

print()
print("Maplepaw name:")
print(get_cat_name(MAPLEPAW_ID))

print()
print("Direct participant:")
print(MAPLEPAW_ID in direct_participant_ids)

print()

if MAPLEPAW_ID in direct_participant_ids:
print("RESULT: Maplepaw IS an actual participant in this event.")
else:
print("RESULT: Maplepaw is NOT an actual participant in this event.")

print()
print("=" * 70)
print("RELATIONSHIP PARTICIPATION CHECK")
print("=" * 70)

for property_name in relationship_properties:
ids = get_relation_ids(event, property_name)

```
if MAPLEPAW_ID in ids:
    print()
    print(f"Maplepaw IS listed in {property_name}.")
    print("This relationship property therefore treats Maplepaw as")
    print("a participant in this event.")
else:
    print()
    print(f"Maplepaw is NOT listed in {property_name}.")
```

print()
print("=" * 70)
print("EXPECTED FILTERING RULE")
print("=" * 70)

print()
print("For Maplepaw's event views:")
print()
print("Maplepaw must be a direct event participant.")
print("A sibling/parent/mate/cohort/etc. relationship to an event")
print("participant must NOT by itself make Maplepaw an event participant.")
print()
print("Therefore, if Maplepaw is absent from Subject Cat and Related")
print("Cats, this event must NOT be included in Maplepaw's event view,")
print("even if Maplepaw is a sibling of kits appearing in the event.")
print()
print("=" * 70)
print("TEST COMPLETE")
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
print("=" * 70)
