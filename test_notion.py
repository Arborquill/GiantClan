import os
import requests

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
EVENTS_DATABASE_ID = os.environ["EVENTS_DATABASE_ID"]
CATS_DATABASE_ID = os.environ["CATS_DATABASE_ID"]

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

TARGET_EVENT_TITLE = "While out on a secret date, Cliffshock and Blackchirp find an orphaned litter of kits in the wreckage of a dead monster. It isn't the direction they expected their lives to be tugged, but their hearts brim with love for them. Their gentle touch and affectionate purrs are the kits’ home now."

SOURCE_PROPERTIES = {
    "Kit": "Kits",
    "Parent": "Parents",
    "Sibling": "Siblings",
    "Cohort": "Cohort",
    "Mate": "Mate",
    "Mentor": "Mentor(s)",
    "Apprentice": "Apprentices",
}

TARGET_PROPERTIES = {
    "Kit": "Kit Cats",
    "Parent": "Parent Cats",
    "Sibling": "Sibling Cats",
    "Cohort": "Cohort Cats",
    "Mate": "Mate Cats",
    "Mentor": "Mentor Cats",
    "Apprentice": "Apprentice Cats",
}


def get_pages(database_id):
    pages = []
    cursor = None

    while True:
        payload = {}

        if cursor:
            payload["start_cursor"] = cursor

        response = requests.post(
            f"https://api.notion.com/v1/databases/{database_id}/query",
            headers=HEADERS,
            json=payload,
        )

        response.raise_for_status()

        data = response.json()
        pages.extend(data.get("results", []))

        if not data.get("has_more"):
            break

        cursor = data.get("next_cursor")

    return pages


def get_title(page):
    properties = page.get("properties", {})

    for property_data in properties.values():
        if property_data.get("type") == "title":
            title_items = property_data.get("title", [])

            return "".join(
                item.get("plain_text", "")
                for item in title_items
            )

    return ""


def get_relation_ids(page, property_name):
    properties = page.get("properties", {})
    property_data = properties.get(property_name)

    if not property_data:
        return []

    if property_data.get("type") != "relation":
        return []

    return [
        item.get("id")
        for item in property_data.get("relation", [])
        if item.get("id")
    ]


def get_formula_string(page, property_name):
    properties = page.get("properties", {})
    property_data = properties.get(property_name)

    if not property_data:
        return ""

    if property_data.get("type") != "formula":
        return ""

    formula = property_data.get("formula", {})

    if formula.get("type") != "string":
        return ""

    return formula.get("string") or ""


def parse_relationship_types(value):
    if not value:
        return []

    return [
        item.strip()
        for item in value.split("·")
        if item.strip()
    ]


print("=" * 70)
print("FINAL EVENT RELATIONSHIP DRY RUN")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

print("Connecting to Notion...")

events = get_pages(EVENTS_DATABASE_ID)
cats = get_pages(CATS_DATABASE_ID)

print("Connection successful.")

print()
print("=" * 70)
print("FINDING EVENT")
print("=" * 70)

event = None

for page in events:
    if get_title(page) == TARGET_EVENT_TITLE:
        event = page
        break

if event is None:
    print("ERROR: Event was not found.")
    raise SystemExit(1)

event_id = event["id"]

print("Event ID:")
print(event_id)

print()
print("Event:")
print(get_title(event))

print()
print("=" * 70)
print("DIRECT PARTICIPANTS")
print("=" * 70)

subject_ids = get_relation_ids(event, "Subject Cat")
related_ids = get_relation_ids(event, "Related Cats")

participant_ids = []

for cat_id in subject_ids:
    if cat_id not in participant_ids:
        participant_ids.append(cat_id)

for cat_id in related_ids:
    if cat_id not in participant_ids:
        participant_ids.append(cat_id)

cat_by_id = {}

for cat in cats:
    cat_by_id[cat["id"]] = cat

participant_names = {}

for cat_id in participant_ids:
    cat = cat_by_id.get(cat_id)

    if cat:
        participant_names[cat_id] = get_title(cat)
    else:
        participant_names[cat_id] = "[UNKNOWN CAT]"

print("Subject Cat:")
print(subject_ids)

print()
print("Related Cats:")
print(related_ids)

print()
print("All direct participants:")

