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

NEW_EVENT_PROPERTIES = {
    "Kit": "Kit Cats",
    "Parent": "Parent Cats",
    "Sibling": "Sibling Cats",
    "Cohort": "Cohort Cats",
    "Mate": "Mate Cats",
    "Mentor": "Mentor Cats",
    "Apprentice": "Apprentice Cats",
}


def notion_request(url, method="GET", body=None):
    response = requests.request(
        method,
        url,
        headers=HEADERS,
        json=body,
    )

    if not response.ok:
        print()
        print("=" * 70)
        print("NOTION API ERROR")
        print("=" * 70)
        print("HTTP status:")
        print(response.status_code)
        print()
        print("Request URL:")
        print(url)
        print()
        print("Request method:")
        print(method)
        print()
        print("Request body:")
        print(body)
        print()
        print("Notion response:")
        print(response.text)
        print("=" * 70)
        print()
        raise SystemExit(1)

    return response.json()


def get_database_pages(database_id):
    pages = []
    cursor = None

    while True:
        body = {}

        if cursor:
            body["start_cursor"] = cursor

        data = notion_request(
            f"https://api.notion.com/v1/databases/{database_id}/query",
            method="POST",
            body=body,
        )

        pages.extend(data.get("results", []))

        if not data.get("has_more"):
            break

        cursor = data.get("next_cursor")

    return pages


def get_title(page):
    properties = page.get("properties", {})

    for prop in properties.values():
        if prop.get("type") == "title":
            title_items = prop.get("title", [])

            return "".join(
                item.get("plain_text", "")
                for item in title_items
            )

    return ""


def get_relation_ids(page, property_name):
    properties = page.get("properties", {})
    prop = properties.get(property_name)

    if not prop:
        return []

    if prop.get("type") != "relation":
        return []

    return [
        item["id"]
        for item in prop.get("relation", [])
        if item.get("id")
    ]


def get_formula_string(page, property_name):
    properties = page.get("properties", {})
    prop = properties.get(property_name)

    if not prop:
        return ""

    if prop.get("type") != "formula":
        return ""

    formula = prop.get("formula", {})

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
print("EVENT RELATIONSHIP WRITE TEST")
print("=" * 70)
print("THIS TEST WILL MODIFY ONE EVENT PAGE")
print()

print("Connecting to Notion...")

events = get_database_pages(EVENTS_DATABASE_ID)
cats = get_database_pages(CATS_DATABASE_ID)

print("Connection successful.")

print()
print("=" * 70)
print("SEARCHING FOR TARGET EVENT")
print("=" * 70)

matching_events = []

for page in events:
    if get_title(page) == TARGET_EVENT_TITLE:
        matching_events.append(page)

if len(matching_events) == 0:
    print("ERROR: Target event was not found.")
    raise SystemExit(1)

if len(matching_events) > 1:
    print("ERROR: Multiple exact event matches were found.")
    print("Count:", len(matching_events))
    raise SystemExit(1)

event = matching_events[0]
event_id = event["id"]

print("Event ID:")
print(event_id)

print()
print("Event:")
print(get_title(event))

print()
print("=" * 70)
print("CHECKING EVENT RELATION PROPERTIES")
print("=" * 70)

event_properties = event.get("properties", {})

for relationship_type, target_property in NEW_EVENT_PROPERTIES.items():
    prop = event_properties.get(target_property)

    if not prop:
        print()
        print("ERROR: Missing Event property:")
        print(target_property)
        raise SystemExit(1)

    print()
    print(target_property)
    print("Property type:", prop.get("type"))

    if prop.get("type") != "relation":
        print("ERROR: Property is not a relation.")
        raise SystemExit(1)

print()
print("All seven new Event properties are valid relation properties.")

print()
print("=" * 70)
print("DIRECT EVENT PARTICIPANTS")
print("=" * 70)

subject_ids = get_relation_ids(event, "Subject Cat")
related_ids = get_relation_ids(event, "Related Cats")

participant_ids = []

for cat_id in subject_ids + related_ids:
    if cat_id not in participant_ids:
        participant_ids.append(cat_id)

print("Subject Cat IDs:")
print(subject_ids)

print()
print("Related Cats IDs:")
print(related_ids)

print()
print("Direct participant IDs:")
print(participant_ids)

if not participant_ids:
    print()
    print("ERROR: Event has no direct participants.")
    raise SystemExit(1)

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
print("Direct participants:")

for cat_id in participant_ids:
    print(
        participant_names[cat_id],
        "->",
        cat_id,
    )

print()
print("=" * 70)
print("READING RELATIONSHIP TYPES")
print("=" * 70)

relationship_formula = get_formula_string(
    event,
    "Relationship Type",
)

