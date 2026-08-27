import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

EVENTS_DATABASE_ID = "3b79cd66-e972-80d0-aa83-de1c481c6ef6"
CATS_DATABASE_ID = "9849cd66-e972-8390-b142-01cdd6b8b3a6"

notion = Client(auth=NOTION_TOKEN)


def get_data_source_id(database_id):
    database = notion.request(
        path=f"databases/{database_id}"
    )

    data_sources = database.get("data_sources", [])

    if not data_sources:
        raise RuntimeError(
            f"No data sources found for database {database_id}"
        )

    return data_sources[0]["id"]


def get_data_source(data_source_id):
    return notion.request(
        path=f"data_sources/{data_source_id}"
    )


def get_relation_ids(page, property_name):
    prop = page["properties"].get(property_name)

    if not prop or prop["type"] != "relation":
        return []

    return [
        item["id"]
        for item in prop["relation"]
    ]


def get_title(page):
    prop = page["properties"].get("Name")

    if not prop:
        return "(Unnamed)"

    if prop["type"] != "title":
        return "(Unnamed)"

    return "".join(
        item.get("plain_text", "")
        for item in prop["title"]
    ) or "(Unnamed)"


def get_all_pages(data_source_id):
    pages = []
    cursor = None

    while True:
        kwargs = {
            "data_source_id": data_source_id,
            "page_size": 100,
        }

        if cursor:
            kwargs["start_cursor"] = cursor

        response = notion.request(
            path="data_sources/query",
            method="POST",
            body=kwargs
        )

        pages.extend(response.get("results", []))

        if not response.get("has_more"):
            break

        cursor = response.get("next_cursor")

    return pages


print("=" * 70)
print("CONNECTING TO NOTION")
print("=" * 70)

print("Connection successful.")
print()


# -------------------------------------------------------------------
# GET DATA SOURCES
# -------------------------------------------------------------------

cats_data_source_id = get_data_source_id(CATS_DATABASE_ID)
events_data_source_id = get_data_source_id(EVENTS_DATABASE_ID)

print("Cats data source:", cats_data_source_id)
print("Events data source:", events_data_source_id)
print()


# -------------------------------------------------------------------
# LOAD CATS
# -------------------------------------------------------------------

print("=" * 70)
print("LOADING CATS")
print("=" * 70)

cats = get_all_pages(cats_data_source_id)

cat_lookup = {}

for cat in cats:
    cat_lookup[cat["id"]] = get_title(cat)

print(f"Loaded {len(cats)} cats.")
print()


# -------------------------------------------------------------------
# LOAD EVENTS
# -------------------------------------------------------------------

print("=" * 70)
print("LOADING EVENTS")
print("=" * 70)

events = get_all_pages(events_data_source_id)

print(f"Loaded {len(events)} events.")
print()


# -------------------------------------------------------------------
# ANALYZE EVENTS
# -------------------------------------------------------------------

print("=" * 70)
print("EVENT ANALYSIS")
print("=" * 70)

for event in events:

    event_name = get_title(event)

    subject_ids = get_relation_ids(
        event,
        "Subject Cat"
    )

    related_ids = get_relation_ids(
        event,
        "Related Cats"
    )

    participants = []

    for cat_id in subject_ids + related_ids:
        if cat_id not in participants:
            participants.append(cat_id)

    print()
    print("-" * 70)
    print(f"EVENT: {event_name}")
    print("-" * 70)

    print("Subject Cats:")

    if subject_ids:
        for cat_id in subject_ids:
            print(
                f"  - {cat_lookup.get(cat_id, '(Unknown cat)')}"
            )
    else:
        print("  (none)")

    print("Related Cats:")

    if related_ids:
        for cat_id in related_ids:
            print(
                f"  - {cat_lookup.get(cat_id, '(Unknown cat)')}"
            )
    else:
        print("  (none)")

    print("All Participants:")

    if participants:
        for cat_id in participants:
            print(
                f"  - {cat_lookup.get(cat_id, '(Unknown cat)')}"
            )
    else:
        print("  (none)")

    # ---------------------------------------------------------------
    # Show the events that would naturally belong to each participant
    # ---------------------------------------------------------------

    print()
    print("Would appear on cat pages:")

    if participants:
        for cat_id in participants:
            print(
                f"  - {cat_lookup.get(cat_id, '(Unknown cat)')}"
            )
    else:
        print("  (none)")


# -------------------------------------------------------------------
# SPECIAL CASES
# -------------------------------------------------------------------

print()
print("=" * 70)
print("MULTIPLE-SUBJECT EVENTS")
print("=" * 70)

multiple_subject_events = 0

for event in events:

    subject_ids = get_relation_ids(
        event,
        "Subject Cat"
    )

    if len(subject_ids) > 1:

        multiple_subject_events += 1

        print()
        print(f"EVENT: {get_title(event)}")
        print("Subjects:")

        for cat_id in subject_ids:
            print(
                f"  - {cat_lookup.get(cat_id, '(Unknown cat)')}"
            )

        related_ids = get_relation_ids(
            event,
            "Related Cats"
        )

        if related_ids:
            print("Related cats:")

            for cat_id in related_ids:
                print(
                    f"  - {cat_lookup.get(cat_id, '(Unknown cat)')}"
                )

if multiple_subject_events == 0:
    print("No events currently have multiple Subject Cats.")

print()
print("=" * 70)
print("READ-ONLY TEST COMPLETE")
print("=" * 70)
print()
print("Nothing in Notion was modified.")
