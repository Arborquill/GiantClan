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


def get_event_name(page):
    properties = page.get("properties", {})

    event_property = properties.get("Event")

    if not event_property:
        return "(no Event property)"

    title_data = event_property.get("title", [])

    if title_data:
        return title_data[0].get(
            "plain_text",
            "(unnamed)"
        )

    rich_text_data = event_property.get("rich_text", [])

    if rich_text_data:
        return rich_text_data[0].get(
            "plain_text",
            "(unnamed)"
        )

    return "(unnamed)"


def get_formula_value(page):
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


def determine_actions(relationships):
    actions = []

    if "Cohort" in relationships:
        actions.append(
            "Would process the Cohort relationship."
        )

    if "Mate" in relationships:
        actions.append(
            "Would process the Mate relationship."
        )

    if "Mentor" in relationships:
        actions.append(
            "Would process the Mentor relationship."
        )

    if "Apprentice" in relationships:
        actions.append(
            "Would process the Apprentice relationship."
        )

    if not actions:
        actions.append(
            "No recognized relationship action."
        )

    return actions


def main():
    print("Connecting to Notion...")
    print()

    events = get_events()

    print("Connection successful.")
    print()
    print("=" * 70)
    print("RELATIONSHIP DECISION TEST")
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

        try:
            event_name = get_event_name(event)
            event_id = event.get("id")

            print(f"Event: {event_name}")
            print(f"ID: {event_id}")
            print()

            formula_value = get_formula_value(event)

            print("Formula value:")
            print(repr(formula_value))
            print()

            relationships = split_relationship_types(
                formula_value
            )

            print("Detected relationships:")
            print(repr(relationships))
            print()

            actions = determine_actions(
                relationships
            )

            print("WOULD TAKE THESE ACTIONS:")

            for action in actions:
                print(f"  - {action}")

            print()

            print("RESULT: SUCCESS")
            successful += 1

        except Exception as error:
            print()
            print("RESULT: FAILED")
            print(
                f"Error: {type(error).__name__}: {error}"
            )
            failed += 1

        print()

    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Successful decisions: {successful}")
    print(f"Empty/unknown:         {empty}")
    print(f"Failed:                {failed}")
    print()

    if failed == 0:
        print("RELATIONSHIP DECISION TEST PASSED.")
    else:
        print("RELATIONSHIP DECISION TEST HAD FAILURES.")

    print()
    print("=" * 70)
    print("TEST COMPLETE")
    print("No Notion pages or properties were modified.")
    print("=" * 70)


if __name__ == "__main__":
    notion = Client(auth=NOTION_TOKEN)
    main()