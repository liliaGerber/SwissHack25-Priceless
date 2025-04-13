from langchain.chat_models import azure_openai
from langchain.agents import initialize_agent, AgentType
from dotenv import dotenv_values
from tools.prices_tool import TopStocksTool
from tools.mortgage_calculator import MortgageCalculatorTool
from tools.retreiver_tool import LocalFileDisplayTool
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate


class AgentExec:
    def __init__(self):
        config = dotenv_values(".env")
        self.llm = azure_openai.AzureChatOpenAI(
            openai_api_version="2024-05-01-preview",
            openai_api_base=config["endpoint"],
            openai_api_key=config["api_key"],
            model_name="gpt-4o-mini",
            deployment_name="gpt-4o-mini",
            temperature=0,
        )

        self.tools = [
            TopStocksTool(),
            MortgageCalculatorTool(),
            LocalFileDisplayTool(),
        ]
        self.memory = ConversationBufferMemory()

        self.agent_executor = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            verbose=True,
            memory=self.memory,
            agent=AgentType.OPENAI_FUNCTIONS,
        )

    def execute(self, query):
        result = self.agent_executor.run(query)
        return result
    
if __name__ == "__main__":
    agent_exec = AgentExec()
    human_input = "Tell me about the top stocks."
    while human_input.lower() != "exit":
        result = agent_exec.execute(human_input)
        print(result)
        human_input = input("Enter your query: ")
