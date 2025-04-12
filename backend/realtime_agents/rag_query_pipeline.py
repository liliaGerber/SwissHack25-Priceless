from sentence_transformers import SentenceTransformer
import chromadb
import ollama
from typing import List

MODEL_NAME = 'all-MiniLM-L6-v2'
CHROMA_COLLECTION_NAME = "mongo_rag"
LLM_MODEL = 'gemma3:1b'


def initialize_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def get_chroma_collection(name: str) -> chromadb.api.models.Collection.Collection:
    client = chromadb.Client()
    return client.get_collection(name=name)


def retrieve_context(question: str, model: SentenceTransformer, collection: chromadb.api.models.Collection.Collection, top_k: int = 3) -> str:
    question_embedding = model.encode(question).tolist()
    results = collection.query(query_embeddings=[question_embedding], n_results=top_k)
    return "\n".join(results["documents"][0])


def ask_llm(context: str, question: str) -> str:
    prompt = f"Context:\n{context}\n\nQuestion: {question}"
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']


def query_rag(question: str) -> str:
    embed_model = initialize_embedding_model()
    chroma_collection = get_chroma_collection(CHROMA_COLLECTION_NAME)
    context = retrieve_context(question, embed_model, chroma_collection)
    return ask_llm(context, question)


if __name__ == "__main__":
    user_question = "What is the policy on user access rights?"
    answer = query_rag(user_question)
    print("Answer:", answer)
