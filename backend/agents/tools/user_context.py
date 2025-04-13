import os
from collections import defaultdict
from typing import Type, Dict, Any
from dotenv import dotenv_values

# --- Core LangChain Imports ---
from langchain_core.tools import BaseTool
from langchain_core.pydantic_v1 import BaseModel, Field # Use v1 for tool compatibility if needed
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_core.language_models.llms import BaseLLM # To type hint the LLM

from langchain.chat_models import azure_openai
from typing import Optional


# --- User Context Management (Slightly Modified) ---
class UserContextManager:
    """Manages in-memory context for different users."""
    def __init__(self):
        self._context_store = defaultdict(lambda: {"history": [], "preferences": {}})

    def add_interaction(self, user_id: str, query: str, response: str):
        """Adds a query-response pair to the user's history."""
        history = self._context_store[user_id]["history"]
        history.append(f"User: {query}")
        history.append(f"Agent: {response}")
        max_history_items = 10
        if len(history) > max_history_items:
            self._context_store[user_id]["history"] = history[-max_history_items:]

    def update_preference(self, user_id: str, key: str, value: any):
        """Stores or updates a user preference."""
        self._context_store[user_id]["preferences"][key] = value

    def get_context_string(self, user_id: str, mock: bool = False) -> str: # Default mock to False
        """Retrieves the user's context formatted as a string for prompt injection."""
        if mock: # Keep mock option for direct testing if needed, but tool won't use it
             user_text = f"""
            Name: Olia
            Hobbies: Horse riding
            Email: olia@example.com
            Status: Premium
            balance: 88888.88
            avoidTopics: Divorce/Separation, Past Bankruptcy
            """
             return user_text

        user_data = self._context_store[user_id]
        context_parts = []

        # Add preferences if any
        if user_data["preferences"]:
            prefs = ", ".join([f'{k}="{v}"' for k, v in user_data["preferences"].items()])
            context_parts.append(f"User Preferences: [{prefs}]")

        # Add history if any
        if user_data["history"]:
            history_str = "\n".join(user_data["history"])
            context_parts.append(f"Recent Conversation History:\n{history_str}")

        if not context_parts:
            return "No context available for this user." # Provide a default string

        # Format the context clearly
        return "-- User Context --\n" + "\n\n".join(context_parts) + "\n-- End Context --"

    def get_preference(self, user_id: str, key: str):
        """Retrieves a specific preference."""
        return self._context_store[user_id]["preferences"].get(key)

# --- Tool Definition with Internal Chain ---

# 1. Define Input Schema for the Tool
class UserContextReplyInput(BaseModel):
    user_id: str = Field(description="The unique identifier for the user.")
    query: str = Field(description="The specific question the user is asking.")

# 2. Define the Tool
class UserContextReplyTool(BaseTool):
    name: str = "UserContextReply"
    description: str = (
        "Answers user queries based on their stored context (history, preferences). "
        "Use this tool when the user asks questions about themselves, their past interactions, or preferences."
    )
    args_schema: Type[BaseModel] = UserContextReplyInput

    # Dependencies needed by the tool
    context_manager: Optional[UserContextManager] = None
    llm: Optional[BaseLLM] = None
    chain: Optional[LLMChain] = None # Initialize chain later

    def __init__(self, context_manager: UserContextManager, llm: BaseLLM, **kwargs):
        super().__init__(**kwargs) # Initialize BaseTool first

        # Store dependencies
        self.context_manager = context_manager
        self.llm = llm

        # Define the prompt template for the internal chain
        prompt_template = """
You are a helpful assistant accessing specific information about a user.
Use the provided context ONLY to answer the user's query.
If the context does not contain the information needed to answer the query, state that clearly.
Do not make up information. Be concise and directly answer the question based on the context.

{context}

User Query: {query}

Answer:
"""
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "query"]
        )

        # Initialize the internal LLMChain
        self.chain = LLMChain(llm=self.llm, prompt=prompt)

    def _run(self, user_id: str, query: str, **kwargs) -> str:
        """Executes the tool's logic."""
        # 1. Fetch context for the user
        user_context = self.context_manager.get_context_string(user_id)

        # 2. Run the internal chain with the context and query
        # Use .invoke for newer LangChain versions or .run for older ones
        try:
            # Newer Langchain versions prefer invoke
            result = self.chain.invoke({"context": user_context, "query": query})
            # The result is often a dictionary, extract the text response
            answer = result.get('text', "Error: Could not extract answer from LLM response.")
        except AttributeError:
            # Fallback for older versions using run
            answer = self.chain.run(context=user_context, query=query)
        except Exception as e:
            return f"Error executing internal chain: {e}"

        return answer.strip()

    # Optional: Implement async version if needed
    # async def _arun(self, user_id: str, query: str) -> str:
    #     """Executes the tool's logic asynchronously."""
    #     user_context = self.context_manager.get_context_string(user_id)
    #     try:
    #         result = await self.chain.ainvoke({"context": user_context, "query": query})
    #         answer = result.get('text', "Error: Could not extract answer from LLM response.")
    #     except AttributeError:
    #          answer = await self.chain.arun(context=user_context, query=query)
    #     except Exception as e:
    #         return f"Error executing internal chain asynchronously: {e}"
    #     return answer.strip()


