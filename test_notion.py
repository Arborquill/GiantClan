import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

# This is the actual Events data source ID established in our earlier tests.
EVENTS_DATA_SOURCE_ID = "cf09cd66-e972-8293-8c29-073c01330f5b"

SEARCH_TEXT = "orphaned litter"

notion = Client(auth=NOTION_TOKEN)


def get_plain_text(prop):
    if not prop:
        return ""

    if prop.get("type") == "title":
        items = prop.get("title", [])
    elif prop.get("type") == "rich_text":
        items = prop.get("rich_text", [])
    else:
        return ""

    return "".join(
        item.get("plain_text", "")
        for item in items
    )


def get_relation_ids(prop):
    if not prop:
        return []

    if prop.get("type") != "relation":
        return []

    return [
        item["id"]
        for item in prop.get("relation", [])
    ]


def get_page_title(page):
    for prop in page.get("properties", {}).values():
        if prop.get("type") == "title":
            return get_plain_text(prop)

    return "(unnamed)"


def get_event_text(page):
    properties = page.get("properties", {})

    for property_name in [
        "Event",
        "Description",
        "Note",
    ]:
        if property_name in properties:
            text = get_plain_text(properties[property_name])

            if text:
                return text

    return ""


def get_cat_name(cat_id):
    page = notion.pages.retrieve(page_id=cat_id)
    return get_page_title(page)


print("=" * 70)
print("SIBLING EVENT PARTICIPATION TEST")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

print("Connecting to Notion...")

response = notion.data_sources.query(
    data_source_id=EVENTS_DATA_SOURCE_ID
)

events = []

while True:
    events.extend(response.get("results", []))

    if not response.get("has_more"):
        break

    response = notion.data_sources.query(
        data_source_id=EVENTS_DATA_SOURCE_ID,
        start_cursor=response["next_cursor"]
    )

print("Connection successful.")
print()
print("Events retrieved:", len(events))

# ----------------------------------------------------------------------
# FIND THE LITTER EVENT
# ----------------------------------------------------------------------

matches = []

for event in events:
    event_text = get_event_text(event)

    if SEARCH_TEXT.lower() in event_text.lower():
        matches.append(event)

print()
print("=" * 70)
print("TARGET EVENT SEARCH")
print("=" * 70)

print()
print("Search text:")
print(repr(SEARCH_TEXT))

print()
print("Matches found:", len(matches))

if not matches:
    print()
    print("ERROR: No event containing the search text was found.")
    print()
    print("Available event text:")
    
    for event in events:
        print()
        print("ID:", event["id"])
        print("Title:", repr(get_page_title(event)))
        print("Event:", repr(get_event_text(event)))

    raise SystemExit(1)

if len(matches) > 1:
    print()
    print("WARNING: Multiple matching events found.")

    for number, event in enumerate(matches, start=1):
        print()
        print("MATCH", number)
        print("ID:", event["id"])
        print("Event:", repr(get_event_text(event)))

    raise SystemExit(1)

event = matches[0]
event_id = event["id"]
properties = event.get("properties", {})

print()
print("Target event found.")

print()
print("Event ID:")
print(event_id)

print()
print("Event:")
print(get_event_text(event))

# ----------------------------------------------------------------------
# GET PARTICIPANTS
# ----------------------------------------------------------------------

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

print()
print("=" * 70)
print("EVENT PARTICIPANTS")
print("=" * 70)

print()
print("SUBJECT CATS")

for cat_id in subject_ids:
    print(
        get_cat_name(cat_id),
        "(" + cat_id + ")"
    )

print()
print("RELATED CATS")

for cat_id in related_ids:
    print(
        get_cat_name(cat_id),
        "(" + cat_id + ")"
    )

print()
print("ALL PARTICIPANTS")

participant_names = {}

for cat_id in participant_ids:
    name = get_cat_name(cat_id)
    participant_names[cat_id] = name

    print(
        name,
        "(" + cat_id + ")"
    )

# ----------------------------------------------------------------------
# CHECK SIBLING RELATIONS
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("SIBLING PROCESSING")
print("=" * 70)

print()
print(
    "A sibling relationship qualifies only when BOTH cats "
    "are participants in this event."
)

qualifying_pairs = []
qualified_cat_ids = []

for cat_id in participant_ids:

    cat_page = notion.pages.retrieve(page_id=cat_id)
    cat_properties = cat_page.get("properties", {})

    sibling_property = cat_properties.get("Siblings")

    sibling_ids = get_relation_ids(sibling_property)

    print()
    print(
        participant_names[cat_id],
        "(" + cat_id + ")"
    )

    print("Existing Sibling IDs:")
    print(sibling_ids)

    found_pair = False

    for sibling_id in sibling_ids:

        if sibling_id not in participant_ids:
            continue

        sibling_name = participant_names.get(sibling_id)

        if sibling_name is None:
            sibling_name = get_cat_name(sibling_id)

        pair = tuple(sorted([cat_id, sibling_id]))

        if pair not in qualifying_pairs:
            qualifying_pairs.append(pair)

        if cat_id not in qualified_cat_ids:
            qualified_cat_ids.append(cat_id)

        if sibling_id not in qualified_cat_ids:
            qualified_cat_ids.append(sibling_id)

        print()
        print(
            "QUALIFYING SIBLING PAIR:",
            participant_names[cat_id],
            "<->",
            sibling_name
        )

        found_pair = True

    if found_pair:
        print()
        print("RESULT: qualifies.")
    else:
        print()
        print("RESULT: does NOT qualify.")

# ----------------------------------------------------------------------
# SHOW PROPOSED EVENT PROPERTY
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("PROPOSED EVENT PROPERTY")
print("=" * 70)

print()
print("Sibling Cats would contain:")

if not qualified_cat_ids:
    print("  - Nothing")

else:
    for cat_id in qualified_cat_ids:
        print(
            "  -",
            participant_names[cat_id],
            "(" + cat_id + ")"
        )

# ----------------------------------------------------------------------
# EXPLICIT MAPLEPAW CHECK
# ----------------------------------------------------------------------

MAPLEPAW_ID = "3c09cd66-e972-80f9-9355-c0df84dd19ec"

print()
print("=" * 70)
print("MAPLEPAW CHECK")
print("=" * 70)

print()
print("Maplepaw:")
print(MAPLEPAW_ID)

print()
print("Is Maplepaw an event participant?")
print(MAPLEPAW_ID in participant_ids)

print()
print("Would Maplepaw be added to Sibling Cats?")
print(MAPLEPAW_ID in qualified_cat_ids)

if MAPLEPAW_ID not in participant_ids and MAPLEPAW_ID not in qualified_cat_ids:
    print()
    print("RESULT: CORRECT.")
    print(
        "Maplepaw is a sibling of participating cats but is not "
        "participating in this event, so he is excluded."
    )

# ----------------------------------------------------------------------
# HYPOTHETICAL PAYLOAD
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("HYPOTHETICAL UPDATE PAYLOAD")
print("=" * 70)

payload = {
    "properties": {
        "Sibling Cats": {
            "relation": [
                {"id": cat_id}
                for cat_id in qualified_cat_ids
            ]
        }
    }
}

print()
print("This payload is NOT being sent to Notion.")
print()
print(payload)

print()
print("=" * 70)
print("TEST COMPLETE")
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
print("=" * 70)
