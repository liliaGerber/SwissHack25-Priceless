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

context_manager = UserContextManager()
user1 = '67f9ebbe72b23bd97cd9ada3'
user2 = 'Lilia Schmidt'

# 2. Populate some context
context_manager.add_interaction(user1, "What's the weather?", "It's sunny.")
context_manager.add_interaction(user1, "What about tomorrow?", "Expecting rain.")
context_manager.update_preference(user1, 'location', 'London')
context_manager.update_preference(user1, 'status', 'Premium')       # Add status based on mock

context_manager.add_interaction(user2, "Recommend a book", "Try 'Project Hail Mary'.")
context_manager.update_preference(user2, 'genre', 'Sci-Fi')
