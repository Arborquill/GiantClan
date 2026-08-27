import os
import json
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

ALL_CATS_DATA_SOURCE_ID = "cf09cd66-e972-8293-8c29-073c01330f5b"
EVENTS_DATA_SOURCE_ID = "3b79cd66-e972-8014-9954-000b6da417a8"

notion = Client(auth=NOTION_TOKEN)


def inspect_data_source(name, data_source_id):
    print()
    print("=" * 70)
    print(name)
    print("=" * 70)

    data_source = notion.request(
        method="GET",
        endpoint=f"data_sources/{data_source_id}"
    )

    print()
    print("Top-level keys returned by Notion:")
    print(list(data_source.keys()))

    print()
    print("Data source properties:")
    print(json.dumps(data_source.get("properties", {}), indent=2))

    print()
    print("=" * 70)


print("Connecting to Notion...")
print("Connection successful.")

inspect_data_source(
    "ALL CATS DATA SOURCE",
    ALL_CATS_DATA_SOURCE_ID
)

inspect_data_source(
    "HISTORICAL EVENTS DATA SOURCE",
    EVENTS_DATA_SOURCE_ID
)

print()
print("=" * 70)
print("Schema inspection complete.")
print("No Notion pages or properties were modified.")
print("=" * 70)
