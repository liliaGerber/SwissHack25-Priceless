import pandas as pd
import yake
from pymongo import MongoClient

df_raw = pd.read_csv("raiffeisen_full_text.csv")

# Initialize YAKE for German
kw_extractor = yake.KeywordExtractor(lan="de", n=3, top=5)

def extract_keywords(text):
    text = str(text).strip()
    if pd.isna(text) or len(text.split()) < 5:
        return ""  # Leave empty if too short
    keywords = kw_extractor.extract_keywords(text)
    return ", ".join([kw[0] for kw in keywords])

df_keywords = df_raw.copy()

for column in df_keywords.columns:
    if column == "Produktname":
        continue
    print(f"Extracting keywords for section: {column}")
    df_keywords[column] = df_raw[column].apply(extract_keywords)

# Convert DataFrame to dictionary
data_to_insert = df_keywords.to_dict(orient="records")

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Change to your MongoDB connection string if needed
db = client["raiffeisen_db"]
collection = db["products"]

# Insert data
collection.delete_many({})  # Optional: Clean previous data
collection.insert_many(data_to_insert)

print("✓ YAKE keywords written successfully to MongoDB!")