for cat_id in participant_ids:
    print(
        participant_names[cat_id],
        "->",
        cat_id,
    )

print()
print("Participant count:")
print(len(participant_ids))

print()
print("=" * 70)
print("RELATIONSHIP TYPES")
print("=" * 70)

relationship_string = get_formula_string(
    event,
    "Relationship Type",
)

print("Relationship Type:")
print(repr(relationship_string))

relationship_types = parse_relationship_types(
    relationship_string
)

print()
print("Detected:")
print(relationship_types)

print()
print("=" * 70)
print("BUILDING NEW EVENT RELATIONS")
print("=" * 70)

participant_set = set(participant_ids)

final_relations = {}

for relationship_type in relationship_types:
    source_property = SOURCE_PROPERTIES.get(
        relationship_type
    )

    target_property = TARGET_PROPERTIES.get(
        relationship_type
    )

    print()
    print("-" * 70)
    print(relationship_type)
    print("Source:", source_property)
    print("Target:", target_property)

    if not source_property:
        print("ERROR: No source property mapping.")
        final_relations[relationship_type] = []
        continue

    if not target_property:
        print("ERROR: No target property mapping.")
        final_relations[relationship_type] = []
        continue

    matching_ids = set()

    for participant_id in participant_ids:
        participant = cat_by_id.get(participant_id)

        if not participant:
            continue

        participant_relationships = get_relation_ids(
            participant,
            source_property,
        )

        for related_id in participant_relationships:
            if related_id in participant_set:
                matching_ids.add(related_id)

    ordered_ids = []

    for participant_id in participant_ids:
        if participant_id in matching_ids:
            ordered_ids.append(participant_id)

    final_relations[relationship_type] = ordered_ids

    print()
    print("Cats that would be written:")

    if not ordered_ids:
        print("[NONE]")
    else:
        for cat_id in ordered_ids:
            print(
                participant_names.get(
                    cat_id,
                    "[UNKNOWN CAT]",
                )
            )

print()
print("=" * 70)
print("FINAL VALUES TO WRITE")
print("=" * 70)

for relationship_type in relationship_types:
    target_property = TARGET_PROPERTIES.get(
        relationship_type
    )

    ids = final_relations.get(
        relationship_type,
        [],
    )

    print()
    print(target_property + ":")

    if not ids:
        print("[EMPTY]")
        continue

    for cat_id in ids:
        print(
            "-",
            participant_names.get(
                cat_id,
                "[UNKNOWN CAT]",
            ),
            "(" + cat_id + ")",
        )

print()
print("=" * 70)
print("MAPLEPAW SAFETY CHECK")
print("=" * 70)

maplepaw_id = None

for cat in cats:
    if get_title(cat) == "Maplepaw":
        maplepaw_id = cat["id"]
        break

if maplepaw_id is None:
    print("Maplepaw was not found.")
else:
    print("Maplepaw ID:")
    print(maplepaw_id)

    print()
    print(
        "Maplepaw is a direct participant:",
        maplepaw_id in participant_set,
    )

    print()
    print("Maplepaw appears in proposed relations:")

    maplepaw_found = False

    for relationship_type, ids in final_relations.items():
        if maplepaw_id in ids:
            print(
                "ERROR:",
                relationship_type,
                "contains Maplepaw",
            )
            maplepaw_found = True

    if not maplepaw_found:
        print("NO")

print()
print("=" * 70)
print("EXPECTED FINAL RESULT")
print("=" * 70)

print()
print("Kit Cats:")
print("Hawkkit, Dahliakit, Moorkit, Bluekit, Basskit")

print()
print("Parent Cats:")
print("Cliffshock, Blackchirp")

print()
print("Sibling Cats:")
print("Hawkkit, Dahliakit, Moorkit, Bluekit, Basskit")

print()
print("Cohort Cats:")
print("Hawkkit, Dahliakit, Moorkit, Bluekit, Basskit")

print()
print("Mate Cats:")
print("Cliffshock, Blackchirp")

print()
print("Mentor Cats:")
print("[EMPTY]")

print()
print("Apprentice Cats:")
print("[EMPTY]")

print()
print("=" * 70)
print("TEST COMPLETE")
print("=" * 70)
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
print("=" * 70)