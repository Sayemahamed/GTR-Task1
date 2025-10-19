import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

class TradingBot:
    def __init__(self,symbol:str,start_date:str,end_date:str,budget:float=5000) -> None:
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
        console = Console()
        console.print(f"[bold blue]Fetching data for {self.symbol} from {self.start_date} to {self.end_date}[/bold blue]")
        try:
            self.data = yf.download(tickers=self.symbol, start=self.start_date, end=self.end_date,auto_adjust=True)
            console.print(f"[bold green]Data fetched for {self.symbol}[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Error fetching data for {self.symbol}: {e}[/bold red]")
            return False
        if self.data is None or self.data.empty:
            console.print(f"[yellow]No data found for {self.symbol} between {self.start_date} and {self.end_date}[/yellow]")
            return False
        self.data.drop_duplicates(inplace=True)
        self.data.ffill(inplace=True)
        console.print("[bold green]Data Processed Successfully[/bold green]")
        return True
    
    def calculate_moving_average(self)->bool:
        Console().print("[bold blue]Calculating Moving Average[/bold blue]")
        if self.data is None or self.data.empty:
            Console().print(f"[yellow]No data found for {self.symbol} between {self.start_date} and {self.end_date}[/yellow]")
            return False
        self.data["MA50"] = self.data["Close"].rolling(window=50).mean()
        self.data["MA200"] = self.data["Close"].rolling(window=200).mean()
        Console().print("[bold green]Moving Average Calculated Successfully[/bold green]")
        return True
    
    def run_strategy(self):
        Console().print("[bold blue]Running Trading Strategy[/bold blue]")
        if self.data is None or self.data.empty:
            Console().print(f"[yellow]No data found for {self.symbol} between {self.start_date} and {self.end_date}[/yellow]")
            return False
        
        close_prices = self.data['Close'].to_numpy().flatten()
        ma50_values = self.data['MA50'].to_numpy().flatten()
        ma200_values = self.data['MA200'].to_numpy().flatten()
        trade_dates = self.data.index

        for i in range(1, len(close_prices)):
            prev_ma50 = ma50_values[i-1]
            prev_ma200 = ma200_values[i-1]
            
            curr_ma50 = ma50_values[i]
            curr_ma200 = ma200_values[i]
            curr_price = close_prices[i]
            trade_date = trade_dates[i]

            if prev_ma50 < prev_ma200 and curr_ma50 > curr_ma200 and not self.in_position:
                num_shares_to_buy = int(self.budget / curr_price)
                if num_shares_to_buy > 0:
                    self.shares_held = num_shares_to_buy
                    self.budget -= num_shares_to_buy * curr_price
                    self.in_position = True
                    self.trades.append({'date': trade_date, 'price': curr_price, 'action': 'BUY', 'shares': num_shares_to_buy})
                    Console().print(f"-> [green]BUY[/green]  : {num_shares_to_buy} shares at ${curr_price:.2f} on {trade_date.date()}")

            elif prev_ma50 > prev_ma200 and curr_ma50 < curr_ma200 and self.in_position:
                self.budget += self.shares_held * curr_price
                self.trades.append({'date': trade_date, 'price': curr_price, 'action': 'SELL', 'shares': self.shares_held})
                Console().print(f"-> [red]SELL[/red] : {self.shares_held} shares at ${curr_price:.2f} on {trade_date.date()}")
                self.shares_held = 0
                self.in_position = False

        if self.in_position:
            last_price = close_prices[-1]
            last_date = trade_dates[-1]
            self.budget += self.shares_held * last_price
            self.trades.append({'date': last_date, 'price': last_price, 'action': 'FORCE SELL', 'shares': self.shares_held})
            Console().print(f"-> [yellow]FORCE SELL[/yellow]: {self.shares_held} shares at ${last_price:.2f} on {last_date.date()} (end of period).")
            self.shares_held = 0
            self.in_position = False
        
        Console().print("[bold blue]Strategy simulation finished.[/bold blue]")




if __name__ == "__main__":
    trading_bot:TradingBot = TradingBot(
        symbol="AMZN",
        start_date="2018-01-01",
        end_date="2023-12-31"
    )
    
    if trading_bot.fetch_data() and trading_bot.calculate_moving_average():
        trading_bot.run_strategy()
    else:
        pass
