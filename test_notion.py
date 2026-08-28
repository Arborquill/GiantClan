import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

TARGET_TITLE = "While out on a secret date, Cliffshock and Blackchirp find an orphaned litter of kits in the wreckage of a dead monster. It isn't the direction they expected their lives to be tugged, but their hearts brim with love for them. Their gentle touch and affectionate purrs are the kits’ home now."

MAPLEPAW_ID = "3c09cd66-e972-80f9-9355-c0df84dd19ec"

notion = Client(auth=NOTION_TOKEN)


def get_title(prop):
    if not isinstance(prop, dict):
        return ""

    title_data = prop.get("title", [])

    if not isinstance(title_data, list):
        return ""

    parts = []

    for item in title_data:
        if not isinstance(item, dict):
            continue

        if item.get("plain_text"):
            parts.append(item["plain_text"])
        else:
            text = item.get("text")
            if isinstance(text, dict) and text.get("content"):
                parts.append(text["content"])

    return "".join(parts)


def get_rich_text(prop):
    if not isinstance(prop, dict):
        return ""

    data = prop.get("rich_text", [])

    if not isinstance(data, list):
        return ""

    parts = []

    for item in data:
        if not isinstance(item, dict):
            continue

        if item.get("plain_text"):
            parts.append(item["plain_text"])
        else:
            text = item.get("text")
            if isinstance(text, dict) and text.get("content"):
                parts.append(text["content"])

    return "".join(parts)


def get_relation_ids(prop):
    if not isinstance(prop, dict):
        return []

    relation = prop.get("relation", [])

    if not isinstance(relation, list):
        return []

    return [
        item["id"]
        for item in relation
        if isinstance(item, dict) and item.get("id")
    ]


def get_cat_name(page_id):
    page = notion.pages.retrieve(page_id=page_id)
    properties = page.get("properties", {})

    for prop in properties.values():
        if isinstance(prop, dict) and prop.get("type") == "title":
            name = get_title(prop)
            if name:
                return name

    return "(unknown)"


print("=" * 70)
print("TARGET LITTER EVENT INSPECTION")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

print("Connecting to Notion...")
print("Connection successful.")
print()

# ----------------------------------------------------------------------
# FIND EVENT BY ITS ACTUAL TITLE
# ----------------------------------------------------------------------

print("=" * 70)
print("SEARCHING EVENT DATABASE BY TITLE")
print("=" * 70)

response = notion.search(
    query=TARGET_TITLE,
    filter={
        "property": "object",
        "value": "page"
    }
)

results = response.get("results", [])

matches = []

for page in results:
    if not isinstance(page, dict):
        continue

    properties = page.get("properties", {})

    page_title = ""

    for prop in properties.values():
        if isinstance(prop, dict) and prop.get("type") == "title":
            page_title = get_title(prop)
            break

    if page_title == TARGET_TITLE:
        matches.append(page)

print("Exact title matches:", len(matches))
print()

if not matches:
    print("ERROR: No exact event title match was found.")
    print()
    print("Search results received:")

    for page in results:
        properties = page.get("properties", {})
        page_title = ""

        for prop in properties.values():
            if isinstance(prop, dict) and prop.get("type") == "title":
                page_title = get_title(prop)
                break

        print("-", repr(page_title))
        print("  ID:", page.get("id"))

    raise SystemExit(1)

if len(matches) > 1:
    print("WARNING: Multiple exact matches found.")
    print()

event = matches[0]
event_id = event["id"]
properties = event.get("properties", {})

print("TARGET EVENT FOUND")
print()
print("Event ID:")
print(event_id)
print()

# ----------------------------------------------------------------------
# EVENT TITLE
# ----------------------------------------------------------------------

event_title = ""

for prop in properties.values():
    if isinstance(prop, dict) and prop.get("type") == "title":
        event_title = get_title(prop)
        break

print("=" * 70)
print("EVENT")
print("=" * 70)
print()
print("Title:")
print(repr(event_title))
print()

# ----------------------------------------------------------------------
# EVENT TEXT
# ----------------------------------------------------------------------

if "Event" in properties:
    event_text = get_rich_text(properties["Event"])
else:
    event_text = ""

print("Event property:")
print(repr(event_text))
print()

# ----------------------------------------------------------------------
# RELATIONSHIP TYPE
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
print("DIRECT EVENT PARTICIPANTS")
print("=" * 70)

subject_ids = []
related_ids = []

if "Subject Cat" in properties:
    subject_ids = get_relation_ids(properties["Subject Cat"])

if "Related Cats" in properties:
    related_ids = get_relation_ids(properties["Related Cats"])

print()
print("Subject Cat IDs:")
print(subject_ids)
print()

for cat_id in subject_ids:
    print("-", get_cat_name(cat_id))
    print("  ID:", cat_id)

print()
print("Related Cats IDs:")
print(related_ids)
print()

for cat_id in related_ids:
    print("-", get_cat_name(cat_id))
    print("  ID:", cat_id)

all_participant_ids = list(dict.fromkeys(subject_ids + related_ids))

print()
print("ALL DIRECT PARTICIPANT IDs:")
print(all_participant_ids)
print()

# ----------------------------------------------------------------------
# MAPLEPAW
# ----------------------------------------------------------------------

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

print("Maplepaw in Subject Cat:")
print(MAPLEPAW_ID in subject_ids)

print("Maplepaw in Related Cats:")
print(MAPLEPAW_ID in related_ids)

print("Maplepaw is direct event participant:")
print(MAPLEPAW_ID in all_participant_ids)

print()

# ----------------------------------------------------------------------
# RELATIONSHIP-SPECIFIC FORMULA PROPERTIES
# ----------------------------------------------------------------------

print("=" * 70)
print("RELATIONSHIP-SPECIFIC FORMULA PROPERTIES")
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
    print()
    print(property_name)
    print("-" * 70)

    if property_name not in properties:
        print("Property NOT PRESENT.")
        continue

    prop = properties[property_name]

    print("Property type:")
    print(prop.get("type"))

    if prop.get("type") == "formula":
        formula = prop.get("formula", {})

        print("Raw formula result:")
        print(formula)

        if isinstance(formula, dict):
            print("Formula string:")
            print(repr(formula.get("string", "")))

    elif prop.get("type") == "relation":
        ids = get_relation_ids(prop)

        print("Relation IDs:")
        print(ids)

        for cat_id in ids:
            print("-", get_cat_name(cat_id))

    else:
        print("Raw property:")
        print(prop)

# ----------------------------------------------------------------------
# PARTICIPANT SUMMARY
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("PARTICIPANT SUMMARY")
print("=" * 70)

print()

for cat_id in all_participant_ids:
    name = get_cat_name(cat_id)

    print(name)
    print("ID:", cat_id)

    if cat_id == MAPLEPAW_ID:
        print("MAPLEPAW: DIRECT PARTICIPANT")
    else:
        print("Direct participant: YES")

    print()

if MAPLEPAW_ID not in all_participant_ids:
    print("IMPORTANT RESULT:")
    print("Maplepaw is NOT a direct participant in this event.")
    print("His existing sibling relationship must NOT make this event appear")
    print("in his event view.")

print()
print("=" * 70)
print("TEST COMPLETE")
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
print("=" * 70)
