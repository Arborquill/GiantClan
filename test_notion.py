import os
import json
import urllib.request
import urllib.error

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
EVENTS_DATABASE_ID = os.environ["EVENTS_DATABASE_ID"]
CATS_DATABASE_ID = os.environ["CATS_DATABASE_ID"]

NOTION_VERSION = "2022-06-28"

TARGET_EVENT_TITLE = "While out on a secret date, Cliffshock and Blackchirp find an orphaned litter of kits in the wreckage of a dead monster. It isn't the direction they expected their lives to be tugged, but their hearts brim with love for them. Their gentle touch and affectionate purrs are the kits’ home now."


def notion_request(url, method="GET", body=None):
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }

    data = None

    if body is not None:
        data = json.dumps(body).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method=method,
    )

    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(
                response.read().decode("utf-8")
            )

    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8")

        print()
        print("=" * 70)
        print("NOTION API ERROR")
        print("=" * 70)
        print("HTTP status:")
        print(error.code)
        print()
        print("Request URL:")
        print(url)
        print()
        print("Request method:")
        print(method)
        print()
        print("Request body:")
        print(json.dumps(body, indent=2))
        print()
        print("Notion response:")
        print(error_body)
        print("=" * 70)

        raise


def get_pages(database_id, database_name):
    print()
    print("Querying " + database_name + " database...")
    print("Database ID:")
    print(database_id)

    pages = []
    cursor = None

    while True:
        body = {}

        if cursor:
            body["start_cursor"] = cursor

        data = notion_request(
            f"https://api.notion.com/v1/databases/{database_id}/query",
            method="POST",
            body=body,
        )

        pages.extend(data.get("results", []))

        if not data.get("has_more"):
            break

        cursor = data.get("next_cursor")

    print(
        database_name,
        "pages retrieved:",
        len(pages),
    )

    return pages


def get_title(page):
    properties = page.get("properties", {})

    for property_data in properties.values():
        if property_data.get("type") == "title":
            title_items = property_data.get("title", [])

            return "".join(
                item.get("plain_text", "")
                for item in title_items
            )

    return ""


print("=" * 70)
print("NOTION DATABASE CONNECTION DIAGNOSTIC")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

print("Environment variables detected:")
print(
    "NOTION_TOKEN:",
    "present" if NOTION_TOKEN else "MISSING",
)
print(
    "EVENTS_DATABASE_ID:",
    EVENTS_DATABASE_ID,
)
print(
    "CATS_DATABASE_ID:",
    CATS_DATABASE_ID,
)

print()
print("=" * 70)
print("CONNECTING")
print("=" * 70)

events = get_pages(
    EVENTS_DATABASE_ID,
    "Events",
)

cats = get_pages(
    CATS_DATABASE_ID,
    "Cats",
)

print()
print("=" * 70)
print("DATABASE CONNECTION TEST PASSED")
print("=" * 70)

print()
print("Events retrieved:")
print(len(events))

print()
print("Cats retrieved:")
print(len(cats))

print()
print("=" * 70)
print("SEARCHING FOR TARGET EVENT")
print("=" * 70)

matches = []

for page in events:
    title = get_title(page)

    if title == TARGET_EVENT_TITLE:
        matches.append(page)

print()
print("Exact title matches:")
print(len(matches))

for page in matches:
    print()
    print("Event ID:")
    print(page["id"])
    print()
    print("Event title:")
    print(repr(get_title(page)))

print()
print("=" * 70)
print("TEST COMPLETE")
print("=" * 70)
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
print("=" * 70)