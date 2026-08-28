from notion_client import Client
import os


NOTION_TOKEN = os.environ["NOTION_TOKEN"]
HISTORICAL_EVENTS_DATA_SOURCE_ID = "3b79cd66-e972-8014-9954-000b6da417a8"


def get_events():
    response = notion.request(
        path=f"data_sources/{HISTORICAL_EVENTS_DATA_SOURCE_ID}/query",
        method="POST",
        body={
            "page_size": 10
        }
    )

    return response.get("results", [])


def get_page_name(page):
    properties = page.get("properties", {})

    name_property = properties.get("Event")

    if not name_property:
        return "(no Event property)"

    title_data = name_property.get("title", [])

    if title_data:
        return title_data[0].get(
            "plain_text",
            "(unnamed)"
        )

    return "(unnamed)"


def get_relationship_type_value(page):
    properties = page.get("properties", {})

    relationship_property = properties.get(
        "Relationship Type"
    )

    if not relationship_property:
        return None

    if relationship_property.get("type") != "formula":
        return None

    formula = relationship_property.get("formula", {})

    if formula.get("type") != "string":
        return None

    return formula.get("string")


def split_relationship_types(value):
    if not value:
        return []

    return [
        relationship.strip()
        for relationship in value.split("·")
        if relationship.strip()
    ]


def main():
    print("Connecting to Notion...")
    print()

    events = get_events()

    print("Connection successful.")
    print()
    print("=" * 70)
    print("RELATIONSHIP TYPE PARSING TEST")
    print("=" * 70)
    print("READ ONLY - NOTHING WILL BE CHANGED")
    print()
    print(f"Events retrieved: {len(events)}")
    print()

    successful = 0
    empty = 0
    failed = 0

    for number, event in enumerate(events, start=1):
        print("-" * 70)
        print(f"EVENT {number}")
        print("-" * 70)

        event_name = get_page_name(event)
        event_id = event.get("id")

        print(f"Name: {event_name}")
        print(f"ID: {event_id}")
        print()

        try:
            formula_value = get_relationship_type_value(event)

            print("Formula value:")
            print(repr(formula_value))
            print()

            if not formula_value:
                print("Parsed relationships:")
                print([])
                print()
                print("RESULT: EMPTY")
                empty += 1
                continue

            relationships = split_relationship_types(
                formula_value
            )

            print("Parsed relationships:")
            print(repr(relationships))
            print()

            print("Individual relationship checks:")

            for relationship in relationships:
                print(f"  - {relationship}")

            print()
            print("RESULT: SUCCESS")
            successful += 1

        except Exception as error:
            print()
            print("RESULT: FAILED")
            print(f"Error: {type(error).__name__}: {error}")
            failed += 1

        print()

    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Successfully parsed: {successful}")
    print(f"Empty values:        {empty}")
    print(f"Failed:              {failed}")
    print()

    if failed == 0:
        print("RELATIONSHIP TYPE PARSING TEST PASSED.")
    else:
        print("RELATIONSHIP TYPE PARSING TEST HAD FAILURES.")

    print()
    print("=" * 70)
    print("TEST COMPLETE")
    print("No Notion pages or properties were modified.")
    print("=" * 70)


if __name__ == "__main__":
    notion = Client(auth=NOTION_TOKEN)
    main()
