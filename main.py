# This file is the main file of the bot, Run this file to start the bot.

# //////////////////////////////////////////////////////////////////////////
# Running this file launches multiple instances of the trading bot,      ///
# each operating in parallel on a different symbol.                      ///
# All bots are connected to a single trading account.                    ///
# This approach is designed to enable multi-symbol trading.              ///
# //////////////////////////////////////////////////////////////////////////

import Required_libraries

symbols = [
    "EURUSD",   # یورو / دلار آمریکا
    "GBPUSD",   # پوند انگلیس / دلار آمریکا
    "USDJPY",   # دلار آمریکا / ین ژاپن
    "USDCHF",   # دلار آمریکا / فرانک سوئیس
    "AUDUSD",   # دلار استرالیا / دلار آمریکا
    "USDCAD",   # دلار آمریکا / دلار کانادا
    "NZDUSD",   # دلار نیوزیلند / دلار آمریکا
    "XAUUSD",   # طلا / دلار آمریکا
    "XAGUSD",   # نقره / دلار آمریکا
    "WTI",      # نفت خام آمریکا
    "UKOIL",    # نفت خام برنت (دریای شمال)
    "BTCUSD",   # بیت‌کوین / دلار آمریکا
    "US30",     # شاخص داوجونز
    "NAS100",   # شاخص نزدک ۱۰۰
    "SPX500",   # شاخص S&P 500
    "DAX40"     # شاخص بورس آلمان (دکس ۴۰)
]

processes = []
for symbol in symbols:
    log_file = open(f"logs/{symbol}.log", "w") 
    process = Required_libraries.subprocess.Popen(
        ["AI_Trading_Bot", "Trading_Bot.py", "--symbol", symbol],
        stdout=log_file,
        stderr=log_file
    )
    print(f"Bot for {symbol} started (PID: {process.pid})")
    processes.append(process)

for p in processes:
    p.wait()
