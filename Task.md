# 💹 Algorithmic Trading Adventure — Task 1

## 🧭 Task Description

**Scenario:**  
Alex, a budding programmer and finance enthusiast, embarks on an **algorithmic trading adventure** with a budget of **$5000**.  
Their mission is to develop a Python-based tool that can make informed decisions in the stock market using a **class-based approach** for flexibility.

**Task Steps:**
1. **Initialize a Class** to encapsulate the trading strategy with parameters such as stock symbol, start date, and end date.  
   Example: `Class_Name("AAPL", "2018-01-01", "2023-12-31")`
2. **Install `yfinance`** to access historical market data.  
3. **Download historical data** for the specified symbol and date range.  
4. **Clean the data** — remove duplicates and handle missing values (forward fill).  
5. **Compute moving averages** for 50-day and 200-day periods.  
6. **Detect the Golden Cross** — when the 50-day MA crosses above the 200-day MA (buy signal).  
7. **Investment Strategy:**  
   - Buy the maximum number of shares possible within the $5000 budget.  
   - When the cross reverses (Death Cross), sell all shares.  
   - Only one position can be held at a time.  
8. **Force close** any open position at the last date of the dataset.  
9. **Evaluate** performance — calculate total profit or loss to assess the strategy’s success.

---

## 🧠 Theoretical Background

### 📊 Algorithmic Trading
Algorithmic trading (or **algo-trading**) is the process of using computer algorithms to automatically execute trading strategies.  
It allows traders to make data-driven decisions faster and without emotion.

### ⚖️ Moving Averages
A **moving average (MA)** smooths price data to identify trends over time:
- **Short-term MA (50-day):** Captures short-term market direction.  
- **Long-term MA (200-day):** Reflects overall market trend.

### 🌟 Golden Cross & Death Cross
- **Golden Cross:** When the 50-day MA crosses **above** the 200-day MA → **Bullish signal** → Buy.  
- **Death Cross:** When the 50-day MA crosses **below** the 200-day MA → **Bearish signal** → Sell.  

This combination is one of the simplest yet most widely used strategies in technical analysis.

### 💰 Objective
The goal is to **simulate and evaluate** this trading strategy to understand:
- How technical indicators guide trading decisions.  
- How automated logic affects investment outcomes.  
- The balance between potential reward and risk in algorithmic trading.

---

## 🧾 Outcome
By completing this task, Alex (and the learner) gains both **programming experience** and **financial insight**, learning how algorithms can be applied to real-world market analysis and trading strategy evaluation.
