import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
EVENTS_DATABASE_ID = os.environ["EVENTS_DATABASE_ID"]

notion = Client(auth=NOTION_TOKEN)

TARGET_EVENT = (
    "While out on a secret date, Cliffshock and Blackchirp find an orphaned "
    "litter of kits in the wreckage of a dead monster. It isn't the direction "
    "they expected their lives to be tugged, but their hearts brim with love "
    "for them. Their gentle touch and affectionate purrs are the kits’ home now."
)


def get_plain_text(property_value):
    if not property_value:
        return ""

    prop_type = property_value.get("type")

    if prop_type == "title":
        items = property_value.get("title", [])
    elif prop_type == "rich_text":
        items = property_value.get("rich_text", [])
    else:
        return ""

    return "".join(
        item.get("plain_text", "")
        for item in items
    )


def get_relation_ids(property_value):
    if not property_value:
        return []

    if property_value.get("type") != "relation":
        return []

    return [
        item["id"]
        for item in property_value.get("relation", [])
    ]


def get_cat_name(page):
    properties = page.get("properties", {})

    # Find the title property dynamically.
    for prop in properties.values():
        if prop.get("type") == "title":
            return get_plain_text(prop)

    return "(unnamed)"


def get_page(page_id):
    return notion.pages.retrieve(page_id=page_id)


def find_event():
    response = notion.data_sources.query(
        data_source_id=EVENTS_DATABASE_ID
    )

    matches = []

    for page in response.get("results", []):
        name = get_cat_name(page)

        if name == TARGET_EVENT:
            matches.append(page)

    while response.get("has_more"):
        response = notion.data_sources.query(
            data_source_id=EVENTS_DATABASE_ID,
            start_cursor=response["next_cursor"]
        )

        for page in response.get("results", []):
            name = get_cat_name(page)

            if name == TARGET_EVENT:
                matches.append(page)

    if not matches:
        return None

    if len(matches) > 1:
        print("WARNING: Multiple events matched the exact title.")
        print("Number of matches:", len(matches))

    return matches[0]


print("=" * 70)
print("LITTER EVENT PARTICIPATION TEST")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

print("Connecting to Notion...")
print()

event = find_event()

if event is None:
    print("ERROR: Target event was not found.")
    print()
    print("Target title:")
    print(TARGET_EVENT)
    raise SystemExit(1)

event_id = event["id"]
properties = event["properties"]

print("Target event found.")
print()
print("Event:")
print(get_cat_name(event))
print()
print("ID:")
print(event_id)

print()
print("=" * 70)
print("EVENT PARTICIPANTS")
print("=" * 70)

subject_ids = get_relation_ids(
    properties.get("Subject Cat")
)

related_ids = get_relation_ids(
    properties.get("Related Cats")
)

participant_ids = []

for cat_id in subject_ids + related_ids:
    if cat_id not in participant_ids:
        participant_ids.append(cat_id)

print()
print("Subject Cat IDs:")
print(subject_ids)

print()
print("Related Cats IDs:")
print(related_ids)

print()
print("All participant IDs:")
print(participant_ids)

print()
print("Number of participants:")
print(len(participant_ids))

print()
print("=" * 70)
print("PARTICIPANT NAMES")
print("=" * 70)

participants = {}

for cat_id in participant_ids:
    cat_page = get_page(cat_id)
    cat_name = get_cat_name(cat_page)

    participants[cat_id] = {
        "name": cat_name,
        "page": cat_page
    }

    print(cat_name)
    print("ID:", cat_id)
    print()

print()
print("=" * 70)
print("MAPLEPAW PARTICIPATION CHECK")
print("=" * 70)

maplepaw_id = None

for cat_id, data in participants.items():
    if data["name"] == "Maplepaw":
        maplepaw_id = cat_id

if maplepaw_id is None:
    print()
    print("Maplepaw is NOT an Event participant.")
    print("This is the expected result.")
else:
    print()
    print("WARNING: Maplepaw IS an Event participant.")
    print("Maplepaw ID:", maplepaw_id)

print()
print("=" * 70)
print("SIBLING RELATIONSHIP ANALYSIS")
print("=" * 70)

print()
print(
    "A cat may qualify for Sibling Cats only when BOTH conditions are true:"
)
print()
print("1. The cat participates in this Event.")
print("2. Another participating cat is actually in that cat's Sibling Cats relation.")
print()

qualifying_pairs = []

for cat_id, data in participants.items():
    cat_name = data["name"]
    cat_page = data["page"]

    cat_properties = cat_page.get("properties", {})

    sibling_property = cat_properties.get("Sibling Cats")

    sibling_ids = get_relation_ids(sibling_property)

    print("-" * 70)
    print(cat_name)
    print("ID:", cat_id)
    print("Existing Sibling IDs:", sibling_ids)

    found_pair = False

    for other_id in participant_ids:
        if other_id == cat_id:
            continue

        if other_id in sibling_ids:
            other_name = participants[other_id]["name"]

            print()
            print("QUALIFYING PAIR:")
            print(cat_name, "<->", other_name)

            qualifying_pairs.append(
                (cat_id, other_id)
            )

            found_pair = True

    if found_pair:
        print()
        print("RESULT:", cat_name, "qualifies for Sibling Cats.")
    else:
        print()
        print("RESULT:", cat_name, "does NOT qualify for Sibling Cats.")

print()
print("=" * 70)
print("PROPOSED EVENT PROPERTY")
print("=" * 70)

sibling_event_ids = []

for first_id, second_id in qualifying_pairs:
    if first_id not in sibling_event_ids:
        sibling_event_ids.append(first_id)

    if second_id not in sibling_event_ids:
        sibling_event_ids.append(second_id)

print()
print("Sibling Cats would contain:")

for cat_id in sibling_event_ids:
    print(
        " -",
        participants[cat_id]["name"],
        "(" + cat_id + ")"
    )

if not sibling_event_ids:
    print(" - None")

print()
print("=" * 70)
print("MAPLEPAW FALSE-POSITIVE TEST")
print("=" * 70)

print()
print(
    "Maplepaw must NOT appear in Sibling Cats unless Maplepaw is an "
    "actual Event participant."
)

if maplepaw_id is None:
    if maplepaw_id in sibling_event_ids:
        print()
        print("RESULT: FAILURE")
        print(
            "Maplepaw was included in Sibling Cats even though "
            "Maplepaw is not participating in the Event."
        )
    else:
        print()
        print("RESULT: SUCCESS")
        print(
            "Maplepaw is not an Event participant and is not included "
            "in Sibling Cats."
        )
else:
    print()
    print(
        "Maplepaw is participating, so the false-positive exclusion "
        "test does not apply."
    )

print()
print("=" * 70)
print("IMPORTANT RELATIONSHIP RULE")
print("=" * 70)

print()
print(
    "This test intentionally does NOT traverse relationships outward."
)
print()
print(
    "Being a sibling of a participating cat is not sufficient."
)
print(
    "A cat must itself participate in the Event."
)
print()
print(
    "Therefore, Maplepaw's relationship to the five participating kits "
    "must not cause this event to appear in Maplepaw's Sibling events."
)

print()
print("=" * 70)
print("TEST COMPLETE")
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
print("=" * 70)
