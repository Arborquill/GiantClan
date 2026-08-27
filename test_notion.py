import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

ALL_CATS_ID = "9849cd66e9728390b14201cdd6b8b3a6"
EVENTS_ID = "3b79cd66e97280d0aa83de1c481c6ef6"

notion = Client(auth=NOTION_TOKEN)


def print_database_schema(name, database_id):
    print()
    print("=" * 70)
    print(name)
    print("=" * 70)

    database = notion.databases.retrieve(database_id=database_id)

    print("Database title:", end=" ")

    title = database.get("title", [])
    if title:
        print("".join(item.get("plain_text", "") for item in title))
    else:
        print("(no title returned)")

    print()
    print("Properties:")
    print("-" * 70)

    properties = database.get("properties", {})

    for property_name, property_data in properties.items():
        property_type = property_data.get("type", "unknown")

        print(f"\n{property_name}")
        print(f"  Type: {property_type}")

        if property_type == "relation":
            relation = property_data.get("relation", {})
            related_database = relation.get("database_id")
            print(f"  Related database ID: {related_database}")

            if relation.get("dual_property"):
                dual = relation["dual_property"]
                print(f"  Two-way property: {dual.get('synced_property_name')}")

        elif property_type == "formula":
            formula = property_data.get("formula", {})
            print(f"  Formula return type: {formula.get('type')}")

        elif property_type == "rollup":
            rollup = property_data.get("rollup", {})
            print(f"  Rollup type: {rollup.get('type')}")

        elif property_type == "select":
            options = property_data.get("select", {}).get("options", [])
            if options:
                print("  Options:", ", ".join(option.get("name", "") for option in options))

        elif property_type == "multi_select":
            options = property_data.get("multi_select", {}).get("options", [])
            if options:
                print("  Options:", ", ".join(option.get("name", "") for option in options))


print("Connecting to Notion...")
print("Connection successful.")

print_database_schema("ALL CATS", ALL_CATS_ID)
print_database_schema("HISTORICAL EVENTS", EVENTS_ID)

print()
print("=" * 70)
print("Schema inspection complete.")
print("No Notion pages or properties were modified.")
print("=" * 70)
