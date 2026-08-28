import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

EVENTS_DATA_SOURCE_ID = "cf09cd66-e972-8293-8c29-073c01330f5b"

notion = Client(auth=NOTION_TOKEN)


def get_plain_text(property_value):
    if not property_value:
        return ""

    if property_value.get("type") == "title":
        items = property_value.get("title", [])
    elif property_value.get("type") == "rich_text":
        items = property_value.get("rich_text", [])
    else:
        return ""

    return "".join(
        item.get("plain_text", "")
        for item in items
    )


def get_page_title(page):
    for prop in page.get("properties", {}).values():
        if prop.get("type") == "title":
            return get_plain_text(prop)

    return "(unnamed)"


print("=" * 70)
print("FIND LITTER EVENT")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

print("Connecting to Notion...")

response = notion.data_sources.query(
    data_source_id=EVENTS_DATA_SOURCE_ID
)

all_events = []

while True:
    for page in response.get("results", []):
        all_events.append(page)

    if not response.get("has_more"):
        break

    response = notion.data_sources.query(
        data_source_id=EVENTS_DATA_SOURCE_ID,
        start_cursor=response["next_cursor"]
    )

print("Connection successful.")
print()
print("Events retrieved:", len(all_events))

print()
print("=" * 70)
print("SEARCH RESULTS")
print("=" * 70)

matches = []

for page in all_events:
    title = get_page_title(page)

    if "orphaned litter" in title.lower():
        matches.append(page)

    elif "cliffshock" in title.lower() and "blackchirp" in title.lower():
        matches.append(page)

    elif "secret date" in title.lower():
        matches.append(page)

if not matches:
    print()
    print("No matching events found using the expected phrases.")
    print()
    print("Printing ALL event titles so we can identify the correct one:")
    print()

    for page in all_events:
        print("TITLE:")
        print(repr(get_page_title(page)))
        print("ID:")
        print(page["id"])
        print("-" * 70)

else:
    print()
    print("Matching events found:", len(matches))

    for number, page in enumerate(matches, start=1):
        title = get_page_title(page)

        print()
        print("MATCH", number)
        print("-" * 70)
        print("Title:")
        print(repr(title))
        print()
        print("ID:")
        print(page["id"])

        print()
        print("Property names:")
        print(list(page.get("properties", {}).keys()))

print()
print("=" * 70)
print("TEST COMPLETE")
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
print("=" * 70)