print("Relationship Type:")
print(repr(relationship_formula))

relationship_types = parse_relationship_types(
    relationship_formula
)

print()
print("Detected relationships:")
print(relationship_types)

if not relationship_types:
    print()
    print("ERROR: No relationship types were detected.")
    raise SystemExit(1)

print()
print("=" * 70)
print("BUILDING EVENT RELATIONSHIPS")
print("=" * 70)

all_participant_set = set(participant_ids)

results = {}

for relationship_type in relationship_types:
    source_property = RELATIONSHIP_PROPERTIES.get(
        relationship_type
    )

    target_property = NEW_EVENT_PROPERTIES.get(
        relationship_type
    )

    print()
    print("-" * 70)
    print("RELATIONSHIP:", relationship_type)
    print("Source cat property:", source_property)
    print("Target Event property:", target_property)

    if not source_property:
        print("ERROR: No source property mapping exists.")
        raise SystemExit(1)

    if not target_property:
        print("ERROR: No target Event property mapping exists.")
        raise SystemExit(1)

    relationship_ids = set()

    for participant_id in participant_ids:
        participant = cat_by_id.get(participant_id)

        if not participant:
            print()
            print("WARNING: Participant cat was not found:")
            print(participant_id)
            continue

        participant_name = participant_names[participant_id]

        related_ids_for_cat = get_relation_ids(
            participant,
            source_property,
        )

        print()
        print(
            participant_name,
            source_property,
            ":",
            related_ids_for_cat,
        )

        for related_id in related_ids_for_cat:
            if related_id in all_participant_set:
                relationship_ids.add(related_id)

    ordered_ids = [
        cat_id
        for cat_id in participant_ids
        if cat_id in relationship_ids
    ]

    results[relationship_type] = ordered_ids

    print()
    print("FINAL IDs FOR", target_property + ":")

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
print("MAPLEPAW SAFETY CHECK")
print("=" * 70)

maplepaw_id = None

for page in cats:
    if get_title(page) == "Maplepaw":
        maplepaw_id = page["id"]
        break

if maplepaw_id is None:
    print("WARNING: Maplepaw was not found.")
else:
    print("Maplepaw ID:")
    print(maplepaw_id)

    print()
    print("Maplepaw direct participant:")
    print(maplepaw_id in all_participant_set)

    for relationship_type, ids in results.items():
        if maplepaw_id in ids:
            print()
            print("ERROR: Maplepaw would be written to:")
            print(NEW_EVENT_PROPERTIES[relationship_type])
            raise SystemExit(1)

    print()
    print("Maplepaw is excluded from every proposed Event relation.")

print()
print("=" * 70)
print("PROPOSED EVENT PROPERTY UPDATE")
print("=" * 70)

update_properties = {}

for relationship_type, target_property in NEW_EVENT_PROPERTIES.items():
    ids = results.get(
        relationship_type,
        [],
    )

    update_properties[target_property] = {
        "relation": [
            {"id": cat_id}
            for cat_id in ids
        ]
    }

    print()
    print(target_property + ":")

    if not ids:
        print("[NONE]")
    else:
        for cat_id in ids:
            print(
                "-",
                participant_names.get(
                    cat_id,
                    "[CAT NOT FOUND]",
                ),
            )

print()
print("=" * 70)
print("UPDATING EVENT")
print("=" * 70)

print()
print("Updating only the seven new Event relation properties.")
print("Existing formula properties will NOT be modified.")

updated_event = notion_request(
    f"https://api.notion.com/v1/pages/{event_id}",
    method="PATCH",
    body={
        "properties": update_properties
    },
)

print()
print("Event update successful.")

print()
print("=" * 70)
print("VERIFYING UPDATED EVENT")
print("=" * 70)

verified_properties = updated_event.get(
    "properties",
    {},
)

for relationship_type, target_property in NEW_EVENT_PROPERTIES.items():
    prop = verified_properties.get(target_property, {})

    actual_ids = [
        item["id"]
        for item in prop.get("relation", [])
        if item.get("id")
    ]

    expected_ids = results.get(
        relationship_type,
        [],
    )

    print()
    print(target_property)
    print("Expected:")
    print(expected_ids)
    print("Actual:")
    print(actual_ids)

    if actual_ids != expected_ids:
        print()
        print("ERROR: Verification failed.")
        raise SystemExit(1)

print()
print("=" * 70)
print("WRITE TEST COMPLETE")
print("=" * 70)

print()
print("The seven new Event relation properties were populated.")
print("Only direct event participants were eligible.")
print("Maplepaw was excluded because he is not a direct participant.")
print("Existing formula properties were not modified.")
print()
print("NOTION UPDATE COMPLETED SUCCESSFULLY.")
print("=" * 70) 
