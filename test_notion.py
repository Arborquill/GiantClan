import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

EVENT_ID = "3c99cd66-e972-80fc-a803-de69fe8bd6de"

notion = Client(auth=NOTION_TOKEN)


def get_page(page_id):
    return notion.pages.retrieve(page_id=page_id)


def get_title(page):
    properties = page.get("properties", {})

    for prop in properties.values():
        if prop.get("type") == "title":
            title_data = prop.get("title", [])

            if title_data:
                return "".join(
                    item.get("plain_text", "")
                    for item in title_data
                )

    return "(Unnamed)"


def get_relation_ids(page, property_name):
    prop = page.get("properties", {}).get(property_name)

    if not prop:
        return []

    if prop.get("type") != "relation":
        return []

    return [
        item["id"]
        for item in prop.get("relation", [])
    ]


def get_relationship_type(event):
    prop = event["properties"].get("Relationship Type")

    if not prop:
        return ""

    formula = prop.get("formula", {})

    if formula.get("type") != "string":
        return ""

    return formula.get("string") or ""


def parse_relationships(value):
    if not value:
        return []

    return [
        item.strip()
        for item in value.split("·")
        if item.strip()
    ]


def main():
    print("=" * 70)
    print("EVENT RELATIONSHIP INDEXING TEST")
    print("=" * 70)
    print("READ ONLY - NOTHING WILL BE CHANGED")
    print()

    event = get_page(EVENT_ID)

    print("EVENT")
    print("-" * 70)
    print(get_title(event))
    print()
    print("ID:")
    print(EVENT_ID)
    print()

    relationship_value = get_relationship_type(event)
    relationships = parse_relationships(relationship_value)

    print("Relationship Type:")
    print(repr(relationship_value))
    print()

    print("Detected relationships:")
    print(relationships)
    print()

    subject_ids = get_relation_ids(event, "Subject Cat")
    related_ids = get_relation_ids(event, "Related Cats")

    participant_ids = []

    for cat_id in subject_ids:
        if cat_id not in participant_ids:
            participant_ids.append(cat_id)

    for cat_id in related_ids:
        if cat_id not in participant_ids:
            participant_ids.append(cat_id)

    print("=" * 70)
    print("SUBJECT CATS")
    print("=" * 70)

    participant_pages = {}

    for cat_id in subject_ids:
        cat = get_page(cat_id)
        participant_pages[cat_id] = cat

        print()
        print(get_title(cat))
        print("ID:", cat_id)

    print()
    print("=" * 70)
    print("RELATED CATS")
    print("=" * 70)

    for cat_id in related_ids:
        cat = get_page(cat_id)
        participant_pages[cat_id] = cat

        print()
        print(get_title(cat))
        print("ID:", cat_id)

    print()
    print("=" * 70)
    print("RELATIONSHIP ANALYSIS")
    print("=" * 70)

    property_names = {
        "Cohort": "Cohort",
        "Mate": "Mate",
        "Mentor": "Mentor",
        "Apprentice": "Apprentice"
    }

    proposed_properties = {
        "Cohort": [],
        "Mate": [],
        "Mentor": [],
        "Apprentice": []
    }

    for relationship in relationships:
        print()
        print("-" * 70)
        print(relationship.upper())
        print("-" * 70)

        if relationship not in property_names:
            print("No Cat property mapping exists for this relationship.")
            continue

        cat_property = property_names[relationship]

        qualifying_cats = []

        for cat_id in participant_ids:
            cat = participant_pages[cat_id]
            cat_name = get_title(cat)

            existing_ids = get_relation_ids(
                cat,
                cat_property
            )

            print()
            print(cat_name)
            print("Existing", relationship, "IDs:")
            print(existing_ids)

            for other_id in participant_ids:
                if other_id == cat_id:
                    continue

                if other_id in existing_ids:
                    other_name = get_title(
                        participant_pages[other_id]
                    )

                    print(
                        "  QUALIFIES:",
                        cat_name,
                        "<->",
                        other_name
                    )

                    if cat_id not in qualifying_cats:
                        qualifying_cats.append(cat_id)

        print()
        print("Would place these cats into Event", relationship, "Cats:")

        if qualifying_cats:
            for cat_id in qualifying_cats:
                cat_name = get_title(
                    participant_pages[cat_id]
                )

                print(
                    "  -",
                    cat_name,
                    "(" + cat_id + ")"
                )

                proposed_properties[
                    relationship
                ].append(cat_id)
        else:
            print("  None")

    print()
    print("=" * 70)
    print("HYPOTHETICAL EVENT PROPERTY RESULTS")
    print("=" * 70)
    print()
    print("These values WOULD be written to the Event.")
    print("They are NOT being written.")
    print()

    for relationship in proposed_properties:
        print(relationship + " Cats:")

        cat_ids = proposed_properties[relationship]

        if not cat_ids:
            print("  []")
            print()
            continue

        for cat_id in cat_ids:
            print(
                "  -",
                get_title(participant_pages[cat_id]),
                "(" + cat_id + ")"
            )

        print()

    print("=" * 70)
    print("TEST COMPLETE")
    print("NO UPDATE API CALLS WERE MADE.")
    print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
    print("=" * 70)


if __name__ == "__main__":
    main()
