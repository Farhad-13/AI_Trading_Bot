# This file is the main file of the bot, Run this file to start the bot.

# //////////////////////////////////////////////////////////////////////////
# Running this file launches multiple instances of the trading bot,      ///
# each operating in parallel on a different symbol.                      ///
# All bots are connected to a single trading account.                    ///
# This approach is designed to enable multi-symbol trading.              ///
# //////////////////////////////////////////////////////////////////////////

import Required_libraries

# First, we need to add this symbols to Metatrader's watch list
symbols = [
    "EURUSD",   # Euro / US Dollar
    "GBPUSD",   # British Pound / US Dollar
    "USDJPY",   # US Dollar / Japanese Yen
    "USDCAD",   # US Dollar / Canadian Dollar
    "XAUUSD",   # Gold / US Dollar
    "XAGUSD"   # Silver / US Dollar
]
# The commented symbols were not supported in my broker
    #"US30",     # Dow Jones index
    # "UKOIL",    # Brent crude oil (North Sea)
    # "BTCUSD",   # Bitcoin / USD
    # "NAS100",   # Nasdaq 100 index
    # "SPX500",   # S&P 500 index
    # "DAX40"     # German stock market index (Dex 40)

processes = []
for symbol in symbols:
    log_file = open(f"logs/{symbol}.log", "w") 
    process = Required_libraries.subprocess.Popen(
        ["python", "Trading_Bot.py", "--symbol", symbol],
        stdout=log_file,
        stderr=log_file
    )
    print(f"Bot for {symbol} started (PID: {process.pid})")
    processes.append(process)

for p in processes:
    p.wait()
