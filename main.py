import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

class TradingBot:
    def __init__(self,symbol:str,start_date:str,end_date:str,budget:float=10000) -> None:
        self.symbol: str = symbol
        self.start_date: str = start_date
        self.end_date: str = end_date
        self.initial_budget: float = budget
        self.budget: float = budget
        self.shares_purchased: int = 0
        self.in_position: bool = False
        self.data:pd.DataFrame|None=None
        self.trades=[]
    def fetch_data(self)->bool:
        Console().print(f"[bold blue]Fetching data for {self.symbol} from {self.start_date} to {self.end_date}")
        try:
            self.data = yf.download(tickers=self.symbol, start=self.start_date, end=self.end_date,auto_adjust=True)
            Console().print(f"[bold green]Data fetched for {self.symbol}")
        except Exception as e:
            Console().print(f"[bold red]Error fetching data for {self.symbol}: {e}")
            return False
        if self.data is None or self.data.empty:
            Console().print(f"[yellow]No data found for {self.symbol} between {self.start_date} and {self.end_date}")
            return False
        self.data.drop_duplicates(inplace=True)
        self.data.ffill(inplace=True)
        Console().print("[bold green]Data Processed Successfully")
        return True
    
    def calculate_moving_average(self)->bool:
        Console().print("[bold blue]Calculating Moving Average")
        if self.data is None or self.data.empty:
            Console().print(f"[yellow]No data found for {self.symbol} between {self.start_date} and {self.end_date}")
            return False
        self.data["MA50"] = self.data["Close"].rolling(window=50).mean()
        self.data["MA200"] = self.data["Close"].rolling(window=200).mean()
        Console().print("[bold green]Moving Average Calculated Successfully")
        return True




if __name__ == "__main__":
    trading_bot:TradingBot = TradingBot(
        symbol="AMZN",
        start_date="2018-01-01",
        end_date="2023-12-31"
    )
    
    if trading_bot.fetch_data() and trading_bot.calculate_moving_average():
        pass
    else:
        pass