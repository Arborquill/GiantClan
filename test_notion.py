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
    print("COHORT WRITE PAYLOAD TEST")
    print("=" * 70)
    print("READ ONLY - NOTHING WILL BE CHANGED")
    print()

    # ---------------------------------------------------------------
    # Retrieve the known test event
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
    print()

    # ---------------------------------------------------------------
    # Read Relationship Type
    # ---------------------------------------------------------------

    formula_value = get_relationship_formula(event)

    print("Relationship Type:")
    print(repr(formula_value))
    print()

    relationships = parse_relationships(formula_value)

    print("Detected relationships:")
    print(relationships)
    print()

    if "Cohort" not in relationships:
        print("ERROR: Cohort relationship was not detected.")
        return

    # ---------------------------------------------------------------
    # Get Subject Cats
    # ---------------------------------------------------------------

    subject_ids = get_relation_ids(
        properties.get("Subject Cat")
    )

    print("-" * 70)
    print("SUBJECT CATS")
    print("-" * 70)

    subject_cats = []

    for cat_id in subject_ids:
        name = get_cat_name(notion, cat_id)

        subject_cats.append({
            "id": cat_id,
            "name": name,
        })

        print(f"{name}")
        print(f"ID: {cat_id}")
        print()

    # ---------------------------------------------------------------
    # Get Related Cats
    # ---------------------------------------------------------------

    related_ids = get_relation_ids(
        properties.get("Related Cats")
    )

    print("-" * 70)
    print("RELATED CATS")
    print("-" * 70)

    related_cats = []

    for cat_id in related_ids:
        name = get_cat_name(notion, cat_id)

        related_cats.append({
            "id": cat_id,
            "name": name,
        })

        print(f"{name}")
        print(f"ID: {cat_id}")
        print()

    # ---------------------------------------------------------------
    # Inspect existing Cohort relations
    # ---------------------------------------------------------------

    print("-" * 70)
    print("EXISTING COHORT RELATIONS")
    print("-" * 70)

    cohort_data = {}

    for subject in subject_cats:
        page = notion.pages.retrieve(
            page_id=subject["id"]
        )

        cat_properties = page.get("properties", {})

        cohort_property = cat_properties.get("Cohort")

        if not cohort_property:
            print(f"{subject['name']}: Cohort property NOT FOUND")
            cohort_data[subject["id"]] = []
            continue

        if cohort_property.get("type") != "relation":
            print(
                f"{subject['name']}: Cohort property has unexpected "
                f"type: {cohort_property.get('type')}"
            )
            cohort_data[subject["id"]] = []
            continue

        existing_ids = get_relation_ids(cohort_property)

        cohort_data[subject["id"]] = existing_ids

        print(f"{subject['name']}:")
        print(f"  Existing Cohort IDs: {existing_ids}")

        if existing_ids:
            for existing_id in existing_ids:
                existing_name = get_cat_name(
                    notion,
                    existing_id
                )
                print(
                    f"  - {existing_name} "
                    f"({existing_id})"
                )
        else:
            print("  - No existing Cohort cats.")

        print()

    # ---------------------------------------------------------------
    # Construct the hypothetical update payload
    # ---------------------------------------------------------------

    print("-" * 70)
    print("HYPOTHETICAL UPDATE PAYLOADS")
    print("-" * 70)

    print("These payloads WOULD be sent to Notion.")
    print("They are NOT being sent.")
    print()

    for subject in subject_cats:
        existing_ids = cohort_data.get(
            subject["id"],
            []
        )

        print(f"{subject['name']}")
        print()

        for related in related_cats:
            related_id = related["id"]

            if related_id in existing_ids:
                print(
                    f"  {related['name']} is already in "
                    f"{subject['name']}'s Cohort."
                )
                continue

            updated_ids = existing_ids + [related_id]

            payload = {
                "properties": {
                    "Cohort": {
                        "relation": [
                            {"id": cat_id}
                            for cat_id in updated_ids
                        ]
                    }
                }
            }

            print(
                f"  Would add {related['name']} "
                f"to {subject['name']}'s Cohort."
            )

            print("  Payload:")
            print(f"  {payload}")
            print()

    # ---------------------------------------------------------------
    # Final safety check
    # ---------------------------------------------------------------

    print("=" * 70)
    print("TEST COMPLETE")
    print("NO UPDATE API CALLS WERE MADE.")
    print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
    print("=" * 70)


if __name__ == "__main__":
    main()