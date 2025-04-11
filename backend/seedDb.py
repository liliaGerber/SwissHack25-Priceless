import random
from datetime import datetime

from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["raiffeisen"]


def seed_advisors():
    advisors = [
        {"name": "Alice Johnson", "email": "alice.johnson@bank.com", "department": "Investments"},
        {"name": "Bob Smith", "email": "bob.smith@bank.com", "department": "Loans"},
        {"name": "Clara Evans", "email": "clara.evans@bank.com", "department": "Savings"},
    ]
    db.advisors.insert_many(advisors)
    print("Seeded advisors.")


def seed_customers():
    advisor_ids = list(db.advisors.find({}, {"_id": 1}))
    if not advisor_ids:
        raise Exception("Seed advisors first")

    customers = []
    for i in range(10):
        advisor_id = random.choice(advisor_ids)["_id"]
        customers.append({
            "name": f"Customer {i + 1}",
            "email": f"customer{i + 1}@example.com",
            "joined": datetime(2023, random.randint(1, 12), random.randint(1, 28)),
            "balance": round(random.uniform(500, 10000), 2),
            "advisor_id": advisor_id
        })

    db.customers.insert_many(customers)
    print("Seeded customers.")


def seed_database():
    for name in ["customers", "advisors"]:
        if name not in db.list_collection_names():
            db.create_collection(name)

    # Run seeds
    seed_advisors()
    seed_customers()
