import os
from notion_client import Client


NOTION_TOKEN = os.environ["NOTION_TOKEN"]

TEST_EVENT_ID = "3c99cd66-e972-80fc-a803-de69fe8bd6de"


def get_plain_text(property_data):
    if not property_data:
        return ""

    items = (
        property_data.get("title")
        or property_data.get("rich_text")
        or []
    )

    return "".join(
        item.get("plain_text", "")
        for item in items
    )


def get_relation_ids(property_data):
    if not property_data:
        return []

    return [
        item["id"]
        for item in property_data.get("relation", [])
    ]


def get_cat_name(notion, cat_id):
    page = notion.pages.retrieve(page_id=cat_id)

    for property_data in page.get("properties", {}).values():
        if property_data.get("type") == "title":
            return get_plain_text(property_data)

    return "(Unnamed cat)"


def get_relationship_formula(event):
    property_data = event["properties"].get("Relationship Type")

    if not property_data:
        return ""

    formula = property_data.get("formula", {})

    return formula.get("string") or ""


def parse_relationships(formula_value):
    if not formula_value:
        return []

    return [
        relationship.strip()
        for relationship in formula_value.split("·")
        if relationship.strip()
    ]


def main():
    notion = Client(auth=NOTION_TOKEN)

    print("Connecting to Notion...")
    notion.users.me()
    print("Connection successful.")
    print()

    print("=" * 70)
    print("COHORT PROCESSING TEST")
    print("=" * 70)
    print("READ ONLY - NOTHING WILL BE CHANGED")
    print()

    # ---------------------------------------------------------------
    # Retrieve the exact event used by the previous successful tests
    # ---------------------------------------------------------------

    event = notion.pages.retrieve(
        page_id=TEST_EVENT_ID
    )

    properties = event.get("properties", {})

    event_text = get_plain_text(
        properties.get("Event")
    )

    print("Event:")
    print(event_text)
    print("ID:")
    print(TEST_EVENT_ID)
    print()

    # ---------------------------------------------------------------
    # Relationship Type
    # ---------------------------------------------------------------

    formula_value = get_relationship_formula(event)

    print("Formula value:")
    print(repr(formula_value))
    print()

    relationships = parse_relationships(formula_value)

    print("Detected relationships:")
    print(relationships)
    print()

    # ---------------------------------------------------------------
    # Subject Cats
    # ---------------------------------------------------------------

    subject_ids = get_relation_ids(
        properties.get("Subject Cat")
    )

    print("-" * 70)
    print("SUBJECT CATS")
    print("-" * 70)

    subject_cats = []

    for cat_id in subject_ids:
        cat_name = get_cat_name(notion, cat_id)

        subject_cats.append({
            "id": cat_id,
            "name": cat_name,
        })

        print(f"{cat_name}")
        print(f"ID: {cat_id}")
        print()

    # ---------------------------------------------------------------
    # Related Cats
    # ---------------------------------------------------------------

    related_ids = get_relation_ids(
        properties.get("Related Cats")
    )

    print("-" * 70)
    print("RELATED CATS")
    print("-" * 70)

    related_cats = []

    for cat_id in related_ids:
        cat_name = get_cat_name(notion, cat_id)

        related_cats.append({
            "id": cat_id,
            "name": cat_name,
        })

        print(f"{cat_name}")
        print(f"ID: {cat_id}")
        print()

    # ---------------------------------------------------------------
    # Cohort detection
    # ---------------------------------------------------------------

    print("-" * 70)
    print("COHORT PROCESSING")
    print("-" * 70)

    if "Cohort" not in relationships:
        print("ERROR: Cohort was not detected.")
        print()
        print("Expected Relationship Type to contain:")
        print("Cohort")
        print()
        print("Actual formula value:")
        print(repr(formula_value))
        return

    print("Cohort relationship detected.")
    print()

    # ---------------------------------------------------------------
    # Simulate Cohort processing
    # ---------------------------------------------------------------

    print("SUBJECT -> RELATED PAIRS")
    print("-" * 70)

    if not subject_cats:
        print("No Subject Cats found.")
    elif not related_cats:
        print("No Related Cats found.")
    else:
        for subject in subject_cats:
            for related in related_cats:
                print(
                    f"{subject['name']} "
                    f"<-> "
                    f"{related['name']}"
                )

    print()

    # ---------------------------------------------------------------
    # Explicit summary of what would happen
    # ---------------------------------------------------------------

    print("-" * 70)
    print("WOULD PERFORM")
    print("-" * 70)

    for subject in subject_cats:
        for related in related_cats:
            print(
                f"Would add {related['name']} to "
                f"{subject['name']}'s Cohort relationship."
            )

    print()
    print("=" * 70)
    print("TEST COMPLETE")
    print("No Notion pages or properties were modified.")
    print("=" * 70)


if __name__ == "__main__":
    main()