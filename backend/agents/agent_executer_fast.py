import os
import sys
from dotenv import dotenv_values
from concurrent.futures import ThreadPoolExecutor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.tools.prices_tool import TopStocksTool
from agents.tools.mortgage_calculator import MortgageCalculatorTool
from agents.tools.retreiver_tool import LocalFileDisplayTool
from agents.tools.user_context import UserContextManager
from langchain_community.chat_models import AzureChatOpenAI


class AgentExecFast:
    def __init__(self):
        config = dotenv_values(os.path.join(os.path.dirname(__file__), "..", ".env"))

        self.llm = AzureChatOpenAI(
            openai_api_version="2024-05-01-preview",
            openai_api_base=config["endpoint"],
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
        self.context_manager = UserContextManager()

    def route_and_execute(self, user_id: str, query: str) -> str:
        query_lower = query.lower()
        response = None
        tool_used = False

        # --- Simple tool routing ---
        print("Here in simple routing")
        if "mortgage" in query_lower:
            response = self.tools["mortgage"].run({"principal": 300000})
            tool_used = True
        elif "stocks" in query_lower or "stock" in query_lower:
            response = self.tools["stocks"].run({})
            tool_used = True
        elif "file" in query_lower or "read" in query_lower:
            response = self.tools["file"].run({"filename": "example.txt"})
            tool_used = True

        # --- Fallback to direct LLM call with context ---
        if not tool_used:
            context_str = self.context_manager.get_context_string(user_id)
            prompt_with_context = f"{context_str}{query}"
            print(f"--- Sending to LLM with Context for {user_id} ---")
            print(prompt_with_context)
            print("------------------------------------------------")
            llm_response = self.llm.invoke(prompt_with_context)
            response = llm_response.content
            print(response)
        
        # --- Add interaction to context ---
        if response:
            self.context_manager.add_interaction(user_id, query, response)
            
        return response or "Sorry, I could not process that."

    def execute(self, user_id: str, query: str) -> str:
        """Threaded execution for non-blocking use in real-time contexts."""
        future = self.executor.submit(self.route_and_execute, user_id, query)
        return future.result()


if __name__ == "__main__":
    agent_exec = AgentExecFast()
    current_user_id = "test_user_01"
    print(f"Chatting as user: {current_user_id}")

    while True:
        user_input = input(f"[{current_user_id}] Enter your query (or 'exit'): ")
        if user_input.lower() == "exit":
            break
        output = agent_exec.execute(current_user_id, user_input)
        print(f"🧠 [{current_user_id}] {output}")
