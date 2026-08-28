from notion_client import Client
import os


NOTION_TOKEN = os.environ["NOTION_TOKEN"]
HISTORICAL_EVENTS_DATA_SOURCE_ID = "3b79cd66-e972-8014-9954-000b6da417a8"


def get_page(page_id):
    return notion.request(
        path=f"pages/{page_id}",
        method="GET"
    )


def get_first_event():
    response = notion.request(
        path=f"data_sources/{HISTORICAL_EVENTS_DATA_SOURCE_ID}/query",
        method="POST",
        body={
            "page_size": 1
        }
    )

    if not response.get("results"):
        print("No events were returned.")
        return None

    return response["results"][0]


def get_relation_ids(properties, property_name):
    prop = properties.get(property_name)

    if not prop:
        return []

    if prop.get("type") != "relation":
        return []

    return [
        item["id"]
        for item in prop.get("relation", [])
    ]


def get_page_name(page):
    properties = page.get("properties", {})
    name_property = properties.get("Name") or properties.get("Event")

    if not name_property:
        return "(no name property)"

    title_data = name_property.get("title", [])

    if title_data:
        return title_data[0].get("plain_text", "(unnamed)")

    rich_text_data = name_property.get("rich_text", [])

    if rich_text_data:
        return rich_text_data[0].get("plain_text", "(unnamed)")

    return "(unnamed)"


def inspect_relationship_type(event):
    print("=" * 70)
    print("RELATIONSHIP TYPE TEST")
    print("=" * 70)
    print("READ ONLY - NOTHING WILL BE CHANGED")
    print()

    event_id = event["id"]
    event_name = get_page_name(event)

    print("Event:")
    print(event_name)
    print()

    properties = event["properties"]

    subject_ids = get_relation_ids(
        properties,
        "Subject Cat"
    )

    related_ids = get_relation_ids(
        properties,
        "Related Cats"
    )

    print("Subject Cat IDs:")
    print(subject_ids)
    print()

    print("Related Cats IDs:")
    print(related_ids)
    print()

    print("-" * 70)
    print("SUBJECT CATS")
    print("-" * 70)

    for i, cat_id in enumerate(subject_ids, start=1):
        cat = get_page(cat_id)
        print(f"Subject Cat {i}: {get_page_name(cat)}")
        print(f"ID: {cat_id}")
        print()

    print("-" * 70)
    print("RELATED CATS")
    print("-" * 70)

    for i, cat_id in enumerate(related_ids, start=1):
        cat = get_page(cat_id)
        print(f"Related Cat {i}: {get_page_name(cat)}")
        print(f"ID: {cat_id}")
        print()

    relationship_property = properties.get("Relationship Type")

    print("-" * 70)
    print("RELATIONSHIP TYPE FORMULA RESULT")
    print("-" * 70)

    if relationship_property:
        print(relationship_property)
    else:
        print("Relationship Type property was not found.")

    print()
    print("=" * 70)
    print("TEST COMPLETE")
    print("No Notion pages or properties were modified.")
    print("=" * 70)


print("Connecting to Notion...")

notion = Client(auth=NOTION_TOKEN)

print("Connection successful.")
print()

event = get_first_event()

if event:
    inspect_relationship_type(event)