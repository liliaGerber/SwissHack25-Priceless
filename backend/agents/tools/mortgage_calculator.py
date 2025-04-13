## This is a file that is used to generate a langchain tool for mortgage calculator

from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class MortgageInput(BaseModel):
    principal: float = Field(..., description="Loan amount or Principal in currency units")


class MortgageCalculatorTool(BaseTool):
    name: str = "mortgage_calculator_tool"
    description:str = "Calculate monthly mortgage payment, total payment, and total interest"
    args_schema: Type[BaseModel] = MortgageInput

    def _run(self, principal: float) -> dict:
        annual_rate = 3.5
        years = 30
        r = annual_rate / 100 / 12  # Monthly interest rate
        n = years * 12              # Total number of payments

        if r == 0:
            monthly_payment = principal / n
        else:
            monthly_payment = principal * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

        total_payment = monthly_payment * n
        total_interest = total_payment - principal

        return {
            "monthly_payment": round(monthly_payment, 2),
            "total_payment": round(total_payment, 2),
            "total_interest": round(total_interest, 2)
        }

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not supported")

if __name__ == "__main__":
    tool = MortgageCalculatorTool()

    result = tool.run({
        "principal": 300000,   # € or $ 
    })

    print(result)
