import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

HAWKKIT_EVENT_ID = "3c89cd66-e972-805a-a8ce-fef962c23d09"
MAPLEPAW_ID = "3c09cd66-e972-80f9-9355-c0df84dd19ec"

notion = Client(auth=NOTION_TOKEN)


def get_plain_text(rich_text):
    if not isinstance(rich_text, list):
        return ""

    parts = []

    for item in rich_text:
        if not isinstance(item, dict):
            continue

        plain = item.get("plain_text")
        if plain:
            parts.append(plain)

        elif item.get("text"):
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
            cat_id = item.get("id")
            if cat_id:
                ids.append(cat_id)

    return ids


print("=" * 70)
print("HAWKKIT EVENT CONTENT + PARTICIPATION TEST")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

print("Connecting to Notion...")
notion.pages.retrieve(page_id=HAWKKIT_EVENT_ID)
print("Connection successful.")
print()

# ----------------------------------------------------------------------
# RETRIEVE HAWKKIT PAGE
# ----------------------------------------------------------------------

print("=" * 70)
print("HAWKKIT PAGE")
print("=" * 70)

page = notion.pages.retrieve(page_id=HAWKKIT_EVENT_ID)

print("Page ID:")
print(HAWKKIT_EVENT_ID)
print()

properties = page.get("properties", {})

print("Property names:")
print(list(properties.keys()))
print()

# ----------------------------------------------------------------------
# INSPECT ALL RELEVANT PROPERTIES
# ----------------------------------------------------------------------

print("=" * 70)
print("RELEVANT EVENT PROPERTIES")
print("=" * 70)

for property_name in [
    "Name",
    "Event",
    "Subject of an Event",
    "Subject Cat",
    "Related Cats",
    "Siblings",
    "Parents",
    "Historical Events",
]:
    if property_name not in properties:
        print(property_name + ": NOT PRESENT")
        print()
        continue

    prop = properties[property_name]

    print(property_name + ":")
    print("  Type:", prop.get("type"))

    prop_type = prop.get("type")

    if prop_type == "title":
        value = prop.get("title", [])
        print("  Text:", repr(get_plain_text(value)))

    elif prop_type == "rich_text":
        value = prop.get("rich_text", [])
        print("  Text:", repr(get_plain_text(value)))

    elif prop_type == "relation":
        value = prop.get("relation", [])
        print("  Relation IDs:", get_relation_ids(prop))

    else:
        print("  Raw value:", prop.get(prop_type))

    print()

# ----------------------------------------------------------------------
# RETRIEVE PAGE CONTENT BLOCKS
# ----------------------------------------------------------------------

print("=" * 70)
print("PAGE CONTENT BLOCKS")
print("=" * 70)

blocks = notion.blocks.children.list(block_id=HAWKKIT_EVENT_ID)

print("Number of blocks returned:")
print(len(blocks.get("results", [])))
print()

all_page_text = []

for index, block in enumerate(blocks.get("results", []), start=1):
    block_type = block.get("type")

    print("BLOCK", index)
    print("Type:", block_type)

    block_data = block.get(block_type)

    if isinstance(block_data, dict):
        rich_text = block_data.get("rich_text")

        if isinstance(rich_text, list):
            text = get_plain_text(rich_text)

            if text:
                print("Text:")
                print(repr(text))
                all_page_text.append(text)

    print("-" * 70)

print()

# ----------------------------------------------------------------------
# COMBINED EVENT TEXT
# ----------------------------------------------------------------------

print("=" * 70)
print("COMBINED EVENT TEXT")
print("=" * 70)

combined_text = " ".join(all_page_text)

if combined_text:
    print(repr(combined_text))
else:
    print("NO PAGE TEXT FOUND.")

print()

# ----------------------------------------------------------------------
# MAPLEPAW CHECK
# ----------------------------------------------------------------------

print("=" * 70)
print("MAPLEPAW PARTICIPATION CHECK")
print("=" * 70)

print("Maplepaw ID:")
print(MAPLEPAW_ID)
print()

maplepaw_in_any_relation = False

for property_name in properties:
    prop = properties[property_name]

    if prop.get("type") != "relation":
        continue

    relation_ids = get_relation_ids(prop)

    if MAPLEPAW_ID in relation_ids:
        print("Maplepaw appears in relation property:")
        print(property_name)
        print()

        maplepaw_in_any_relation = True

if not maplepaw_in_any_relation:
    print("Maplepaw is NOT present in any relation property on this event.")
    print()

# ----------------------------------------------------------------------
# TEXT SEARCH
# ----------------------------------------------------------------------

print("=" * 70)
print("ORPHANED LITTER TEXT SEARCH")
print("=" * 70)

search_phrases = [
    "orphaned litter",
    "dead monster",
    "Cliffshock",
    "Blackchirp",
]

for phrase in search_phrases:
    found = phrase.lower() in combined_text.lower()

    print(repr(phrase), "->", found)

print()

print("=" * 70)
print("TEST COMPLETE")
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
print("=" * 70)
