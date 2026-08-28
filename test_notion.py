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

    name_property = properties.get("Name")

    if not name_property:
        name_property = properties.get("Event")

    if not name_property:
        return "(no name property)"

    title_data = name_property.get("title", [])

    if title_data:
        return title_data[0].get(
            "plain_text",
            "(unnamed)"
        )

    rich_text_data = name_property.get("rich_text", [])

    if rich_text_data:
        return rich_text_data[0].get(
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


def main():
    print("Connecting to Notion...")
    print()

    events = get_events()

    print("Connection successful.")
    print()
    print("=" * 70)
    print("PYTHON FORMULA VALUE TEST")
    print("=" * 70)
    print("READ ONLY - NOTHING WILL BE CHANGED")
    print()
    print(f"Events retrieved: {len(events)}")
    print()

    successful = 0
    empty = 0
    failed = 0

    for number, event in enumerate(events, start=1):
        event_name = get_page_name(event)
        event_id = event.get("id")

        print("-" * 70)
        print(f"EVENT {number}")
        print("-" * 70)
        print(f"Name: {event_name}")
        print(f"ID: {event_id}")

        try:
            relationship_type = get_relationship_type_value(
                event
            )

            print()
            print("Relationship Type returned to Python:")
            print(repr(relationship_type))

            if relationship_type is None:
                print()
                print("RESULT: EMPTY OR NOT A STRING FORMULA")
                empty += 1
            else:
                print()
                print("RESULT: SUCCESS")
                print(f"Value: {relationship_type}")
                print(
                    f"Python type: {type(relationship_type).__name__}"
                )
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
    print(f"Successful formula values: {successful}")
    print(f"Empty/non-string values:   {empty}")
    print(f"Failed retrievals:         {failed}")
    print()

    if failed == 0 and successful > 0:
        print("PYTHON CAN RELIABLY RETRIEVE THE FORMULA STRING VALUE.")
    elif failed == 0 and successful == 0:
        print("No usable formula string values were retrieved.")
    else:
        print("Some formula value retrievals failed.")

    print()
    print("=" * 70)
    print("TEST COMPLETE")
    print("No Notion pages or properties were modified.")
    print("=" * 70)


if __name__ == "__main__":
    notion = Client(auth=NOTION_TOKEN)
    main()
