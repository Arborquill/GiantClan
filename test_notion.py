import os
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
EVENT_ID = "3c89cd66-e972-80f9-8036-c2858a8a140c"

notion = Client(auth=NOTION_TOKEN)

print("=" * 70)
print("ZERO-INDENTATION RELATIONSHIP TEST")
print("=" * 70)
print("READ ONLY - NOTHING WILL BE CHANGED")
print()

notion.users.me()
print("Connection successful.")
print()

event = notion.pages.retrieve(page_id=EVENT_ID)
p = event["properties"]

print("EVENT")
print("-" * 70)
print(p["Event"]["title"][0]["plain_text"])
print()

relationship_string = p["Relationship Type"]["formula"]["string"]
relationships = relationship_string.split(" · ")

print("RELATIONSHIP TYPES")
print("-" * 70)
print(relationships)
print()

subject_ids = [x["id"] for x in p["Subject Cat"]["relation"]]
related_ids = [x["id"] for x in p["Related Cats"]["relation"]]

participant_ids = subject_ids + related_ids

print("DIRECT PARTICIPANTS")
print("-" * 70)
print(participant_ids)
print()

cat_cliffshock = notion.pages.retrieve(page_id="3c09cd66-e972-8024-b9cd-c95b729dddec")
cat_blackchirp = notion.pages.retrieve(page_id="3bf9cd66-e972-80c2-ba66-c0d5231e636c")
cat_hawkkit = notion.pages.retrieve(page_id="3c89cd66-e972-805a-a8ce-fef962c23d09")
cat_dahliakit = notion.pages.retrieve(page_id="3c89cd66-e972-806a-8a2d-d23c7a1c8322")
cat_moorkit = notion.pages.retrieve(page_id="3c89cd66-e972-80d1-9581-d5dcd0b75b7e")
cat_bluekit = notion.pages.retrieve(page_id="3c89cd66-e972-80dd-9d1c-db61a32fdaa6")
cat_basskit = notion.pages.retrieve(page_id="3c89cd66-e972-8061-97dc-e36b021e7dae")

print("PARTICIPANT RELATIONSHIPS")
print("-" * 70)

print("Cliffshock Siblings:")
print(cat_cliffshock["properties"]["Siblings"]["relation"])
print()

print("Cliffshock Parents:")
print(cat_cliffshock["properties"]["Parents"]["relation"])
print()

print("Cliffshock Kits:")
print(cat_cliffshock["properties"]["Kits"]["relation"])
print()

print("Cliffshock Cohort:")
print(cat_cliffshock["properties"]["Cohort"]["relation"])
print()

print("Cliffshock Mate:")
print(cat_cliffshock["properties"]["Mate"]["relation"])
print()

print("Blackchirp Siblings:")
print(cat_blackchirp["properties"]["Siblings"]["relation"])
print()

print("Blackchirp Parents:")
print(cat_blackchirp["properties"]["Parents"]["relation"])
print()

print("Blackchirp Kits:")
print(cat_blackchirp["properties"]["Kits"]["relation"])
print()

print("Blackchirp Cohort:")
print(cat_blackchirp["properties"]["Cohort"]["relation"])
print()

print("Blackchirp Mate:")
print(cat_blackchirp["properties"]["Mate"]["relation"])
print()

print("Hawkkit Siblings:")
print(cat_hawkkit["properties"]["Siblings"]["relation"])
print()

print("Hawkkit Parents:")
print(cat_hawkkit["properties"]["Parents"]["relation"])
print()

print("Hawkkit Kits:")
print(cat_hawkkit["properties"]["Kits"]["relation"])
print()

print("Hawkkit Cohort:")
print(cat_hawkkit["properties"]["Cohort"]["relation"])
print()

print("Hawkkit Mate:")
print(cat_hawkkit["properties"]["Mate"]["relation"])
print()

print("Dahliakit Siblings:")
print(cat_dahliakit["properties"]["Siblings"]["relation"])
print()

print("Dahliakit Parents:")
print(cat_dahliakit["properties"]["Parents"]["relation"])
print()

print("Dahliakit Kits:")
print(cat_dahliakit["properties"]["Kits"]["relation"])
print()

print("Moorkit Siblings:")
print(cat_moorkit["properties"]["Siblings"]["relation"])
print()

print("Moorkit Parents:")
print(cat_moorkit["properties"]["Parents"]["relation"])
print()

print("Bluekit Siblings:")
print(cat_bluekit["properties"]["Siblings"]["relation"])
print()

print("Bluekit Parents:")
print(cat_bluekit["properties"]["Parents"]["relation"])
print()

print("Basskit Siblings:")
print(cat_basskit["properties"]["Siblings"]["relation"])
print()

print("Basskit Parents:")
print(cat_basskit["properties"]["Parents"]["relation"])
print()

print("=" * 70)
print("EXPECTED EVENT RELATIONS")
print("=" * 70)
print()

print("Direct participants are:")
print("Cliffshock")
print("Blackchirp")
print("Hawkkit")
print("Dahliakit")
print("Moorkit")
print("Bluekit")
print("Basskit")
print()

print("Maplepaw is NOT a direct participant.")
print("Maplepaw must therefore appear in NONE of the new Event relations.")
print()

print("The final writable Event properties will be:")
print("Kit Cats")
print("Parent Cats")
print("Sibling Cats")
print("Cohort Cats")
print("Mate Cats")
print("Mentor Cats")
print("Apprentice Cats")
print()

print("=" * 70)
print("TEST COMPLETE")
print("NO UPDATE API CALLS WERE MADE.")
print("NO NOTION PAGES OR PROPERTIES WERE MODIFIED.")
print("=" * 70)
