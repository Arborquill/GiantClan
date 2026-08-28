import os
from notion_client import Client

notion = Client(auth=os.environ["NOTION_TOKEN"])

EVENTS = "3b79cd66-e972-8014-9954-000b6da417a8"

print("Connecting to Notion...")
print("Connection successful.")
print()
print("=" * 70)
print("RELATION ID TO CAT NAME TEST")
print("=" * 70)
print()
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

result = notion.request(
f"data_sources/{EVENTS}/query",
"POST",
{}
)

events = result.get("results", [])
event = events[0]
properties = event.get("properties", {})

subject_property = properties.get("Subject Cat", {})
subject_relations = subject_property.get("relation", [])

related_property = properties.get("Related Cats", {})
related_relations = related_property.get("relation", [])

print("Subject Cat IDs:")
print(subject_relations)
print()

print("Related Cats IDs:")
print(related_relations)
print()

subject_id_1 = subject_relations[0]["id"]
subject_id_2 = subject_relations[1]["id"]
subject_id_3 = subject_relations[2]["id"]
subject_id_4 = subject_relations[3]["id"]

related_id_1 = related_relations[0]["id"]

cat_1 = notion.request(
f"pages/{subject_id_1}",
"GET"
)

cat_2 = notion.request(
f"pages/{subject_id_2}",
"GET"
)

cat_3 = notion.request(
f"pages/{subject_id_3}",
"GET"
)

cat_4 = notion.request(
f"pages/{subject_id_4}",
"GET"
)

cat_5 = notion.request(
f"pages/{related_id_1}",
"GET"
)

name_1 = cat_1.get("properties", {}).get("Name", {}).get("title", [])
name_2 = cat_2.get("properties", {}).get("Name", {}).get("title", [])
name_3 = cat_3.get("properties", {}).get("Name", {}).get("title", [])
name_4 = cat_4.get("properties", {}).get("Name", {}).get("title", [])
name_5 = cat_5.get("properties", {}).get("Name", {}).get("title", [])

print("CAT 1 NAME DATA:")
print(name_1)
print()

print("CAT 2 NAME DATA:")
print(name_2)
print()

print("CAT 3 NAME DATA:")
print(name_3)
print()

print("CAT 4 NAME DATA:")
print(name_4)
print()

print("CAT 5 NAME DATA:")
print(name_5)
print()

print("=" * 70)
print("TEST COMPLETE")
print("No Notion pages or properties were modified.")
print("=" * 70)
