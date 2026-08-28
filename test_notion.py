import os
from notion_client import Client


NOTION_TOKEN = os.environ["NOTION_TOKEN"]
ALL_CATS_DATA_SOURCE_ID = "9849cd66-e972-8390-b142-01cdd6b8b3a6"
EVENTS_DATA_SOURCE_ID = "cf09cd66-e972-8293-8c29-073c01330f5b"


def get_plain_text(property_data):
    """Extract plain text from a Notion title/rich_text property."""
    if not property_data:
        return ""

    results = property_data.get("title") or property_data.get("rich_text") or []

    return "".join(
        item.get("plain_text", "")
        for item in results
    )


def get_relation_ids(property_data):
    """Extract related page IDs from a Notion relation property."""
    if not property_data:
        return []

    return [
        item["id"]
        for item in property_data.get("relation", [])
    ]


def get_cat_name(notion, cat_id):
    """Retrieve a cat page and return its name."""
    page = notion.pages.retrieve(page_id=cat_id)
    properties = page.get("properties", {})

    # Find the title property rather than assuming its name.
    for prop in properties.values():
        if prop.get("type") == "title":
            return get_plain_text(prop)

    return "(Unnamed cat)"


def get_relationship_formula(event):
    """Retrieve the Relationship Type formula as a Python string."""
    property_data = event["properties"].get("Relationship Type")

    if not property_data:
        return ""

    formula = property_data.get("formula", {})

    return formula.get("string") or ""


def parse_relationships(formula_value):
    """Turn 'Cohort · Mate · Mentor' into a list of relationship names."""
    if not formula_value:
        return []

    return [
        relationship.strip()
        for relationship in formula_value.split("·")
        if relationship.strip()
    ]


def test_cohort_processing(notion, event):
    print("=" * 70)
    print("COHORT PROCESSING TEST")
    print("=" * 70)
    print("READ ONLY - NOTHING WILL BE CHANGED")
    print()

    event_id = event["id"]
    event_name = get_plain_text(event["properties"].get("Event"))

    print("Event:")
    print(event_name)
    print("ID:", event_id)
    print()

    # ---------------------------------------------------------------
    # Retrieve the relationship formula
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
    # Retrieve Subject Cats
    # ---------------------------------------------------------------

    subject_property = event["properties"].get("Subject Cat")
    subject_ids = get_relation_ids(subject_property)

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

        print(f"Cat: {cat_name}")
        print(f"ID:  {cat_id}")
        print()

    # ---------------------------------------------------------------
    # Retrieve Related Cats
    # ---------------------------------------------------------------

    related_property = event["properties"].get("Related Cats")
    related_ids = get_relation_ids(related_property)

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

        print(f"Cat: {cat_name}")
        print(f"ID:  {cat_id}")
        print()

    # ---------------------------------------------------------------
    # Cohort processing
    # ---------------------------------------------------------------

    print("-" * 70)
    print("COHORT PROCESSING")
    print("-" * 70)

    if "Cohort" not in relationships:
        print("Cohort relationship was NOT detected.")
        print("Cohort processing was skipped.")
        return

    print("Cohort relationship detected.")
    print()

    print("The Cohort processor would receive:")
    print()

    print("Subject Cats:")
    for cat in subject_cats:
        print(f"  - {cat['name']} ({cat['id']})")

    print()

    print("Related Cats:")
    for cat in related_cats:
        print(f"  - {cat['name']} ({cat['id']})")

    print()

    # ---------------------------------------------------------------
    # Simulate the logical operation without writing anything
    # ---------------------------------------------------------------

    print("SIMULATED COHORT RESULT")
    print("-" * 70)

    if not subject_cats:
        print("No Subject Cats were found.")
    elif not related_cats:
        print("No Related Cats were found.")
    else:
        for subject in subject_cats:
            for related in related_cats:
                print(
                    f"Would establish Cohort relationship: "
                    f"{subject['name']} <-> {related['name']}"
                )

    print()
    print("=" * 70)
    print("TEST COMPLETE")
    print("No Notion pages or properties were modified.")
    print("=" * 70)


def main():
    notion = Client(auth=NOTION_TOKEN)

    print("Connecting to Notion...")
    notion.users.me()
    print("Connection successful.")
    print()

    print("=" * 70)
    print("FINDING HISTORICAL EVENT")
    print("=" * 70)

    response = notion.data_sources.query(
        data_source_id=EVENTS_DATA_SOURCE_ID
    )

    events = response.get("results", [])

    if not events:
        print("No events were returned.")
        return

    event = events[0]

    test_cohort_processing(notion, event)


if __name__ == "__main__":
    main()