import docx
import pandas as pd
import sqlite3
import yake

PRODUCTS = [
    "Beratungsmandat", "Festhypothek", "Mastercard", "TWINT",
    "Sparkonto", "Visa Card", "Variable Hypothek", "Vermögensverwaltungsmandat"
]

SECTIONS = [
    "Überblick", "Vorteile", "Leistungen", "Risiken", "Konditionen",
    "Produktinformationen", "Funktionen", "Onlineservice",
    "Versicherungsleistungen", "Anpassungsmöglichkeiten", "Häufige Fragen"
]

# Extract Keywords using YAKE
kw_extractor = yake.KeywordExtractor(lan="de", n=3, top=5)

def extract_keywords(text):
    text = str(text).strip()
    if pd.isna(text) or len(text.split()) < 5:
        return ""  # Leave empty if too short
    keywords = kw_extractor.extract_keywords(text)
    return ", ".join([kw[0] for kw in keywords])

# Parse DOCX File
def parse_docx(file_path):
    doc = docx.Document(file_path)
    products_data = []
    current_product = None
    current_section = None

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        if text in PRODUCTS:
            if current_product:
                products_data.append(current_product)
            current_product = {"Produktname": text}
            for section in SECTIONS:
                current_product[section] = ""
            current_section = None
            continue

        if text in SECTIONS:
            current_section = text
            continue

        if current_section and current_product:
            current_product[current_section] += " " + text

    if current_product:
        products_data.append(current_product)

    return pd.DataFrame(products_data)


if __name__ == "__main__":
    file_path = "../../data/raiffeisenprodukte_final.docx"

    # Step 1 — Extract Raw Text
    df_raw = parse_docx(file_path)
    df_raw.to_csv("raiffeisen_full_text.csv", index=False)

    # Step 2 — Extract Keywords using YAKE
    df_keywords = df_raw.copy()

    for section in SECTIONS:
        print(f"Extracting keywords for section: {section}")
        df_keywords[section] = df_raw[section].apply(extract_keywords)

    # Step 3 — Save Keywords to CSV
    df_keywords.to_csv("raiffeisen_keywords_final.csv", index=False)

    # Step 4 — Save to SQLite DB
    conn = sqlite3.connect("raiffeisen.db")
    df_keywords.to_sql("products", conn, if_exists="replace", index=False)

    print("Finished successfully: Text extracted, Keywords written into CSV + DB!")
