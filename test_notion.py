```python
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
        relation["id"]
        for relation in prop.get("relation", [])
    ]


def get_event_relation_type(event):
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
        relationship.strip()
        for relationship in value.split("·")
        if relationship.strip()
    ]


def get_event_participants(event):
    subject_ids = get_relation_ids(event, "Subject Cat")
    related_ids = get_relation_ids(event, "Related Cats")

    all_ids = []

    for cat_id in subject_ids + related_ids:
        if cat_id not in all_ids:
            all_ids.append(cat_id)

    return subject_ids, related_ids, all_ids


def get_relationship_ids_for_cat(cat_page, relationship):
    property_map = {
        "Cohort": "Cohort",
        "Mate": "Mate",
        "Mentor": "Mentor Cats",
        "Apprentice": "Apprentice Cats",
    }

    property_name = property_map.get(relationship)

    if not property_name:
        return []

    return get_relation_ids(cat_page, property_name)


def main():
    print("=" * 70)
    print("EVENT RELATIONSHIP INDEXING TEST")
    print("=" * 70)
    print("READ ONLY - NOTHING WILL BE CHANGED")
    print()

    event = get_page(EVENT_ID)

    event_title = get_title(event)

    print("EVENT")
    print("-" * 70)
    print(event_title)
    print()
    print("Event ID:")
    print(EVENT_ID)
    print()

    relationship_value = get_event_relation_type(event)
    relationships = parse_relationships(relationship_value)

    print("Relationship Type:")
    print(repr(relationship_value))
    print()
    print("Detected relationships:")
    print(relationships)
    print()

    subject_ids, related_ids, participant_ids = get_event_participants(event)

    print("=" * 70)
    print("EVENT PARTICIPANTS")
    print("=" * 70)

    print()
    print("SUBJECT CATS")
    print("-" * 70)

    subject_pages = {}

    for cat_id in subject_ids:
        cat = get_page(cat_id)
        name = get_title(cat)
        subject_pages[cat_id] = cat

        print(f"{name}")
        print(f"ID: {cat_id}")
        print()

    print("RELATED CATS")
    print("-" * 70)

    related_pages = {}

    for cat_id in related_ids:
        cat = get_page(cat_id)
        name = get_title(cat)
        related_pages[cat_id] = cat

        print(f"{name}")
        print(f"ID: {cat_id}")
        print()

    print("=" * 70)
    print("ALL PARTICIPANTS")
    print("=" * 70)

    participant_pages = {}

    for cat_id in participant_ids:
        if cat_id in subject_pages:
            cat = subject_pages[cat_id]
        elif cat_id in related_pages:
            cat = related_pages[cat_id]
        else:
            cat = get_page(cat_id)

        participant_pages[cat_id] = cat

        print(f"{get_title(cat)}")
        print(f"ID: {cat_id}")
        print()

    print("=" * 70)
    print("RELATIONSHIP ANALYSIS")
    print("=" * 70)

    proposed_event_properties = {
        "Cohort": [],
        "Mate": [],
        "Mentor": [],
        "Apprentice": [],
    }

    for relationship in relationships:
        if relationship not in proposed_event_properties:
            print()
            print(f"Skipping unsupported relationship: {relationship}")
            continue

        print()
        print("-" * 70)
        print(f"{relationship.upper()} RELATIONSHIP")
        print("-" * 70)

        print()
        print("Checking each participant's existing relationship...")

        for cat_id in participant_ids:
            cat = participant_pages[cat_id]
            cat_name = get_title(cat)

            relation_ids = get_relationship_ids_for_cat(
                cat,
                relationship
            )

            relation_names = []

            for relation_id in relation_ids:
                try:
                    related_cat = get_page(relation_id)
                    relation_names.append(
                        (relation_id, get_title(related_cat))
                    )
                except Exception:
                    relation_names.append(
                        (relation_id, "(Could not retrieve)")
                    )

            print()
            print(f"{cat_name}:")
            print(f"  Existing {relationship} IDs: {relation_ids}")

            if relation_names:
                for relation_id, relation_name in relation_names:
                    print(
                        f"  - {relation_name} ({relation_id})"
                    )
            else:
                print(f"  - No existing {relationship} cats.")

        print()
        print("PARTICIPANT PAIRS THAT QUALIFY")
        print("-" * 70)

        qualifying_pairs = []
        qualifying_cats = []

        for cat_id in participant_ids:
            cat = participant_pages[cat_id]
            cat_name = get_title(cat)

            relation_ids = get_relationship_ids_for_cat(
                cat,
                relationship
            )

            for other_id in participant_ids:
                if other_id == cat_id:
                    continue

                if other_id in relation_ids:
                    other_cat = participant_pages[other_id]
                    other_name = get_title(other_cat)

                    qualifying_pairs.append(
                        (cat_id, cat_name, other_id, other_name)
                    )

                    if cat_id not in qualifying_cats:
                        qualifying_cats.append(cat_id)

        if qualifying_pairs:
            for (
                cat_id,
                cat_name,
                other_id,
                other_name
            ) in qualifying_pairs:
                print(
                    f"{cat_name} <-> {other_name}"
                )
        else:
            print("No qualifying participant pairs found.")

        print()
        print("CATS THAT WOULD BE ADDED TO EVENT PROPERTY")
        print("-" * 70)

        if qualifying_cats:
            for cat_id in qualifying_cats:
                cat_name = get_title(participant_pages[cat_id])

                print(
                    f"Would add {cat_name} to the Event's "
                    f"{relationship} Cats property."
                )

                proposed_event_properties[
                    relationship
                ].append(cat_id)
        else:
            print(
                f"No cats would be added to the Event's "
                f"{relationship} Cats property."
            )

    print()
    print("=" * 70)
    print("FINAL HYPOTHETICAL EVENT PROPERTIES")
    print("=" * 70)
    print()
    print("These are NOT being sent to Notion.")
    print()

    for relationship, cat_ids in proposed_event_properties.items():
        print(f"{relationship} Cats:")

        if not cat_ids:
            print("  []")
            print()
            continue

        for cat_id in cat_ids:
            print(
                f"  - {get_title(participant_pages[cat_id])}"
                f" ({cat_id})"
            )

        print()

    print("=" * 70)
    print("TEST COMPLETE")
    print("NO UPDATE API CALLS WERE MADE.")
    print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
    print("=" * 70)


if __name__ == "__main__":
    main()
```
