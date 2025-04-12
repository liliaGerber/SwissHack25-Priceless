import json
import random
from datetime import datetime, timedelta
from bson import ObjectId
from pymongo import MongoClient


FIRST_NAMES = ["Anna", "Ben", "Chloe", "David", "Elena", "Finn", "Grace", "Henry", "Isla", "Jack",
               "Katherine", "Leo", "Mia", "Noah", "Olivia", "Paul", "Quinn", "Ryan", "Sophia", "Thomas"]
LAST_NAMES = ["Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker", "Schulz", "Hoffmann",
              "Koch", "Bauer", "Richter", "Klein", "Wolf", "Schröder", "Neumann", "Schwarz", "Zimmermann", "Braun"]

GOAL_DESCRIPTIONS = [
    "Retirement Planning", "Buy a House", "Save for Children's Education",
    "Build Emergency Fund", "Buy a Car", "Travel Fund", "Pay Off Debt",
    "Start a Business"
]

PROBLEMATIC_THEMES = [
    "Recent Job Loss", "Divorce/Separation", "Significant Health Issues",
    "Inheritance Disputes", "Problematic Debt Levels", "Past Bankruptcy"
]

BANKING_PRODUCTS = [
    "Girokonto (Checking Account)", "Sparkonto (Savings Account)", "Online Banking",
    "Kreditkarte (Credit Card)", "Wohnkredit (Mortgage)", "Privatkredit (Personal Loan)",
    "Bausparen (Building Society Savings)", "Fondssparplan (Fund Savings Plan)",
    "Aktien depot (Stock Portfolio)", "Versicherung (Insurance Product)", "Leasing"
]

MEETING_NOTE_PARTS = {
    "opening": [
        "Initial consultation.", "Follow-up meeting.", "Quarterly review.", "Goal discussion.", "Product inquiry."
    ],
    "topic": [
        "Discussed goal of {goal}.", "Reviewed current assets.", "Evaluated risk tolerance.",
        "Reviewed portfolio performance.", "Explored options for {product}.", "Discussed market conditions.",
        "Talked about increasing savings rate.", "Addressed concerns about {concern}."
    ],
    "outcome": [
        "Client prefers {approach} approach.", "Agreed on {strategy} strategy.", "Started funding {product}.",
        "Opened a {product}.", "Increased contribution to {goal}.", "Decided to wait and monitor.",
        "Client will provide requested documents.", "Scheduled next review for {future_date}.",
        "Implemented changes to {product}."
    ],
    "details": [
        "Client seemed {emotion}.", "Concerned about market volatility.", "Asked about college savings options.",
        "Needs more information on sustainable investments.", "Happy with current progress.", "Wants to consolidate debts."
    ],
    "misc": [
        "Retirement", "a new car", "their child's education", "market volatility", "low interest rates",
        "investment diversification", "a balanced", "a conservative", "an aggressive", "a diversified portfolio",
        "a savings plan", "a loan application", "their mortgage", "next quarter", "next month",
        "anxious", "optimistic", "cautious", "pleased"
    ]
}

MONGO_URI = "mongodb://localhost:27017/" 
DB_NAME = "raiffeisen_enhanced" 
client = MongoClient(MONGO_URI)
db = client[DB_NAME]


def get_random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def generate_past_date(start_year=2020, end_year=None):
    """Generates a random date between start_year and today."""
    end_year = end_year or datetime.now().year
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    if year == datetime.now().year:
        month = random.randint(1, datetime.now().month)
        if month == datetime.now().month:
             day = random.randint(1, datetime.now().day -1 if datetime.now().day > 1 else 1) # Avoid today

    try:
        return datetime(year, month, day)
    except ValueError:
         return datetime(year, month, day -1) 


def generate_future_date(min_years=1, max_years=20):
    """Generates a random future date."""
    days_in_future = random.randint(min_years * 365, max_years * 365)
    return datetime.now() + timedelta(days=days_in_future)

