import os
import sys
from dotenv import dotenv_values
from concurrent.futures import ThreadPoolExecutor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.tools.prices_tool import TopStocksTool
from agents.tools.mortgage_calculator import MortgageCalculatorTool
from agents.tools.retreiver_tool import LocalFileDisplayTool
from langchain_community.chat_models import AzureChatOpenAI


class AgentExec:
    def __init__(self):
        config = dotenv_values(os.path.join(os.path.dirname(__file__), "..", ".env"))

        self.llm = AzureChatOpenAI(
            openai_api_version="2024-05-01-preview",
            azure_endpoint=config["endpoint"],  # ✅ use proper key
            openai_api_key=config["api_key"],
            model_name="gpt-4o-mini",
            deployment_name="gpt-4o-mini",
            temperature=0,
        )

        self.tools = {
            "mortgage": MortgageCalculatorTool(),
            "stocks": TopStocksTool(),
            "file": LocalFileDisplayTool(),
        }

        self.executor = ThreadPoolExecutor(max_workers=2)

    def route_and_execute(self, query: str) -> str:
        query_lower = query.lower()

        # --- Simple tool routing ---
        if "mortgage" in query_lower:
            return self.tools["mortgage"].run({"principal": 300000})
        elif "stocks" in query_lower or "stock" in query_lower:
            return self.tools["stocks"].run({"market": "US"})
        elif "file" in query_lower or "read" in query_lower:
            return self.tools["file"].run({"filename": "example.txt"})

        # --- Fallback to direct LLM call ---
        response = self.llm.invoke(query)
        return f"💬 AI: {response.content.strip()}"

    def execute(self, query: str) -> str:
        """Threaded execution for non-blocking use in real-time contexts."""
        future = self.executor.submit(self.route_and_execute, query)
        return future.result()


if __name__ == "__main__":
    agent_exec = AgentExec()
    user_input = input("🔍 Enter your query: ")
    while user_input.lower() != "exit":
        print("⚙️  Running...")
        output = agent_exec.execute(user_input)
        print("🧠", output)
        user_input = input("🔍 Enter your query: ")
