import ollama
from bson import ObjectId
from pymongo import MongoClient

# === Config ===
MODEL_NAME = 'all-MiniLM-L6-v2'
LLM_MODEL = 'gemma3:1b'
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "raiffeisen"
COLLECTION_NAME = "customers"



def get_context(customer_id: str):
    documents = []
    mongo_collection = MongoClient(MONGO_URI)[DB_NAME][COLLECTION_NAME]
    print("Customerid: ", customer_id)
    for doc in mongo_collection.find({"id": customer_id}):
        text = "\\n".join(f"{key}: {value}" for key, value in doc.items() if key != "id")
        if text.strip():
            documents.append(text)
    print("User found: ", documents)
    if not documents:
        return "No relevant context found."

    context = "\n".join(doc[:500] for doc in documents)
    return context


def query_rag(question: str, customer_id: str, top_k: int = 3):
    context = get_context(customer_id)
    prompt = (
        "Answer the question using the context below. "
        "If the context is not helpful, say 'Not enough information.'\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer:"
    )
    response = ollama.chat(model=LLM_MODEL, messages=[{"role": "user", "content": prompt}])
    return response['message']['content']


if __name__ == "__main__":
    customer = "67faa98e6fdf05b5f7261303"
    q = "What can you tell me about the customers?"
    print("Question: ", q)
    answer = query_rag(q, customer)
    print("Answer:\n", answer)
