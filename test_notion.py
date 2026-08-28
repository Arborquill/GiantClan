import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

EVENTS_DATABASE_ID = "3b79cd66-e972-80d0-aa83-de1c481c6ef6"
EVENTS_DATA_SOURCE_ID = "3b79cd66-e972-8014-9954-000b6da417a8"
CATS_DATABASE_ID = "9849cd66-e972-8390-b142-01cdd6b8b3a6"
CATS_DATA_SOURCE_ID = "cf09cd66-e972-8293-8c29-073c01330f5b"

notion = Client(auth=NOTION_TOKEN)

TARGET_EVENT_TITLE = (
    "While out on a secret date, Cliffshock and Blackchirp find an orphaned "
    "litter of kits in the wreckage of a dead monster. It isn't the direction "
    "they expected their lives to be tugged, but their hearts brim with love "
    "for them. Their gentle touch and affectionate purrs are the kits’ home now. "
)

RELATIONSHIP_PROPERTIES = {
    "Kit": "Kits",
    "Parent": "Parents",
    "Sibling": "Siblings",
    "Cohort": "Cohort",
    "Mate": "Mate",
    "Mentor": "Mentor(s)",
    "Apprentice": "Apprentices",
}

EVENT_RELATION_PROPERTIES = {
    "Kit": "Kit Cats",
    "Parent": "Parent Cats",
    "Sibling": "Sibling Cats",
    "Cohort": "Cohort Cats",
    "Mate": "Mate Cats",
    "Mentor": "Mentor Cats",
    "Apprentice": "Apprentice Cats",
}


def get_database_pages(data_source_id):
    pages = []
    cursor = None

    while True:
        payload = {}

        if cursor:
            payload["start_cursor"] = cursor

        response = notion.data_sources.query(
            data_source_id=data_source_id,
            **payload,
        )

        pages.extend(response.get("results", []))

        if not response.get("has_more"):
            break

        cursor = response.get("next_cursor")

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
        item["id"]
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

    if formula.get("type") == "string":
        return formula.get("string") or ""

    return ""


def parse_relationship_types(value):
    if not value:
        return []

    return [
        item.strip()
        for item in value.split("·")
        if item.strip()
    ]


print("=" * 70)
print("EVENT RELATIONSHIP BUILD TEST")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

print("Retrieving Event pages...")
events = get_database_pages(EVENTS_DATA_SOURCE_ID)

print("Retrieving All Cats pages...")
cats = get_database_pages(CATS_DATA_SOURCE_ID)

print("Pages retrieved.")

event = None

for page in events:
    if get_title(page) == TARGET_EVENT_TITLE:
        event = page
        break

if event is None:
    print("ERROR: Target event was not found.")
    raise SystemExit(1)

print()
print("=" * 70)
print("EVENT")
print("=" * 70)
print(get_title(event))

subject_ids = get_relation_ids(event, "Subject Cat")
related_ids = get_relation_ids(event, "Related Cats")

participant_ids = []

for cat_id in subject_ids + related_ids:
    if cat_id not in participant_ids:
        participant_ids.append(cat_id)

print()
print("=" * 70)
print("DIRECT PARTICIPANTS")
print("=" * 70)
print(participant_ids)

cat_by_id = {
    page["id"]: page
    for page in cats
}

participant_names = {}

for cat_id in participant_ids:
    page = cat_by_id.get(cat_id)

    if page:
        participant_names[cat_id] = get_title(page)
    else:
        participant_names[cat_id] = "[CAT NOT FOUND]"

print()

for cat_id in participant_ids:
    print(
        participant_names[cat_id],
        "->",
        cat_id,
    )

relationship_formula = get_formula_string(
    event,
    "Relationship Type",
)

relationship_types = parse_relationship_types(
    relationship_formula
)

print()
print("=" * 70)
print("RELATIONSHIP TYPES")
print("=" * 70)
print(relationship_types)

participant_set = set(participant_ids)

results = {}

print()
print("=" * 70)
print("PROPOSED EVENT RELATIONS")
print("=" * 70)

for relationship_type in relationship_types:
    source_property = RELATIONSHIP_PROPERTIES.get(
        relationship_type
    )

    event_property = EVENT_RELATION_PROPERTIES.get(
        relationship_type
    )

    print()
    print("Relationship:")
    print(relationship_type)

    print("Cat property:")
    print(source_property)

    print("Event property:")
    print(event_property)

    if not source_property or not event_property:
        print("WARNING: Missing property mapping.")
        results[relationship_type] = []
        continue

    matching_ids = set()

    for participant_id in participant_ids:
        participant = cat_by_id.get(participant_id)

        if not participant:
            continue

        related_cat_ids = get_relation_ids(
            participant,
            source_property,
        )

        for related_cat_id in related_cat_ids:
            if related_cat_id in participant_set:
                matching_ids.add(related_cat_id)

    ordered_ids = [
        cat_id
        for cat_id in participant_ids
        if cat_id in matching_ids
    ]

    results[relationship_type] = ordered_ids

    print("Would contain:")

    if not ordered_ids:
        print("[NONE]")
    else:
        for cat_id in ordered_ids:
            print(
                participant_names.get(
                    cat_id,
                    "[CAT NOT FOUND]",
                ),
                "->",
                cat_id,
            )

print()
print("=" * 70)
print("FINAL PROPOSED EVENT VALUES")
print("=" * 70)

for relationship_type in relationship_types:
    event_property = EVENT_RELATION_PROPERTIES.get(
        relationship_type
    )

    print()
    print(event_property + ":")

    ids = results.get(
        relationship_type,
        [],
    )

    print(ids)

print()
print("=" * 70)
print("SAFETY CHECK")
print("=" * 70)

maplepaw_id = None

for page in cats:
    if get_title(page) == "Maplepaw":
        maplepaw_id = page["id"]
        break

if maplepaw_id:
    print("Maplepaw direct participant:")
    print(maplepaw_id in participant_set)

    print()
    print("Maplepaw appears in proposed Event relations:")

    found = False

    for relationship_type, ids in results.items():
        if maplepaw_id in ids:
            print(
                "ERROR:",
                relationship_type,
                "-> MAPLEPAW",
            )
            found = True

    if not found:
        print("NO")

print()
print("=" * 70)
print("TEST COMPLETE")
print("=" * 70)
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION DATA WAS MODIFIED.")
