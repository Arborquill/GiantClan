import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

EVENTS_DATA_SOURCE_ID = "cf09cd66-e972-8293-8c29-073c01330f5b"

TARGET_EVENT = (
    "While out on a secret date, Cliffshock and Blackchirp find an orphaned "
    "litter of kits in the wreckage of a dead monster. It isn't the direction "
    "they expected their lives to be tugged, but their hearts brim with love "
    "for them. Their gentle touch and affectionate purrs are the kits’ home now."
)

notion = Client(auth=NOTION_TOKEN)


def get_plain_text(property_value):
    if not property_value:
        return ""

    if property_value.get("type") == "title":
        items = property_value.get("title", [])
    elif property_value.get("type") == "rich_text":
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


def get_page_title(page):
    for prop in page.get("properties", {}).values():
        if prop.get("type") == "title":
            return get_plain_text(prop)

    return "(unnamed)"


def get_page(page_id):
    return notion.pages.retrieve(page_id=page_id)


def find_event():
    response = notion.data_sources.query(
        data_source_id=EVENTS_DATA_SOURCE_ID
    )

    while True:
        for page in response.get("results", []):
            if get_page_title(page) == TARGET_EVENT:
                return page

        if not response.get("has_more"):
            break

        response = notion.data_sources.query(
            data_source_id=EVENTS_DATA_SOURCE_ID,
            start_cursor=response["next_cursor"]
        )

    return None


print("=" * 70)
print("LITTER EVENT PARTICIPATION TEST")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

print("Connecting to Notion...")
event = find_event()

if event is None:
    print()
    print("ERROR: Target event was not found.")
    print()
    print("Target event:")
    print(TARGET_EVENT)
    raise SystemExit(1)

event_id = event["id"]
properties = event["properties"]

print()
print("Event:")
print(get_page_title(event))
print()
print("ID:")
print(event_id)

subject_ids = get_relation_ids(
    properties.get("Subject Cat")
)

related_ids = get_relation_ids(
    properties.get("Related Cats")
)

participant_ids = []

for cat_id in subject_ids:
    if cat_id not in participant_ids:
        participant_ids.append(cat_id)

for cat_id in related_ids:
    if cat_id not in participant_ids:
        participant_ids.append(cat_id)

participants = {}

print()
print("=" * 70)
print("EVENT PARTICIPANTS")
print("=" * 70)

print()
print("SUBJECT CATS")
print("-" * 70)

for cat_id in subject_ids:
    cat_page = get_page(cat_id)
    cat_name = get_page_title(cat_page)

    participants[cat_id] = {
        "name": cat_name,
        "page": cat_page
    }

    print(cat_name)
    print("ID:", cat_id)
    print()

print("RELATED CATS")
print("-" * 70)

for cat_id in related_ids:
    cat_page = get_page(cat_id)
    cat_name = get_page_title(cat_page)

    if cat_id not in participants:
        participants[cat_id] = {
            "name": cat_name,
            "page": cat_page
        }

    print(cat_name)
    print("ID:", cat_id)
    print()

print()
print("TOTAL PARTICIPANTS:", len(participant_ids))

print()
print("=" * 70)
print("MAPLEPAW PARTICIPATION CHECK")
print("=" * 70)

maplepaw_id = None

for cat_id, data in participants.items():
    if data["name"] == "Maplepaw":
        maplepaw_id = cat_id
        break

if maplepaw_id is None:
    print()
    print("Maplepaw is NOT an Event participant.")
    print("EXPECTED: YES")
else:
    print()
    print("Maplepaw IS an Event participant.")
    print("WARNING: This is not the expected result.")
    print("Maplepaw ID:", maplepaw_id)

print()
print("=" * 70)
print("SIBLING RELATIONSHIP ANALYSIS")
print("=" * 70)

print()
print(
    "A cat can be included in the Event's Sibling Cats property only if:"
)
print(
    "1. The cat participates in this Event."
)
print(
    "2. Another participating cat is in that cat's Sibling Cats relation."
)

qualifying_ids = []

for cat_id in participant_ids:
    data = participants[cat_id]
    cat_name = data["name"]
    cat_page = data["page"]

    sibling_ids = get_relation_ids(
        cat_page.get("properties", {}).get("Sibling Cats")
    )

    print()
    print("-" * 70)
    print(cat_name)
    print("ID:", cat_id)
    print("Existing Sibling IDs:", sibling_ids)

    qualifying_partners = []

    for other_id in participant_ids:
        if other_id == cat_id:
            continue

        if other_id in sibling_ids:
            other_name = participants[other_id]["name"]

            qualifying_partners.append(other_name)

            if cat_id not in qualifying_ids:
                qualifying_ids.append(cat_id)

    if qualifying_partners:
        print()
        print("QUALIFIES BECAUSE PARTICIPATING SIBLING(S):")

        for partner in qualifying_partners:
            print(" -", partner)

        print()
        print("RESULT: QUALIFIES")
    else:
        print()
        print("RESULT: Does NOT qualify")

print()
print("=" * 70)
print("PROPOSED EVENT PROPERTY")
print("=" * 70)

print()
print("Sibling Cats would contain:")

for cat_id in qualifying_ids:
    print(
        " -",
        participants[cat_id]["name"],
        "(" + cat_id + ")"
    )

if not qualifying_ids:
    print(" - None")

print()
print("=" * 70)
print("MAPLEPAW FALSE-POSITIVE TEST")
print("=" * 70)

print()

if maplepaw_id is None:
    if maplepaw_id in qualifying_ids:
        print("RESULT: FAILURE")
        print(
            "Maplepaw was incorrectly included despite not participating."
        )
    else:
        print("RESULT: SUCCESS")
        print(
            "Maplepaw is not a participant and is not included "
            "in the Event's Sibling Cats."
        )
else:
    print("RESULT: WARNING")
    print(
        "Maplepaw is actually participating in this Event, so "
        "the exclusion test cannot be used."
    )

print()
print("=" * 70)
print("FINAL LOGIC CHECK")
print("=" * 70)
print()
print(
    "This test does NOT follow sibling relationships outward."
)
print(
    "A non-participating cat cannot be pulled into an Event merely "
    "because it is related to a participating cat."
)
print()
print(
    "For Maplepaw, the expected result is:"
)
print(
    "  Participating in Event: NO"
)
print(
    "  Included in Event Sibling Cats: NO"
)

print()
print("=" * 70)
print("TEST COMPLETE")
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
print("=" * 70)
