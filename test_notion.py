import os
import json
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

ALL_CATS_DATA_SOURCE_ID = "cf09cd66-e972-8293-8c29-073c01330f5b"
HISTORICAL_EVENTS_DATA_SOURCE_ID = "3b79cd66-e972-8014-9954-000b6da417a8"


def inspect_data_source(label, data_source_id):
    print("=" * 70)
    print(label)
    print("=" * 70)

    data_source = notion.request(
        f"data_sources/{data_source_id}",
        "GET"
    )

    print("Top-level keys returned by Notion:")
    print(list(data_source.keys()))

    print()
    print("Data source properties:")
    print(
        json.dumps(
            data_source.get("properties", {}),
            indent=2
        )
    )

    print()


print("Connecting to Notion...")

notion = Client(auth=NOTION_TOKEN)

print("Connection successful.")
print()

inspect_data_source(
    "ALL CATS DATA SOURCE",
    ALL_CATS_DATA_SOURCE_ID
)

inspect_data_source(
    "HISTORICAL EVENTS DATA SOURCE",
    HISTORICAL_EVENTS_DATA_SOURCE_ID
)

print("=" * 70)
print("Schema inspection complete.")
print("No Notion pages or properties were modified.")
print("=" * 70)
