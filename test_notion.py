import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

EVENTS_DATABASE_ID = "3b79cd66-e972-80d0-aa83-de1c481c6ef6"
EVENTS_DATA_SOURCE_ID = "3b79cd66-e972-8014-9954-000b6da417a8"

CATS_DATABASE_ID = "9849cd66-e972-8390-b142-01cdd6b8b3a6"
CATS_DATA_SOURCE_ID = "cf09cd66-e972-8293-8c29-073c01330f5b"

notion = Client(auth=NOTION_TOKEN)


# ============================================================
# RELATIONSHIP MAPPINGS
# ============================================================

RELATIONSHIP_PROPERTIES = {
    "Kit": "Kits",
    "Parent": "Parents",
    "Sibling": "Siblings",
    "Cohort": "Cohort",
    "Mate": "Mate",
    "Mentor": "Mentor(s)",
    "Apprentice": "Apprentices",
}

EVENT_RELATION_PROPERTIES = {
    "Kit": "Kit Cats",
    "Parent": "Parent Cats",
    "Sibling": "Sibling Cats",
    "Cohort": "Cohort Cats",
    "Mate": "Mate Cats",
    "Mentor": "Mentor Cats",
    "Apprentice": "Apprentice Cats",
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_database_pages(data_source_id):
    pages = []
    cursor = None

    while True:

        payload = {}

        if cursor:
            payload["start_cursor"] = cursor

        response = notion.data_sources.query(
            data_source_id=data_source_id,
            **payload,
        )

        pages.extend(
            response.get("results", [])
        )

        if not response.get("has_more"):
            break

        cursor = response.get("next_cursor")

    return pages


def get_title(page):
    properties = page.get(
        "properties",
        {}
    )

    for property_data in properties.values():

        if property_data.get("type") == "title":

            title_items = property_data.get(
                "title",
                []
            )

            return "".join(
                item.get(
                    "plain_text",
                    ""
                )
                for item in title_items
            )

    return ""


def get_relation_ids(page, property_name):
    properties = page.get(
        "properties",
        {}
    )

    property_data = properties.get(
        property_name
    )

    if not property_data:
        return []

    if property_data.get("type") != "relation":
        return []

    return [
        item["id"]
        for item in property_data.get(
            "relation",
            []
        )
        if item.get("id")
    ]


def get_formula_string(page, property_name):
    properties = page.get(
        "properties",
        {}
    )

    property_data = properties.get(
        property_name
    )

    if not property_data:
        return ""

    if property_data.get("type") != "formula":
        return ""

    formula = property_data.get(
        "formula",
        {}
    )

    if formula.get("type") == "string":
        return formula.get(
            "string"
        ) or ""

    return ""


def parse_relationship_types(value):
    if not value:
        return []

    return [
        item.strip()
        for item in value.split("·")
        if item.strip()
    ]


# ============================================================
# BUILD EVENT RELATIONSHIPS
# ============================================================
#
# event_id:
#     The Notion page ID of the Event to process.
#
# Returns:
#     A dictionary containing the result of the operation.
#
# ============================================================

def build_event_relationships(event_id):

    print("=" * 70)
    print("EVENT RELATIONSHIP BUILD")
    print("=" * 70)
    print()

    # ========================================================
    # RETRIEVE EVENT
    # ========================================================

    print("Retrieving Event...")

    event = notion.pages.retrieve(
        page_id=event_id
    )

    actual_event_id = event["id"]

    print("Retrieving All Cats pages...")

    cats = get_database_pages(
        CATS_DATA_SOURCE_ID
    )

    print("Pages retrieved.")

    # ========================================================
    # EVENT INFORMATION
    # ========================================================

    print()
    print("=" * 70)
    print("EVENT")
    print("=" * 70)

    event_title = get_title(event)

    print(event_title)

    print()
    print("Event ID:")
    print(actual_event_id)

    # ========================================================
    # GET DIRECT PARTICIPANTS
    # ========================================================
    #
    # ONLY cats directly listed in Subject Cat or Related Cats
    # can ever appear in the Event relationship properties.
    #
    # A participant's personal relationships do NOT
    # automatically make those cats Event participants.
    #
    # ========================================================

    subject_ids = get_relation_ids(
        event,
        "Subject Cat"
    )

    related_ids = get_relation_ids(
        event,
        "Related Cats"
    )

    participant_ids = []

    for cat_id in subject_ids + related_ids:

        if cat_id not in participant_ids:
            participant_ids.append(cat_id)

    print()
    print("=" * 70)
    print("DIRECT PARTICIPANTS")
    print("=" * 70)

    print(participant_ids)

    # ========================================================
    # BUILD CAT LOOKUP
    # ========================================================

    cat_by_id = {
        page["id"]: page
        for page in cats
    }

    participant_names = {}

    for cat_id in participant_ids:

        page = cat_by_id.get(
            cat_id
        )

        if page:

            participant_names[cat_id] = get_title(
                page
            )

        else:

            participant_names[cat_id] = (
                "[CAT NOT FOUND]"
            )

    print()

    for cat_id in participant_ids:

        print(
            participant_names[cat_id],
            "->",
            cat_id,
        )

    # ========================================================
    # GET RELATIONSHIP TYPES
    # ========================================================

    relationship_formula = get_formula_string(
        event,
        "Relationship Type",
    )

    relationship_types = parse_relationship_types(
        relationship_formula
    )

    print()
    print("=" * 70)
    print("RELATIONSHIP TYPES")
    print("=" * 70)

    print("Raw formula value:")
    print(repr(relationship_formula))

    print("Parsed relationship types:")
    print(relationship_types)

    # ========================================================
    # CALCULATE EVENT RELATIONS
    # ========================================================
    #
    # If Relationship Type is BLANK:
    #     Do NOT modify any Event relationship properties.
    #
    # If Relationship Type contains a relationship:
    #     Calculate that relationship using ONLY direct
    #     participants.
    #
    # If the relationship exists between participants:
    #     Store the matching participant(s).
    #
    # If the relationship type exists but there is NO
    # matching relationship between participants:
    #     Store an EMPTY relation.
    #
    # This intentionally clears stale Event relations.
    #
    # ========================================================

    participant_set = set(
        participant_ids
    )

    results = {}

    print()
    print("=" * 70)
    print("CALCULATED EVENT RELATIONS")
    print("=" * 70)

    if not relationship_types:

        print(
            "No relationship types were found."
        )

        print(
            "No Event relationship properties "
            "will be changed."
        )

    for relationship_type in relationship_types:

        source_property = RELATIONSHIP_PROPERTIES.get(
            relationship_type
        )

        event_property = EVENT_RELATION_PROPERTIES.get(
            relationship_type
        )

        print()
        print("Relationship:")
        print(relationship_type)

        print("Cat property:")
        print(source_property)

        print("Event property:")
        print(event_property)

        if not source_property or not event_property:

            print(
                "WARNING: Missing property mapping."
            )

            results[relationship_type] = []

            continue

        matching_ids = set()

        # ----------------------------------------------------
        # ONLY examine relationships between direct
        # participants.
        # ----------------------------------------------------

        for participant_id in participant_ids:

            participant = cat_by_id.get(
                participant_id
            )

            if not participant:
                continue

            related_cat_ids = get_relation_ids(
                participant,
                source_property,
            )

            for related_cat_id in related_cat_ids:

                if related_cat_id in participant_set:

                    matching_ids.add(
                        related_cat_id
                    )

        # ----------------------------------------------------
        # Preserve Event participant order.
        #
        # If nothing matched, this becomes [].
        # That intentionally clears the Event relation.
        # ----------------------------------------------------

        ordered_ids = [
            cat_id
            for cat_id in participant_ids
            if cat_id in matching_ids
        ]

        results[relationship_type] = ordered_ids

        print("Will contain:")

        if not ordered_ids:

            print(
                "[NONE]"
            )

            print(
                "The Event relationship property "
                "will be cleared."
            )

        else:

            for cat_id in ordered_ids:

                print(
                    participant_names.get(
                        cat_id,
                        "[CAT NOT FOUND]",
                    ),
                    "->",
                    cat_id,
                )

    # ========================================================
    # BUILD UPDATE PAYLOAD
    # ========================================================

    print()
    print("=" * 70)
    print("FINAL EVENT PROPERTY VALUES")
    print("=" * 70)

    properties_to_update = {}

    for relationship_type in relationship_types:

        event_property = EVENT_RELATION_PROPERTIES.get(
            relationship_type
        )

        if not event_property:
            continue

        ids = results.get(
            relationship_type,
            []
        )

        print()
        print(event_property + ":")
        print(ids)

        properties_to_update[event_property] = {
            "relation": [
                {"id": cat_id}
                for cat_id in ids
            ]
        }

    # ========================================================
    # UPDATE EVENT
    # ========================================================

    print()
    print("=" * 70)
    print("UPDATING EVENT")
    print("=" * 70)

    if not properties_to_update:

        print(
            "No relationship properties need updating."
        )

        if not relationship_types:

            print(
                "Reason: Relationship Type is blank."
            )

    else:

        print()
        print("Updating Event relations...")

        notion.pages.update(
            page_id=actual_event_id,
            properties=properties_to_update,
        )

        print("Event updated successfully.")

    # ========================================================
    # READ-BACK VERIFICATION
    # ========================================================

    print()
    print("=" * 70)
    print("READ-BACK VERIFICATION")
    print("=" * 70)

    verification_failed = False

    if not properties_to_update:

        print(
            "Nothing was written, so there is nothing to verify."
        )

    else:

        print()
        print("Retrieving Event again from Notion...")

        updated_event = notion.pages.retrieve(
            page_id=actual_event_id
        )

        print("Event retrieved successfully.")

        updated_properties = updated_event.get(
            "properties",
            {}
        )

        for relationship_type in relationship_types:

            event_property = EVENT_RELATION_PROPERTIES.get(
                relationship_type
            )

            if not event_property:
                continue

            expected_ids = results.get(
                relationship_type,
                []
            )

            property_data = updated_properties.get(
                event_property
            )

            if not property_data:

                print()
                print(event_property + ":")
                print(
                    "ERROR: Property was not returned."
                )

                verification_failed = True

                continue

            actual_ids = [
                item["id"]
                for item in property_data.get(
                    "relation",
                    []
                )
                if item.get("id")
            ]

            print()
            print(event_property + ":")
            print("Expected:")
            print(expected_ids)

            print("Stored:")
            print(actual_ids)

            if actual_ids == expected_ids:

                print(
                    "VERIFICATION: PASS"
                )

            else:

                print(
                    "VERIFICATION: FAIL"
                )

                verification_failed = True

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print()
    print("=" * 70)
    print("BUILD COMPLETE")
    print("=" * 70)

    if not relationship_types:

        print(
            "SUCCESS: Event has no relationship types."
        )

        print(
            "No Event relationship properties were changed."
        )

    elif verification_failed:

        print(
            "WARNING: One or more Event relations "
            "failed read-back verification."
        )

    else:

        print(
            "SUCCESS: All calculated Event relations "
            "were stored correctly."
        )

    print()
    print(
        "Only the Event was modified. "
        "No All Cats pages were modified."
    )

    print("=" * 70)

    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {
        "success": not verification_failed,
        "event_id": actual_event_id,
        "event_title": event_title,
        "relationship_types": relationship_types,
        "updated_properties": properties_to_update,
        "verification_failed": verification_failed,
    }


# ============================================================
# LOCAL TEST
# ============================================================
#
# This is temporary.
#
# When we connect the webhook, this section will be replaced
# by the web endpoint.
#
# For now, change ONLY TEST_EVENT_ID when testing.
#
# ============================================================

if __name__ == "__main__":

    TEST_EVENT_ID = (
        "3c99cd66-e972-80fc-a803-de69fe8bd6de"
    )

    build_event_relationships(
        TEST_EVENT_ID
    )
