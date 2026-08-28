import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

HAWKKIT_EVENT_ID = "3c89cd66-e972-8082-9ae3-f4b5c6fe3ca3"
MAPLEPAW_ID = "3c09cd66-e972-80f9-9355-c0df84dd19ec"

notion = Client(auth=NOTION_TOKEN)


def get_plain_text(value):
    if not isinstance(value, list):
        return ""

    parts = []

    for item in value:
        if not isinstance(item, dict):
            continue

        if item.get("plain_text"):
            parts.append(item["plain_text"])
            continue

        text = item.get("text")

        if isinstance(text, dict) and text.get("content"):
            parts.append(text["content"])

    return "".join(parts)


def get_relation_ids(prop):
    if not isinstance(prop, dict):
        return []

    relation = prop.get("relation")

    if not isinstance(relation, list):
        return []

    ids = []

    for item in relation:
        if isinstance(item, dict) and item.get("id"):
            ids.append(item["id"])

    return ids


def get_page_name(page_id):
    try:
        page = notion.pages.retrieve(page_id=page_id)
        properties = page.get("properties", {})

        for prop in properties.values():
            if not isinstance(prop, dict):
                continue

            if prop.get("type") == "title":
                return get_plain_text(prop.get("title", []))

        return "(no title found)"

    except Exception as error:
        return "(could not retrieve name: " + str(error) + ")"


print("=" * 70)
print("HAWKKIT EVENT RELATIONSHIP INSPECTION")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

print("Connecting to Notion...")
notion.pages.retrieve(page_id=HAWKKIT_EVENT_ID)
print("Connection successful.")
print()

# ----------------------------------------------------------------------
# RETRIEVE EVENT
# ----------------------------------------------------------------------

event = notion.pages.retrieve(page_id=HAWKKIT_EVENT_ID)
properties = event.get("properties", {})

print("=" * 70)
print("EVENT")
print("=" * 70)

event_title = ""

if "Event" in properties:
    event_title = get_plain_text(properties["Event"].get("rich_text", []))

if not event_title:
    for prop in properties.values():
        if isinstance(prop, dict) and prop.get("type") == "title":
            event_title = get_plain_text(prop.get("title", []))
            break

print("Event:")
print(repr(event_title))
print()

print("Event ID:")
print(HAWKKIT_EVENT_ID)
print()

# ----------------------------------------------------------------------
# RELATIONSHIP TYPE FORMULA
# ----------------------------------------------------------------------

print("=" * 70)
print("RELATIONSHIP TYPE")
print("=" * 70)

relationship_type = ""

if "Relationship Type" in properties:
    prop = properties["Relationship Type"]

    print("Property type:")
    print(prop.get("type"))
    print()

    if prop.get("type") == "formula":
        formula = prop.get("formula", {})

        if isinstance(formula, dict):
            relationship_type = formula.get("string", "") or ""

    print("Formula value:")
    print(repr(relationship_type))
else:
    print("Relationship Type property NOT FOUND.")

print()

detected_relationships = []

if relationship_type:
    detected_relationships = [
        item.strip()
        for item in relationship_type.split("·")
        if item.strip()
    ]

print("Detected relationships:")
print(detected_relationships)
print()

# ----------------------------------------------------------------------
# PARTICIPANTS
# ----------------------------------------------------------------------

print("=" * 70)
print("EVENT PARTICIPANTS")
print("=" * 70)

participant_properties = [
    "Subject Cat",
    "Related Cats",
    "Sibling Cats",
    "Parent Cats",
    "Mate Cats",
    "Cohort Cats",
    "Mentor Cats",
    "Apprentice Cats",
]

participant_ids_by_property = {}

for property_name in participant_properties:
    if property_name not in properties:
        participant_ids_by_property[property_name] = []
        print(property_name + ": NOT PRESENT")
        print()
        continue

    prop = properties[property_name]

    if prop.get("type") != "relation":
        participant_ids_by_property[property_name] = []
        print(property_name + ":")
        print("  Type:", prop.get("type"))
        print("  Not a relation property.")
        print()
        continue

    ids = get_relation_ids(prop)
    participant_ids_by_property[property_name] = ids

    print(property_name + ":")
    print("  IDs:", ids)

    if not ids:
        print("  No cats.")
    else:
        for cat_id in ids:
            print("  -", cat_id, "->", get_page_name(cat_id))

    print()