def generate_meeting_note(customer_goals, customer_products):
    """Generates a somewhat plausible meeting note."""
    goal = random.choice(customer_goals)['goal'] if customer_goals else random.choice(MEETING_NOTE_PARTS["misc"])
    product = random.choice(customer_products) if customer_products else random.choice(MEETING_NOTE_PARTS["misc"])
    concern = random.choice(MEETING_NOTE_PARTS["misc"])
    approach = random.choice(MEETING_NOTE_PARTS["misc"])
    strategy = random.choice(MEETING_NOTE_PARTS["misc"])
    emotion = random.choice(MEETING_NOTE_PARTS["misc"])
    future_date = (datetime.now() + timedelta(days=random.randint(30, 90))).strftime('%Y-%m-%d')


    note = f"{random.choice(MEETING_NOTE_PARTS['opening'])} "
    note += random.choice(MEETING_NOTE_PARTS['topic']).format(goal=goal, product=product, concern=concern) + " "
    if random.random() > 0.3: # Add details sometimes
         note += random.choice(MEETING_NOTE_PARTS['details']).format(emotion=emotion) + " "
    if random.random() > 0.2: # Add outcome sometimes
        note += random.choice(MEETING_NOTE_PARTS['outcome']).format(
            approach=approach, strategy=strategy, product=product, goal=goal, future_date=future_date
        )

    note = note.replace("{goal}", random.choice(GOAL_DESCRIPTIONS))
    note = note.replace("{product}", random.choice(BANKING_PRODUCTS))
    note = note.replace("{concern}", random.choice(MEETING_NOTE_PARTS["misc"]))
    note = note.replace("{approach}", random.choice(MEETING_NOTE_PARTS["misc"]))
    note = note.replace("{strategy}", random.choice(MEETING_NOTE_PARTS["misc"]))
    note = note.replace("{emotion}", random.choice(MEETING_NOTE_PARTS["misc"]))
    note = note.replace("{future_date}", (datetime.now() + timedelta(days=random.randint(30, 90))).strftime('%Y-%m-%d'))

    return note.strip()



def seed_advisors():
    if db.advisors.count_documents({}) > 0:
        print("Advisors collection already has data. Skipping seed.")
        return

    advisors = [
        {"name": "Alice Johnson", "email": "alice.johnson@bank.com", "department": "Wealth Management"},
        {"name": "Bob Smith", "email": "bob.smith@bank.com", "department": "Retail Banking"},
        {"name": "Clara Evans", "email": "clara.evans@bank.com", "department": "Business Loans"},
        {"name": "Daniel Mayer", "email": "daniel.mayer@bank.com", "department": "Investments"}
    ]
    db.advisors.insert_many(advisors)
    print(f"Seeded {len(advisors)} advisors.")

def seed_customers(num_customers=20): 
    if db.customers.count_documents({}) > 0:
        print("Customers collection already has data. Skipping seed.")
        return

    advisor_ids = list(db.advisors.find({}, {"_id": 1}))
    if not advisor_ids:
        print("Error: No advisors found. Seed advisors first.")
        return
    advisor_id = random.choice(advisor_ids)["_id"]
    with open("./data/customers.json", "r") as f:
            data = json.load(f)

    if isinstance(data, list):
            for customer in data:
                customer["advisorId"] = ObjectId(advisor_id)
            db.customers.insert_many(data)
    else:
            data["advisorId"] = ObjectId(advisor_id)
            db.customers.insert_one(data)

    print("Seeded customers.")


def seed_database():
    print(f"Using database: {DB_NAME}")


    seed_advisors()
    seed_customers(num_customers=50) # Generate 50 customers

# --- Run the Seeding ---
if __name__ == "__main__":
    seed_database()
    print("Database seeding complete.")
    sample = db.customers.find_one()
    if sample:
        import json
        print("\n--- Sample Customer ---")
        print(json.dumps(sample, indent=2, default=str))
    client.close()