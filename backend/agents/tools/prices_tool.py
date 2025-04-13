### This is a langchain tool that obtains the prices for s&p500, nasdaq, and dow jones
from typing import Any, Dict, List, Tuple
from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import tempfile
import os


class MarketInput(BaseModel):
    market: str = Field(..., description="The equity market name like NASDAQ, NYSE, NSE")


class TopStocksTool(BaseTool):
    name:str = "top_stocks_tool"
    description: str = "Fetches top 3 performing stocks in a given equity market over the last 3 days and generates a price plot."
    args_schema: Type[BaseModel] = MarketInput

    def _run(self, market: str):
        market_tickers = {
            "NASDAQ": ["AAPL", "MSFT", "NVDA", "GOOG", "META", "AMZN", "TSLA"],
            "NYSE": ["JNJ", "PG", "V", "UNH", "MA", "KO"],
            "NSE": ["INFY.NS", "TCS.NS", "RELIANCE.NS", "HDFCBANK.NS", "ICICIBANK.NS"]
        }

        tickers = market_tickers.get(market.upper())
        if not tickers:
            return f"Market {market} not supported."

        data = yf.download(tickers, period="5d")

        # Calculate returns over last 3 trading days
        returns = (data.iloc[-1] - data.iloc[-4]) / data.iloc[-4]
        top_stocks = returns.nlargest(3).index.tolist()

        # Plotting

        ## show the plot for 5 secs and then close it
        plt.figure(figsize=(10, 6))
        for stock in top_stocks:
            plt.plot(data.index[-3:], data[stock].iloc[-3:], label=stock)

        plt.title(f"Top 3 Stocks in {market} - Last 3 Days Performance")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.grid(True)
        plt.legend(top_stocks)
        plt.pause(5)
        plt.close()

    async def _arun(self, market: str):
        raise NotImplementedError("Async not supported")

if __name__ == "__main__":
    # Example usage
    tool = TopStocksTool()

    result = tool.run({"market": "NASDAQ"})