# ----------------------------------------------------------------------
# ALL CATS WHO ARE DIRECTLY INVOLVED
# ----------------------------------------------------------------------

print("=" * 70)
print("DIRECT EVENT PARTICIPANTS")
print("=" * 70)

direct_participant_ids = set()

for property_name in ["Subject Cat", "Related Cats"]:
    for cat_id in participant_ids_by_property.get(property_name, []):
        direct_participant_ids.add(cat_id)

print("Direct participant IDs:")
print(sorted(direct_participant_ids))
print()

for cat_id in sorted(direct_participant_ids):
    print("-", get_page_name(cat_id))
    print("  ID:", cat_id)

print()

# ----------------------------------------------------------------------
# RELATIONSHIP-SPECIFIC PARTICIPANTS
# ----------------------------------------------------------------------

print("=" * 70)
print("RELATIONSHIP-SPECIFIC EVENT DATA")
print("=" * 70)

for property_name in [
    "Sibling Cats",
    "Parent Cats",
    "Mate Cats",
    "Cohort Cats",
    "Mentor Cats",
    "Apprentice Cats",
]:
    ids = participant_ids_by_property.get(property_name, [])

    print(property_name + ":")

    if not ids:
        print("  EMPTY")
    else:
        for cat_id in ids:
            print("  -", get_page_name(cat_id))
            print("    ID:", cat_id)

    print()

# ----------------------------------------------------------------------
# MAPLEPAW CHECK
# ----------------------------------------------------------------------

print("=" * 70)
print("MAPLEPAW CHECK")
print("=" * 70)

print("Maplepaw:")
print(MAPLEPAW_ID)
print()

print("Direct participant?")
print(MAPLEPAW_ID in direct_participant_ids)
print()

for property_name in participant_properties:
    ids = participant_ids_by_property.get(property_name, [])

    if MAPLEPAW_ID in ids:
        print("Maplepaw IS present in:", property_name)
    else:
        print("Maplepaw is NOT present in:", property_name)

print()

# ----------------------------------------------------------------------
# RELATIONSHIP VALIDATION
# ----------------------------------------------------------------------

print("=" * 70)
print("RELATIONSHIP DATA VALIDATION")
print("=" * 70)

for relationship_name in detected_relationships:
    if relationship_name == "Sibling":
        property_name = "Sibling Cats"
    elif relationship_name == "Parent":
        property_name = "Parent Cats"
    elif relationship_name == "Mate":
        property_name = "Mate Cats"
    elif relationship_name == "Cohort":
        property_name = "Cohort Cats"
    elif relationship_name == "Mentor":
        property_name = "Mentor Cats"
    elif relationship_name == "Apprentice":
        property_name = "Apprentice Cats"
    else:
        property_name = relationship_name + " Cats"

    ids = participant_ids_by_property.get(property_name, [])

    print(relationship_name + " -> " + property_name)

    if ids:
        print("  FOUND:", len(ids), "cats")
        for cat_id in ids:
            print("   -", get_page_name(cat_id), "(", cat_id, ")")
    else:
        print("  NO CATS STORED")

    print()

# ----------------------------------------------------------------------
# IMPORTANT PARTICIPATION RULE
# ----------------------------------------------------------------------

print("=" * 70)
print("PARTICIPATION RULE CHECK")
print("=" * 70)

print(
    "A cat should only be included in an event's relationship property "
    "if that cat is itself an actual participant in the event."
)
print()

print("Maplepaw direct participation:", MAPLEPAW_ID in direct_participant_ids)

if MAPLEPAW_ID not in direct_participant_ids:
    print(
        "RESULT: Maplepaw must NOT be treated as an event participant "
        "even if he has sibling/parent/etc. relationships with participants."
    )
else:
    print(
        "RESULT: Maplepaw IS a direct participant and can be evaluated "
        "for event relationship properties."
    )

print()

print("=" * 70)
print("TEST COMPLETE")
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
print("=" * 70)
