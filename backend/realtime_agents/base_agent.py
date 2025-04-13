import ollama
from pymongo import MongoClient

# === Constants ===
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "raiffeisen"
COLLECTION_NAME = "customers"


class ContextualRAGAgent:
    def __init__(self, llm_model: str, prompt: str):
        self.llm_model = llm_model
        self.prompt = prompt
        self.mongo_client = MongoClient(MONGO_URI)
        self.collection = self.mongo_client[DB_NAME][COLLECTION_NAME]

    def get_context(self, customer: str) -> str:
        documents = []
        for doc in self.collection.find({"id": customer}):
            text = "\n".join(f"{key}: {value}" for key, value in doc.items() if key != "id")
            if text.strip():
                documents.append(text)
        if not documents:
            return "No relevant context found."
        return "\n".join(doc[:500] for doc in documents)

    def build_prompt(self, question: str, context: str) -> str:
        return (
            "Answer the question using the context below."
            f"Instructions:\n{self.prompt}"
            f"Context:\n{context}\n"
            f"Question: {question}"
        )

    def query(self, question: str, customer: str, top_k: int = 3) -> str:
        context = self.get_context(customer)
        prompt = self.build_prompt(question, context)
        response = ollama.chat(model=self.llm_model, messages=[{"role": "user", "content": prompt}])
        return response['message']['content']


if __name__ == "__main__":
    agent = ContextualRAGAgent(
        llm_model='gemma3:1b',
        prompt='Tell me as much as you know'
    )
    customer_id = "67faa98e6fdf05b5f7261303"
    question = "What can you tell me about the customers?"
    print("Question:", question)
    print("Answer:\n", agent.query(question, customer_id))
