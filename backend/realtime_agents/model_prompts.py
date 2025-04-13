from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
collection = client["your_db"]["your_collection"]

# Load documents
documents = []
for doc in collection.find():
    text = f"Title: {doc.get('title', '')}\nContent: {doc.get('content', '')}"
    documents.append(text)

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Setup ChromaDB
chroma_client = chromadb.Client(Settings(persist_directory="db"))
collection = chroma_client.create_collection(name="mongo_rag")

# Index documents
for i, doc in enumerate(documents):
    embedding = model.encode(doc).tolist()
    collection.add(documents=[doc], ids=[str(i)], embeddings=[embedding])
