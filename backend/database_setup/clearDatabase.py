from pymongo import MongoClient

DATABASE_CONNECTION="mongodb://localhost:27017"
DB="raiffeisen"

def clear_meetings():
    client = MongoClient("mongodb://localhost:27017")
    db = client[DB]
    meetings = db["meetings"]
    result = meetings.delete_many({})
    print(f"✅ Deleted {result.deleted_count} meeting(s).")

def clear_customer():
    client = MongoClient("mongodb://localhost:27017")
    db = client[DB]
    meetings = db["customers"]
    result = meetings.delete_many({})
    print(f"✅ Deleted {result.deleted_count} customers(s).")

def clear_advisor():
    client = MongoClient("mongodb://localhost:27017")
    db = client[DB]
    meetings = db["advisors"]
    result = meetings.delete_many({})
    print(f"✅ Deleted {result.deleted_count} advisors(s).")

clear_advisor()
clear_customer()
clear_meetings()