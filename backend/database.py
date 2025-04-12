from pymongo import MongoClient

from seedDb import seed_database

def connect_db(mongo_url, db_name):
    try:    
        client = MongoClient(mongo_url)
        # The ismaster command is cheap and does not require auth.
        client.admin.command("ismaster")
        _db = client[db_name]
        print(f"Connected to MongoDB database '{db_name}'.")
        return _db
    except Exception as e:
        print(f"Error connecting to MongoDB at {mongo_url}: {e}")
        return None

if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017/")

    db = client["raiffeisen"]
    for name in ["customers", "advisors", "summaries"]:
        if name not in db.list_collection_names():
            db.create_collection(name)
            print(f"Created collection: {name}")
        else:
            print(f"Collection already exists: {name}")

    seed_database()
