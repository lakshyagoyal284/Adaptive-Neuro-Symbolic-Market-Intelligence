@echo off
echo Setting up Git repository...

REM Initialize Git repository
git init

REM Add all files
git add .

REM Initial commit
git commit -m "Initial commit: Adaptive Neuro-Symbolic Market Intelligence System

Features:
- Enhanced trading system with 18 modern capabilities
- LLM-based backtest analyzer and algorithm improvement
- Multi-timeframe backtesting system
- Detailed trade analysis with stock-specific insights
- Security guard protection against biasing and cheating
- Comprehensive performance metrics and reporting

Stocks Covered:
- AAPL, GOOGL, MSFT (Technology)
- AMZN, TSLA (Consumer Discretionary)
- JPM, BAC (Financial)
- WMT (Consumer Staples)
- JNJ (Healthcare)
- XOM (Energy)

Performance:
- Recent backtest: 16.26% return, 50% win rate
- LLM learning analysis integrated
- Multi-timeframe testing completed"

REM Add remote repository
git remote add origin https://github.com/lakshyagoyal284/Adaptive-Neuro-Symbolic-Market-Intelligence.git

REM Push to GitHub
git push -u origin main

echo Git repository setup complete!
pause