# --- Example Usage ---
if __name__ == '__main__':
    # 1. Initialize User Context Manager
    context_manager = UserContextManager()
    user1 = 'user_abc'
    user2 = 'user_xyz'

    # 2. Populate some context
    context_manager.add_interaction(user1, "What's the weather?", "It's sunny.")
    context_manager.add_interaction(user1, "What about tomorrow?", "Expecting rain.")
    context_manager.update_preference(user1, 'location', 'London')
    context_manager.update_preference(user1, 'email', 'olia@example.com') # Add email based on mock
    context_manager.update_preference(user1, 'status', 'Premium')       # Add status based on mock

    context_manager.add_interaction(user2, "Recommend a book", "Try 'Project Hail Mary'.")
    context_manager.update_preference(user2, 'genre', 'Sci-Fi')

    print("--- Context Setup ---")
    print(f"Context for {user1}:\n{context_manager.get_context_string(user1)}\n")
    print(f"Context for {user2}:\n{context_manager.get_context_string(user2)}\n")

    # 3. Initialize a (Fake) LLM for demonstration
    # Responses the FakeLLM will cycle through
    responses = [
        "Based on your preferences, your email is olia@example.com.",
        "Your status is Premium.",
        "According to your conversation history, the agent expected rain for tomorrow.",
        "Based on your preferences, you like the Sci-Fi genre.",
        "I don't have information about your balance in the provided context.",
    ]
    config = dotenv_values(os.path.join(os.path.dirname(__file__), "..", ".env"))

    fake_llm = azure_openai.AzureChatOpenAI(
            openai_api_version="2024-05-01-preview",
            openai_api_base=config["endpoint"],
            openai_api_key=config["api_key"],
            model_name="gpt-4o-mini",
            deployment_name="gpt-4o-mini",
            temperature=0,
        )


    # 4. Initialize the Tool
    context_tool = UserContextReplyTool(context_manager=context_manager, llm=fake_llm)

    # 5. Use the Tool
    print("--- Tool Execution ---")

    query1 = "What is my email address?"
    print(f"User Query ({user1}): {query1}")
    response1 = context_tool.run(tool_input={"user_id": user1, "query": query1})
    print(f"Tool Response: {response1}\n")

    query2 = "What's my account status?"
    print(f"User Query ({user1}): {query2}")
    response2 = context_tool.run(tool_input={"user_id": user1, "query": query2})
    print(f"Tool Response: {response2}\n")

    query3 = "What did you say about tomorrow's weather?"
    print(f"User Query ({user1}): {query3}")
    response3 = context_tool.run(tool_input={"user_id": user1, "query": query3})
    print(f"Tool Response: {response3}\n")

    query4 = "What genre do I like?"
    print(f"User Query ({user2}): {query4}")
    response4 = context_tool.run(tool_input={"user_id": user2, "query": query4})
    print(f"Tool Response: {response4}\n")

    query5 = "What's my current balance?" # Info not in context
    print(f"User Query ({user1}): {query5}")
    response5 = context_tool.run(tool_input={"user_id": user1, "query": query5})
    print(f"Tool Response: {response5}\n") # FakeLLM might still respond if not prompted well
                                           # A real LLM should follow instructions better.