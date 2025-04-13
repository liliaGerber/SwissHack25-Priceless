import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from base_agent import ContextualRAGAgent


class InvestmentRAGAgent(ContextualRAGAgent):
    def __init__(self):
        super().__init__(
            llm_model="mistral:7b-instruct",
            prompt="You are an investment advisor. Answer the client's question using the context provided. If the context lacks sufficient data, say 'Not enough data to provide advice.'\n\n"
        )


class RetirementRAGAgent(ContextualRAGAgent):
    def __init__(self):
        super().__init__(
            llm_model="mistral:7b-instruct",
            prompt="As a retirement planner, answer this question using only the customer data context.\n\n"
        )

class PlanMyMeetingAgent(ContextualRAGAgent):
    def __init__(self):
        super().__init__(
            llm_model="llama3.2",
            prompt="Based on the context you are planning a one hour meeting between you, the advisor and your customer. what do you want to tak about with the customer? Whats important? How do you time it? The output is a whole meeting plan\n\n"
        )


class SummaryRAGAgent(ContextualRAGAgent):
    def __init__(self):
        super().__init__(
            llm_model="mistral:7b-instruct",
            prompt="Read the customer data and generate a comprehensive summary about the customer's financial profile, behavior, goals, and history.\n\n"
        )


class InteractionAdvisorRAGAgent(ContextualRAGAgent):
    def __init__(self):
        super().__init__(
            "tinyllama",
            prompt="You are an advisor assistant. Using the customer data, give a conversation-ready overview and provide recommendations on how best to interact with the customer based on behavior, preferences, and communication style.\n\n"
        )


class VisionRAGAgent(ContextualRAGAgent):
    def __init__(self):
        super().__init__(
            llm_model="mistral:7b-instruct",
            prompt="Imagine future opportunities and needs for the customer. Based on the customer data, generate insightful suggestions and visionary ideas about services, products, or support that could benefit them.\n\n"
        )


class RealTimeAgent(ContextualRAGAgent):
    def __init__(self):
        super().__init__(
            llm_model="gemma3:1b",
            prompt="You are an agent who answers in real-time, providing short important insights to an advisory during a meeting.\n\n"
        )

# Example usage:
# agent = SummaryRAGAgent()
# answer = agent.query("Generate a customer summary.", "customer_id_here")
