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
            title_items = prop.get("title", [])

            if title_items:
                return "".join(
                    item.get("plain_text", "")
                    for item in title_items
                )

    return "(Unnamed)"


def get_relation_ids(page, property_name):
    properties = page.get("properties", {})
    prop = properties.get(property_name)

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
    print("COHORT EVENT INDEXING TEST")
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
    print("EVENT PARTICIPANTS")
    print("=" * 70)

    participant_pages = {}

    print()
    print("SUBJECT CATS")
    print("-" * 70)

    for cat_id in subject_ids:
        cat = get_page(cat_id)
        participant_pages[cat_id] = cat

        print(get_title(cat))
        print("ID:", cat_id)
        print()

    print("RELATED CATS")
    print("-" * 70)

    for cat_id in related_ids:
        cat = get_page(cat_id)
        participant_pages[cat_id] = cat

        print(get_title(cat))
        print("ID:", cat_id)
        print()

    if "Cohort" not in relationships:
        print("=" * 70)
        print("COHORT PROCESSING")
        print("=" * 70)
        print()
        print("Cohort relationship was NOT detected.")
        print("Cohort processing was skipped.")
        return

    print("=" * 70)
    print("COHORT PROCESSING")
    print("=" * 70)
    print()
    print("Cohort relationship detected.")
    print()
    print("Checking each participant against every other participant.")
    print()
    print("A cat qualifies only when:")
    print("1. The cat is participating in this Event.")
    print("2. Another cat is also participating in this Event.")
    print("3. The cat's existing Cohort relation contains that other cat.")
    print()

    qualifying_cats = []

    print("-" * 70)
    print("PARTICIPANT CHECKS")
    print("-" * 70)

    for cat_id in participant_ids:
        cat = participant_pages[cat_id]
        cat_name = get_title(cat)

        cohort_ids = get_relation_ids(cat, "Cohort")

        print()
        print(cat_name)
        print("ID:", cat_id)
        print("Existing Cohort IDs:", cohort_ids)

        found_event_cohort = False

        for other_id in participant_ids:
            if other_id == cat_id:
                continue

            if other_id in cohort_ids:
                other_cat = participant_pages[other_id]
                other_name = get_title(other_cat)

                print()
                print("  QUALIFYING PAIR:")
                print("  " + cat_name + " <-> " + other_name)

                found_event_cohort = True

        if found_event_cohort:
            qualifying_cats.append(cat_id)
            print()
            print("  RESULT: " + cat_name + " qualifies.")
        else:
            print()
            print("  RESULT: " + cat_name + " does NOT qualify.")

    print()
    print("=" * 70)
    print("PROPOSED EVENT PROPERTY")
    print("=" * 70)
    print()
    print("Cohort Cats would contain:")

    if qualifying_cats:
        for cat_id in qualifying_cats:
            cat_name = get_title(participant_pages[cat_id])

            print(
                "  - "
                + cat_name
                + " ("
                + cat_id
                + ")"
            )
    else:
        print("  - Nobody")

    print()
    print("=" * 70)
    print("HYPOTHETICAL UPDATE PAYLOAD")
    print("=" * 70)
    print()
    print("This payload is NOT being sent to Notion.")
    print()

    payload = {
        "properties": {
            "Cohort Cats": {
                "relation": [
                    {"id": cat_id}
                    for cat_id in qualifying_cats
                ]
            }
        }
    }

    print(payload)

    print()
    print("=" * 70)
    print("TEST COMPLETE")
    print("NO UPDATE API CALLS WERE MADE.")
    print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
    print("=" * 70)


if __name__ == "__main__":
    main()
