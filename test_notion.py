import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

HAWKKIT_ID = "3c89cd66-e972-805a-a8ce-fef962c23d09"
ACTUAL_EVENT_ID = "3c89cd66-e972-8082-9ae3-f4b5c6fe3ca3"
MAPLEPAW_ID = "3c09cd66-e972-80f9-9355-c0df84dd19ec"

notion = Client(auth=NOTION_TOKEN)


def get_plain_text(rich_text):
    if not isinstance(rich_text, list):
        return ""

    parts = []

    for item in rich_text:
        if not isinstance(item, dict):
            continue

        plain_text = item.get("plain_text")

        if plain_text:
            parts.append(plain_text)

        else:
            text_data = item.get("text")

            if isinstance(text_data, dict):
                content = text_data.get("content")

                if content:
                    parts.append(content)

    return "".join(parts)


def get_relation_ids(property_value):
    if not isinstance(property_value, dict):
        return []

    relation = property_value.get("relation")

    if not isinstance(relation, list):
        return []

    ids = []

    for item in relation:
        if isinstance(item, dict):
            relation_id = item.get("id")

            if relation_id:
                ids.append(relation_id)

    return ids


def get_title(properties):
    for prop in properties.values():
        if not isinstance(prop, dict):
            continue

        if prop.get("type") == "title":
            return get_plain_text(prop.get("title", []))

    return ""


def get_event_property_text(properties, property_name):
    prop = properties.get(property_name)

    if not isinstance(prop, dict):
        return ""

    prop_type = prop.get("type")

    if prop_type == "title":
        return get_plain_text(prop.get("title", []))

    if prop_type == "rich_text":
        return get_plain_text(prop.get("rich_text", []))

    return ""


print("=" * 70)
print("ACTUAL HAWKKIT EVENT INSPECTION")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

print("Connecting to Notion...")
notion.pages.retrieve(page_id=HAWKKIT_ID)
print("Connection successful.")
print()

# ----------------------------------------------------------------------
# HAWKKIT CAT PAGE
# ----------------------------------------------------------------------

print("=" * 70)
print("HAWKKIT CAT PAGE")
print("=" * 70)

hawkkit_page = notion.pages.retrieve(page_id=HAWKKIT_ID)
hawkkit_properties = hawkkit_page.get("properties", {})

print("Hawkkit ID:")
print(HAWKKIT_ID)
print()

print("Hawkkit title:")
print(repr(get_title(hawkkit_properties)))
print()

print("Subject of an Event:")
subject_event_prop = hawkkit_properties.get("Subject of an Event")

if subject_event_prop:
    subject_event_ids = get_relation_ids(subject_event_prop)

    print(subject_event_ids)
else:
    subject_event_ids = []
    print("NOT PRESENT")

print()

# ----------------------------------------------------------------------
# ACTUAL EVENT PAGE
# ----------------------------------------------------------------------

print("=" * 70)
print("ACTUAL EVENT PAGE")
print("=" * 70)

event_page = notion.pages.retrieve(page_id=ACTUAL_EVENT_ID)
event_properties = event_page.get("properties", {})

print("Event ID:")
print(ACTUAL_EVENT_ID)
print()

print("Event title:")
print(repr(get_title(event_properties)))
print()

print("Property names:")
print(list(event_properties.keys()))
print()

# ----------------------------------------------------------------------
# INSPECT ALL RELATION PROPERTIES
# ----------------------------------------------------------------------

print("=" * 70)
print("EVENT RELATION PROPERTIES")
print("=" * 70)

relation_properties = {}

for property_name, prop in event_properties.items():

    if not isinstance(prop, dict):
        continue

    if prop.get("type") != "relation":
        continue

    ids = get_relation_ids(prop)

    relation_properties[property_name] = ids

    print(property_name + ":")
    print("  IDs:", ids)
    print()

# ----------------------------------------------------------------------
# INSPECT EVENT TEXT PROPERTIES
# ----------------------------------------------------------------------

print("=" * 70)
print("EVENT TEXT PROPERTIES")
print("=" * 70)

for property_name in event_properties:

    text = get_event_property_text(
        event_properties,
        property_name
    )

    if text:
        print(property_name + ":")
        print(repr(text))
        print()

# ----------------------------------------------------------------------
# PAGE CONTENT
# ----------------------------------------------------------------------

print("=" * 70)
print("EVENT PAGE CONTENT")
print("=" * 70)

blocks_response = notion.blocks.children.list(
    block_id=ACTUAL_EVENT_ID
)

blocks = blocks_response.get("results", [])

print("Number of top-level blocks:")
print(len(blocks))
print()

all_text = []


def inspect_block(block, indent=""):
    block_type = block.get("type")

    print(indent + "Block type:", block_type)

    block_data = block.get(block_type)

    if isinstance(block_data, dict):

        rich_text = block_data.get("rich_text")

        if isinstance(rich_text, list):

            text = get_plain_text(rich_text)

            if text:
                print(indent + "Text:")
                print(indent + repr(text))
                all_text.append(text)

    print()

    if block_type == "column_list":
        try:
            children_response = notion.blocks.children.list(
                block_id=block.get("id")
            )

            children = children_response.get("results", [])

            for child in children:
                inspect_block(child, indent + "  ")

        except Exception as error:
            print(indent + "Could not retrieve child blocks:")
            print(indent + repr(error))
            print()


for block in blocks:
    inspect_block(block)

print("=" * 70)
print("COMBINED EVENT TEXT")
print("=" * 70)

combined_text = " ".join(all_text)

if combined_text:
    print(repr(combined_text))
else:
    print("NO EVENT TEXT FOUND.")

print()

# ----------------------------------------------------------------------
# MAPLEPAW PARTICIPATION
# ----------------------------------------------------------------------

print("=" * 70)
print("MAPLEPAW PARTICIPATION CHECK")
print("=" * 70)

print("Maplepaw ID:")
print(MAPLEPAW_ID)
print()

found_maplepaw = False

for property_name, ids in relation_properties.items():

    if MAPLEPAW_ID in ids:

        print("Maplepaw IS present in:")
        print("  " + property_name)

        found_maplepaw = True

if not found_maplepaw:
    print("Maplepaw is NOT present in any event relation property.")

print()

# ----------------------------------------------------------------------
# HAWKKIT PARTICIPATION
# ----------------------------------------------------------------------

print("=" * 70)
print("HAWKKIT PARTICIPATION CHECK")
print("=" * 70)

found_hawkkit = False

for property_name, ids in relation_properties.items():

    if HAWKKIT_ID in ids:

        print("Hawkkit IS present in:")
        print("  " + property_name)

        found_hawkkit = True

if not found_hawkkit:
    print("Hawkkit is NOT present in any event relation property.")

print()

# ----------------------------------------------------------------------
# FINAL INTERPRETATION
# ----------------------------------------------------------------------

print("=" * 70)
print("PARTICIPATION INTERPRETATION")
print("=" * 70)

if found_hawkkit:
    print("Hawkkit qualifies as an actual participant in this event.")
else:
    print("Hawkkit does NOT qualify as an actual participant.")

if found_maplepaw:
    print("Maplepaw qualifies as an actual participant in this event.")
else:
    print("Maplepaw does NOT qualify as an actual participant.")

print()
print("SIBLINGSHIP ALONE MUST NOT BE USED TO DETERMINE EVENT PARTICIPATION.")
print()

print("=" * 70)
print("TEST COMPLETE")
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
print("=" * 70)