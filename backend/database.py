from pymongo import MongoClient

from seedDb import seed_database

client = MongoClient("mongodb://localhost:27017/")

db = client["raiffeisen"]
for name in ["customers", "advisors", "summaries"]:
    if name not in db.list_collection_names():
        db.create_collection(name)
        print(f"Created collection: {name}")
    else:
        print(f"Collection already exists: {name}")

seed_database()
