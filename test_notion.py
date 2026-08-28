import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

CAT_ID = "3c09cd66-e972-80f9-9355-c0df84dd19ec"

notion = Client(auth=NOTION_TOKEN)


def print_relation_property(name, prop):
    print()
    print(name + ":")
    print("  Type:", prop.get("type"))

    if prop.get("type") != "relation":
        print("  Not a relation property.")
        return

    relation = prop.get("relation", {})

    print("  Full relation definition:")
    print(relation)

    print()
    print("  Database ID:")
    print(relation.get("database_id"))

    print()
    print("  Data source ID:")
    print(relation.get("data_source_id"))

    print()
    print("  Relation type:")
    print(relation.get("type"))

    if "dual_property" in relation:
        print()
        print("  Dual property:")
        print(relation.get("dual_property"))


print("=" * 70)
print("IDENTIFY EVENT DATA SOURCE")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

print("Connecting to Notion...")

cat = notion.pages.retrieve(page_id=CAT_ID)

print("Connection successful.")

properties = cat.get("properties", {})

print()
print("=" * 70)
print("CAT")
print("=" * 70)

print()
print("Cat:")
print("Maplepaw")

print()
print("Cat ID:")
print(CAT_ID)

print()
print("=" * 70)
print("EVENT-RELATED RELATION PROPERTIES")
print("=" * 70)

for property_name in [
    "Subject of an Event",
    "Related to an Event",
    "Subject Event Related Cats",
    "Historical Events",
]:
    if property_name not in properties:
        print()
        print(property_name + ": NOT PRESENT")
        continue

    print_relation_property(
        property_name,
        properties[property_name]
    )

print()
print("=" * 70)
print("ALL RELATION PROPERTIES")
print("=" * 70)

for property_name, prop in properties.items():
    if prop.get("type") == "relation":
        print_relation_property(property_name, prop)

print()
print("=" * 70)
print("TEST COMPLETE")
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
print("=" * 70)
