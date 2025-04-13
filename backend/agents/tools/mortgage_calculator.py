from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class MortgageInput(BaseModel):
    principal: float = Field(..., description="Loan amount")
    annual_rate: float = Field(..., description="Annual interest rate in percent")
    years: int = Field(..., description="Loan term in years")
    down_payment: float = Field(0.0, description="Optional down payment")


def amortization_schedule(loan_amount, r, n, monthly):
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
    description: str = "Calculate monthly mortgage payment, total payment, total interest, LTV, and amortization schedule."
    args_schema: Type[BaseModel] = MortgageInput

    def _run(self, principal: float, annual_rate: float, years: int, down_payment: float = 0.0) -> dict:
        loan_amount = principal - down_payment
        r = annual_rate / 100 / 12  # monthly interest rate
        n = years * 12              # total payments

        if r == 0:
            monthly_payment = loan_amount / n
        else:
            monthly_payment = loan_amount * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

        total_payment = monthly_payment * n
        total_interest = total_payment - loan_amount
        ltv = loan_amount / principal

        return {
            "monthly_payment": round(monthly_payment, 2),
            "total_payment": round(total_payment, 2),
            "total_interest": round(total_interest, 2),
            "ltv": round(ltv, 3),
            "amortization_schedule": amortization_schedule(loan_amount, r, n, monthly_payment)
        }

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async not supported")


if __name__ == "__main__":
    tool = MortgageCalculatorTool()
    result = tool.run({
        "principal": 350000,
        "annual_rate": 3.8,
        "years": 25,
        "down_payment": 50000
    })
    from pprint import pprint
    pprint(result)
