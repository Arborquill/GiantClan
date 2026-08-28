import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]

EVENT_ID = "3c89cd66-e972-80f9-8036-c2858a8a140c"
MAPLEPAW_ID = "3c09cd66-e972-80f9-9355-c0df84dd19ec"

notion = Client(auth=NOTION_TOKEN)

print("=" * 70)
print("LITTER EVENT PARTICIPATION TEST")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

print("Connecting to Notion...")
notion.users.me()
print("Connection successful.")
print()

event = notion.pages.retrieve(page_id=EVENT_ID)
properties = event["properties"]

print("=" * 70)
print("EVENT")
print("=" * 70)
print()

print("Event ID:")
print(EVENT_ID)
print()

print("Event property:")
print(properties.get("Event"))
print()

print("=" * 70)
print("SUBJECT CATS")
print("=" * 70)
print()

subject = properties.get("Subject Cat")
print("Raw Subject Cat property:")
print(subject)
print()

subject_relation = subject.get("relation", [])
print("Subject Cat relation:")
print(subject_relation)
print()

print("=" * 70)
print("RELATED CATS")
print("=" * 70)
print()

related = properties.get("Related Cats")
print("Raw Related Cats property:")
print(related)
print()

related_relation = related.get("relation", [])
print("Related Cats relation:")
print(related_relation)
print()

print("=" * 70)
print("MAPLEPAW")
print("=" * 70)
print()

print("Maplepaw ID:")
print(MAPLEPAW_ID)
print()

print("Maplepaw appears directly in Subject Cat:")
print(any(x.get("id") == MAPLEPAW_ID for x in subject_relation))
print()

print("Maplepaw appears directly in Related Cats:")
print(any(x.get("id") == MAPLEPAW_ID for x in related_relation))
print()

print("=" * 70)
print("RELATIONSHIP TYPE")
print("=" * 70)
print()

relationship_type = properties.get("Relationship Type")
print("Raw property:")
print(relationship_type)
print()

formula = relationship_type.get("formula", {})
print("Formula:")
print(formula)
print()

relationship_string = formula.get("string", "")
print("Formula string:")
print(repr(relationship_string))
print()

print("=" * 70)
print("RELATIONSHIPS DETECTED")
print("=" * 70)
print()

print("Parsed relationships:")
print([x.strip() for x in relationship_string.split("·") if x.strip()])
print()

print("=" * 70)
print("FINAL PARTICIPATION RULE")
print("=" * 70)
print()

print("Only cats appearing directly in Subject Cat or Related Cats")
print("are event participants.")
print()

print("A cat being the sibling, parent, mate, cohort, mentor, or")
print("apprentice of a participant does NOT make that cat a participant.")
print()

print("Maplepaw direct participation:")
print(MAPLEPAW_ID in [x.get("id") for x in subject_relation + related_relation])
print()

print("=" * 70)
print("EXPECTED RESULT FOR MAPLEPAW")
print("=" * 70)
print()

print("Maplepaw should be EXCLUDED from this event because he")
print("is not listed directly in Subject Cat or Related Cats.")
print()

print("His sibling relationship with the five kits does not")
print("make him an event participant.")
print()

print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
print("=" * 70)
