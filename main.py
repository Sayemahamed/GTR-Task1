from typing import Literal

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


class TradingBot:
    def __init__(
        self, symbol: str, start_date: str, end_date: str, budget: float = 5000.0
    ):
        self.symbol: str = symbol
        self.start_date: str = start_date
        self.end_date: str = end_date
        self.initial_budget: float = budget
        self.budget: float = budget
        self.shares_held: int = 0
        self.in_position: bool = False
        self.data: pd.DataFrame | None = None
        self.trades = []

    def fetch_data(self) -> bool:
        console = Console()
        console.print(f"[bold blue]Fetching data for {self.symbol}...[/bold blue]")
        self.data = yf.download(
            self.symbol, start=self.start_date, end=self.end_date, auto_adjust=True
        )
        if self.data is None or self.data.empty:
            console.print(
                "[bold red]No data fetched. Check symbol or date range.[/bold red]"
            )
            return False
        self.data.drop_duplicates(inplace=True)
        self.data.ffill(inplace=True)
        console.print("[green]Data fetched and cleaned successfully.[/green]")
        return True

    def calculate_moving_averages(self) -> bool:
        Console().print("[bold blue]Calculating moving averages...[/bold blue]")
        if self.data is None or self.data.empty:
            Console().print(
                "[bold red]Cannot calculate moving averages, no data available.[/bold red]"
            )
            return False
        self.data["MA50"] = self.data["Close"].rolling(window=50).mean()
        self.data["MA200"] = self.data["Close"].rolling(window=200).mean()
        self.data.dropna(inplace=True)
        Console().print("[green]Moving averages calculated.[/green]")
        return True

    def run_strategy(self):
        console = Console()
        console.print("[bold blue]Running trading strategy...[/bold blue]")

        if self.data is None or self.data.empty:
            return
        close_prices = self.data["Close"].to_numpy().flatten()
        ma50_values = self.data["MA50"].to_numpy().flatten()
        ma200_values = self.data["MA200"].to_numpy().flatten()
        trade_dates = self.data.index

        for i in range(1, len(close_prices)):
            prev_ma50 = ma50_values[i - 1]
            prev_ma200 = ma200_values[i - 1]
            curr_ma50 = ma50_values[i]
            curr_ma200 = ma200_values[i]
            curr_price = close_prices[i]
            trade_date = trade_dates[i]

            if (
                prev_ma50 < prev_ma200
                and curr_ma50 > curr_ma200
                and not self.in_position
            ):
                num_shares_to_buy = int(self.budget / curr_price)
                if num_shares_to_buy > 0:
                    self.shares_held = num_shares_to_buy
                    self.budget -= num_shares_to_buy * curr_price
                    self.in_position = True
                    self.trades.append(
                        {
                            "date": trade_date,
                            "price": curr_price,
                            "action": "BUY",
                            "shares": num_shares_to_buy,
                        }
                    )
                    console.print(
                        f"-> [green]BUY[/green]  : {num_shares_to_buy} shares at ${curr_price:.2f} on {trade_date.date()}"
                    )

            elif prev_ma50 > prev_ma200 and curr_ma50 < curr_ma200 and self.in_position:
                self.budget += self.shares_held * curr_price
                self.trades.append(
                    {
                        "date": trade_date,
                        "price": curr_price,
                        "action": "SELL",
                        "shares": self.shares_held,
                    }
                )
                console.print(
                    f"-> [red]SELL[/red] : {self.shares_held} shares at ${curr_price:.2f} on {trade_date.date()}"
                )
                self.shares_held = 0
                self.in_position = False

        if self.in_position:
            last_price = close_prices[-1]
            last_date = trade_dates[-1]
            self.budget += self.shares_held * last_price
            self.trades.append(
                {
                    "date": last_date,
                    "price": last_price,
                    "action": "FORCE SELL",
                    "shares": self.shares_held,
                }
            )
            console.print(
                f"-> [yellow]FORCE SELL[/yellow]: {self.shares_held} shares at ${last_price:.2f} on {last_date.date()} (end of period)."
            )
            self.shares_held = 0
            self.in_position = False

        console.print("[bold blue]Strategy simulation finished.[/bold blue]")

    def display_summary(self):
        console = Console()
        profit_loss: float = self.budget - self.initial_budget
        percentage_return: float = (profit_loss / self.initial_budget) * 100
        profit_style: Literal["bold green"] | Literal["bold red"] = (
            "bold green" if profit_loss >= 0 else "bold red"
        )
        profit_sign: Literal["+"] | Literal[""] = "+" if profit_loss >= 0 else ""
        summary_text = Text(
            text=f"Initial Budget: ${self.initial_budget:,.2f}\n", justify="left"
        )
        summary_text.append(text=f"Final Budget:   ${self.budget:,.2f}\n")
        summary_text.append(
            text=f"Profit/Loss:    {profit_sign}${profit_loss:,.2f} ({profit_sign}{percentage_return:.2f}%)",
            style=profit_style,
        )

        console.print(
            Panel(
                renderable=summary_text,
                title="[bold cyan]Trading Strategy Evaluation[/bold cyan]",
                expand=False,
                border_style="cyan",
            )
        )

        if self.trades:
            trades_table = Table(
                title="[bold]Trade Log[/bold]",
                show_header=True,
                header_style="bold magenta",
            )
            trades_table.add_column(
                header="Date", style="dim", width=12, justify="center"
            )
            trades_table.add_column(header="Action", justify="center")
            trades_table.add_column(header="Shares", justify="right")
            trades_table.add_column(header="Price", justify="right")
            trades_table.add_column(header="Trade Value", justify="right")

            for trade in self.trades:
                action_style: Literal["green"] | Literal["red"] = (
                    "green" if "BUY" in trade["action"] else "red"
                )
                trade_value = trade["shares"] * trade["price"]
                trades_table.add_row(
                    trade["date"].strftime("%Y-m-%d"),
                    f"[{action_style}]{trade['action']}[/]",
                    f"{trade['shares']}",
                    f"${trade['price']:.2f}",
                    f"${trade_value:,.2f}",
                )
            console.print(trades_table)
        else:
            console.print(
                "[yellow]No trades were executed during this period.[/yellow]"
            )

    def plot_results(self):
        if self.data is None or self.data.empty:
            Console().print(
                "[bold red]Cannot plot results, no data available.[/bold red]"
            )
            return
        plt.style.use(style="seaborn-v0_8-darkgrid")
        fig, ax = plt.subplots(figsize=(15, 8))
        ax.plot(
            self.data.index,
            self.data["Close"],
            label="Close Price",
            color="skyblue",
            alpha=0.8,
            linewidth=1.5,
        )
        ax.plot(
            self.data.index,
            self.data["MA50"],
            label="50-Day MA",
            color="orange",
            linestyle="--",
            linewidth=1.2,
        )
        ax.plot(
            self.data.index,
            self.data["MA200"],
            label="200-Day MA",
            color="purple",
            linestyle="--",
            linewidth=1.2,
        )

        if self.trades:
            buy_dates = [
                trade["date"] for trade in self.trades if "BUY" in trade["action"]
            ]
            buy_prices = [
                trade["price"] for trade in self.trades if "BUY" in trade["action"]
            ]
            sell_dates = [
                trade["date"] for trade in self.trades if "SELL" in trade["action"]
            ]
            sell_prices = [
                trade["price"] for trade in self.trades if "SELL" in trade["action"]
            ]

            ax.scatter(
                x=buy_dates,
                y=buy_prices,
                marker="^",
                color="green",
                s=150,
                label="Buy Signal",
                zorder=5,
                edgecolors="black",
            )
            ax.scatter(
                x=sell_dates,
                y=sell_prices,
                marker="v",
                color="red",
                s=150,
                label="Sell Signal",
                zorder=5,
                edgecolors="black",
            )

        ax.set_title(
            label=f"Golden Cross Trading Strategy for {self.symbol}", fontsize=18
        )
        ax.set_xlabel(xlabel="Date", fontsize=12)
        ax.set_ylabel(ylabel="Price (USD)", fontsize=12)
        ax.legend(fontsize=12, loc="upper left")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    trading_bot = TradingBot(
        symbol="AMZN", start_date="2018-01-01", end_date="2023-12-31"
    )

    if trading_bot.fetch_data() and trading_bot.calculate_moving_averages():
        trading_bot.run_strategy()
        print("\n" + "=" * 50 + "\n")
        trading_bot.display_summary()
        trading_bot.plot_results()
