from langchain.chat_models import azure_openai
from langchain.agents import initialize_agent, AgentType
from dotenv import dotenv_values
import sys, os
# --- End Placeholder ---

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.tools.prices_tool import TopStocksTool
from agents.tools.mortgage_calculator import MortgageCalculatorTool
from agents.tools.retreiver_tool import LocalFileDisplayTool
from agents.tools.user_context import UserContextReplyTool
from langchain.prompts import PromptTemplate
from utils.db_connector import _get_customer_details_from_db
from utils.mock_context import context_manager


class AgentExec:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        config = dotenv_values(config_path)
        self.llm = azure_openai.AzureChatOpenAI(
            openai_api_version="2024-05-01-preview",
            openai_api_base=config.get("endpoint") or os.getenv("AZURE_ENDPOINT"),
            openai_api_key=config.get("api_key") or os.getenv("AZURE_API_KEY"),
            deployment_name=config.get("deployment_name") or os.getenv("AZURE_DEPLOYMENT_ID", "gpt-4o-mini"),
            temperature=0,
        )

        self.tools = [
            TopStocksTool(),
            MortgageCalculatorTool(),
            LocalFileDisplayTool(),
            UserContextReplyTool(context_manager=context_manager, llm= self.llm)
        ]

        self.context_manager = context_manager
        self.agent_executor = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            verbose=True,
            agent=AgentType.OPENAI_FUNCTIONS,
            handle_parsing_errors=True
        )

    def execute(self, user_id: str, query: str):
        # 1. Fetch User Profile Details
        user_details = _get_customer_details_from_db(user_id)
        profile_str = "User Profile: Not Found."
        if user_details:
            # Format the details nicely
            details_list = [f"{key.capitalize()}: {value}" for key, value in user_details.items()]
            profile_str = "User Profile:\n" + "\n".join(details_list)

        # 2. Get Conversation Context
        context_str = self.context_manager.get_context_string(user_id)
        
        # 3. Construct the Full Input for the Agent
        # Add a directive explaining the context is for the current user and can be used
        system_directive = (
            "You are a helpful assistant. The following information pertains ONLY to the user you are currently interacting with. "
            "You ARE permitted to reference and use the details provided in the 'User Profile' and 'Recent Conversation History' sections below "
            "to answer the user's current query. Do not mention information about other users."
        )
        input_parts = [
            system_directive, # Add the new directive first
            f"Current User ID: {user_id}", # Keep user ID info for clarity
            profile_str, # Add the fetched profile string
        ]
        if context_str: # Add context manager output (history, prefs) if it exists
             # Clean up context string
             context_str = context_str.replace("-- User Context --\n", "").replace("\n-- End Context --", "").strip()
             input_parts.append(context_str)
        
        # Combine parts and add the current query
        full_input = "\n\n".join(input_parts) + f"\n\n---\nCurrent User Query: {query}"

        print(f"--- Sending to Agent for {user_id} --- Input --- [see below]")
        print(full_input)
        print("---------------------------------------------")

        # 4. Run the agent
        result = ""
        try:
            result = self.agent_executor.run(full_input)
        except Exception as e:
            print(f"Error during agent execution for user {user_id}: {e}")
            result = "Sorry, I encountered an error processing your request."

        # 5. Store interaction (only if successful)
        if result and "Sorry, I encountered an error" not in result:
            # Store the original, simple query, not the augmented full_input
            self.context_manager.add_interaction(user_id, query, result)
        
        return result
    
if __name__ == "__main__":
    agent_exec = AgentExec()
    # Use the ID that has mock data in the placeholder function
    current_user_id = "67f9ebbe72b23bd97cd9ada3" 
    print(f"Chatting as user: {current_user_id}")

    while True:
        human_input = input(f"[{current_user_id}] Enter your query (or 'exit'): ")
        if human_input.lower() == "exit":
            break
        result = agent_exec.execute(current_user_id, human_input)
        print(f"🧠 [{current_user_id}] {result}")
