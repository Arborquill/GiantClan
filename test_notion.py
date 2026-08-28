import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

EVENT_ID = "3c89cd66-e972-805a-a8ce-fef962c23d09"

notion = Client(auth=NOTION_TOKEN)


def get_plain_text(property_value):
    if not property_value:
        return ""

    property_type = property_value.get("type")

    if property_type == "title":
        items = property_value.get("title", [])
    elif property_type == "rich_text":
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


def get_page_name(page_id):
    page = notion.pages.retrieve(page_id=page_id)
    return get_page_title(page)


print("=" * 70)
print("HAWKKIT EVENT INSPECTION")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

print("Connecting to Notion...")

event = notion.pages.retrieve(page_id=EVENT_ID)

print("Connection successful.")

print()
print("=" * 70)
print("EVENT")
print("=" * 70)

print()
print("Page title:")
print(repr(get_page_title(event)))

print()
print("Event ID:")
print(EVENT_ID)

properties = event.get("properties", {})

print()
print("Property names:")
print(list(properties.keys()))

print()
print("=" * 70)
print("EVENT TEXT")
print("=" * 70)

for property_name in ["Event", "Description", "Note"]:
    if property_name in properties:
        value = get_plain_text(properties[property_name])

        print()
        print(property_name + ":")
        print(repr(value))

print()
print("=" * 70)
print("PARTICIPANTS")
print("=" * 70)

subject_ids = get_relation_ids(
    properties.get("Subject Cat")
)

related_ids = get_relation_ids(
    properties.get("Related Cats")
)

print()
print("Subject Cat IDs:")
print(subject_ids)

print()
print("Related Cats IDs:")
print(related_ids)

all_participant_ids = []

for cat_id in subject_ids:
    if cat_id not in all_participant_ids:
        all_participant_ids.append(cat_id)

for cat_id in related_ids:
    if cat_id not in all_participant_ids:
        all_participant_ids.append(cat_id)

print()
print("ALL PARTICIPANT IDs:")
print(all_participant_ids)

print()
print("Participant names:")

for cat_id in all_participant_ids:
    print(
        " -",
        get_page_name(cat_id),
        "(" + cat_id + ")"
    )

print()
print("=" * 70)
print("RELATIONSHIP PROPERTIES ON EVENT")
print("=" * 70)

relationship_properties = [
    "Cohort Cats",
    "Mate Cats",
    "Mentor Cats",
    "Apprentice Cats",
    "Sibling Cats",
    "Parent Cats",
    "Related Cats"
]

for property_name in relationship_properties:
    if property_name not in properties:
        print()
        print(property_name + ": NOT PRESENT")
        continue

    ids = get_relation_ids(properties[property_name])

    print()
    print(property_name + ":")
    print(ids)

    if ids:
        for cat_id in ids:
            print(
                " -",
                get_page_name(cat_id),
                "(" + cat_id + ")"
            )

print()
print("=" * 70)
print("MAPLEPAW CHECK")
print("=" * 70)

maplepaw_id = "3c09cd66-e972-80f9-9355-c0df84dd19ec"

print()
print("Maplepaw ID:")
print(maplepaw_id)

print()
print("Maplepaw name:")
print(get_page_name(maplepaw_id))

print()
print("Is Maplepaw in Subject Cat?")
print(maplepaw_id in subject_ids)

print()
print("Is Maplepaw in Related Cats?")
print(maplepaw_id in related_ids)

print()
print("Is Maplepaw an Event participant?")
print(maplepaw_id in all_participant_ids)

print()
print("=" * 70)
print("TEST COMPLETE")
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
print("=" * 70)
