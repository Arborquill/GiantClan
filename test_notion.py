import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

CAT_ID = "3c09cd66-e972-80f9-9355-c0df84dd19ec"

notion = Client(auth=NOTION_TOKEN)


def inspect_relation(name, prop):
    print()
    print(name)
    print("-" * 70)

    print("Property type:")
    print(prop.get("type"))

    print()
    print("Raw property:")
    print(prop)

    if prop.get("type") != "relation":
        return

    relation = prop.get("relation")

    print()
    print("Raw relation value:")
    print(relation)

    print()
    print("Python type of relation value:")
    print(type(relation).__name__)

    if isinstance(relation, dict):
        print()
        print("Relation database ID:")
        print(relation.get("database_id"))

        print()
        print("Relation data source ID:")
        print(relation.get("data_source_id"))

        print()
        print("Relation type:")
        print(relation.get("type"))

        if "dual_property" in relation:
            print()
            print("Dual property:")
            print(relation.get("dual_property"))

    elif isinstance(relation, list):
        print()
        print("Relation is a list.")

        for index, item in enumerate(relation):
            print()
            print("Relation item", index + 1)
            print("Python type:", type(item).__name__)
            print("Value:", item)

            if isinstance(item, dict):
                print("Database ID:", item.get("database_id"))
                print("Data source ID:", item.get("data_source_id"))
                print("Type:", item.get("type"))

                if "dual_property" in item:
                    print("Dual property:", item.get("dual_property"))


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
print("MAPLEPAW")
print("=" * 70)

print()
print("Cat ID:")
print(CAT_ID)

print()
print("=" * 70)
print("EVENT-RELATED PROPERTIES")
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

    inspect_relation(
        property_name,
        properties[property_name]
    )

print()
print("=" * 70)
print("TEST COMPLETE")
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
print("=" * 70)
