## This is a file that is used to generate a langchain tool for mortgage calculator

from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class MortgageInput(BaseModel):

    principal: float = Field(1000, description="Loan amount")
    annual_rate: float = Field(3.5, description="Annual interest rate in percent")
    years: int = Field(10, description="Loan term in years")
    down_payment: float = Field(0.0, description="Optional down payment")

def amortization_schedule(loan_amount=1000, r=3.5, n=10, monthly=100):
    balance = loan_amount
    schedule = []
    for i in range(1, n + 1):
        interest = balance * r
        principal_payment = monthly - interest
        balance -= principal_payment
        if i % 12 == 0 or i == n:
            schedule.append({
                "year": i // 12,
                "remaining_balance": round(balance, 2),
                "interest_paid": round(interest * 12, 2),
                "principal_paid": round(principal_payment * 12, 2)
            })
    return schedule


class MortgageCalculatorTool(BaseTool):
    name: str = "mortgage_calculator_tool"
    # Total number of payments
    description: str = "Calculate monthly mortgage payment, total payment, total interest, LTV, and amortization schedule. uses interest rate of 3.5% for 10 years with a 1000€ loan if no other values specified. lists the values of the calculation. no markdown"
    args_schema: Type[BaseModel] = MortgageInput

    def _run(self, principal=10000, annual_rate=100, years=10, down_payment=200) -> dict:
        loan_amount = principal - down_payment
        r = annual_rate / 100 / 12  # monthly interest rate
        n = years * 12              # total payments

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
