import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

EVENTS_DATABASE_ID = "3b79cd66-e972-80d0-aa83-de1c481c6ef6"
EVENTS_DATA_SOURCE_ID = "3b79cd66-e972-8014-9954-000b6da417a8"

CATS_DATABASE_ID = "9849cd66-e972-8390-b142-01cdd6b8b3a6"
CATS_DATA_SOURCE_ID = "cf09cd66-e972-8293-8c29-073c01330f5b"

notion = Client(auth=NOTION_TOKEN)

TARGET_EVENT_TITLE = (
    "Cliffshock and Larchstipe get sore pawpads after failing to find lungwort"
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
print("EVENT RELATIONSHIP BUILD")
print("=" * 70)
print()

# ------------------------------------------------------------
# RETRIEVE DATA
# ------------------------------------------------------------

print("Retrieving Event pages...")
events = get_database_pages(EVENTS_DATA_SOURCE_ID)

print("Retrieving All Cats pages...")
cats = get_database_pages(CATS_DATA_SOURCE_ID)

print("Pages retrieved.")

# ------------------------------------------------------------
# FIND TARGET EVENT
# ------------------------------------------------------------

event = None

for page in events:

    title = get_title(page)

    if title == TARGET_EVENT_TITLE:
        event = page
        break

if event is None:

    print("ERROR: Target event was not found.")
    print()
    print("Events containing 'Cliffshock' and 'Larchstipe':")

    for page in events:

        title = get_title(page)

        if "Cliffshock" in title and "Larchstipe" in title:

            print()
            print("Title:")
            print(title)

            print("ID:")
            print(page["id"])

    raise SystemExit(1)

event_id = event["id"]

# ------------------------------------------------------------
# EVENT
# ------------------------------------------------------------

print()
print("=" * 70)
print("EVENT")
print("=" * 70)

print(get_title(event))

print()
print("Event ID:")
print(event_id)

# ------------------------------------------------------------
# GET DIRECT PARTICIPANTS
# ------------------------------------------------------------

subject_ids = get_relation_ids(
    event,
    "Subject Cat"
)

related_ids = get_relation_ids(
    event,
    "Related Cats"
)

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

# ------------------------------------------------------------
# GET RELATIONSHIP TYPES
# ------------------------------------------------------------

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

# ------------------------------------------------------------
# CALCULATE EVENT RELATIONS
# ------------------------------------------------------------

participant_set = set(participant_ids)

results = {}

print()
print("=" * 70)
print("CALCULATED EVENT RELATIONS")
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

        participant = cat_by_id.get(
            participant_id
        )

        if not participant:
            continue

        related_cat_ids = get_relation_ids(
            participant,
            source_property,
        )

        for related_cat_id in related_cat_ids:

            if related_cat_id in participant_set:

                matching_ids.add(
                    related_cat_id
                )

    ordered_ids = [
        cat_id
        for cat_id in participant_ids
        if cat_id in matching_ids
    ]

    results[relationship_type] = ordered_ids

    print("Will contain:")

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

# ------------------------------------------------------------
# BUILD UPDATE PAYLOAD
# ------------------------------------------------------------

print()
print("=" * 70)
print("FINAL EVENT PROPERTY VALUES")
print("=" * 70)

properties_to_update = {}

for relationship_type in relationship_types:

    event_property = EVENT_RELATION_PROPERTIES.get(
        relationship_type
    )

    if not event_property:
        continue

    ids = results.get(
        relationship_type,
        []
    )

    print()
    print(event_property + ":")
    print(ids)

    properties_to_update[event_property] = {
        "relation": [
            {"id": cat_id}
            for cat_id in ids
        ]
    }

# ------------------------------------------------------------
# SAFETY CHECK
# ------------------------------------------------------------

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

# ------------------------------------------------------------
# UPDATE EVENT
# ------------------------------------------------------------

print()
print("=" * 70)
print("UPDATING EVENT")
print("=" * 70)

print()
print("Updating Event relations...")

notion.pages.update(
    page_id=event_id,
    properties=properties_to_update,
)

print("Event updated successfully.")

# ------------------------------------------------------------
# READ BACK FROM NOTION
# ------------------------------------------------------------

print()
print("=" * 70)
print("READ-BACK VERIFICATION")
print("=" * 70)

print()
print("Retrieving Event again from Notion...")

updated_event = notion.pages.retrieve(
    page_id=event_id
)

print("Event retrieved successfully.")

updated_properties = updated_event.get(
    "properties",
    {}
)

verification_failed = False

for relationship_type in relationship_types:

    event_property = EVENT_RELATION_PROPERTIES.get(
        relationship_type
    )

    if not event_property:
        continue

    expected_ids = results.get(
        relationship_type,
        []
    )

    property_data = updated_properties.get(
        event_property
    )

    if not property_data:

        print()
        print(event_property + ":")
        print("ERROR: Property was not returned.")

        verification_failed = True

        continue

    actual_ids = [
        item["id"]
        for item in property_data.get(
            "relation",
            []
        )
        if item.get("id")
    ]

    print()
    print(event_property + ":")
    print("Expected:")
    print(expected_ids)

    print("Stored:")
    print(actual_ids)

    if actual_ids == expected_ids:

        print("VERIFICATION: PASS")

    else:

        print("VERIFICATION: FAIL")

        verification_failed = True

# ------------------------------------------------------------
# FINAL RESULT
# ------------------------------------------------------------

print()
print("=" * 70)
print("BUILD COMPLETE")
print("=" * 70)

if verification_failed:

    print(
        "WARNING: One or more Event relations "
        "failed read-back verification."
    )

else:

    print(
        "SUCCESS: All calculated Event relations "
        "were stored correctly."
    )

print()
print("No All Cats pages were modified.")
print("=" * 70)
