import Required_libraries

# mt5 initialization
if not Required_libraries.mt5.initialize(): 
    print("Failed to initialize MetaTrader5, error code =", Required_libraries.mt5.last_error())
    quit()
    
def read_and_clear_signal(symbol):
    path = f"signals/{symbol}.txt"

    if not Required_libraries.os.path.exists(path):
        return None  # File does not exist

    try:
        with open(path, "r+") as f:
            content = f.read().strip()
            if content == "":
                return None  # File is empty

            signal = Required_libraries.json.loads(content)

            # Clear the file content after reading
            f.seek(0)
            f.truncate()

            return signal

    except Exception as e:
        print(f"[{symbol}] Error reading signal:", e)
        return None

    
def Get_the_current_price(symbol):
    tick = Required_libraries.mt5.symbol_info_tick(symbol)
    bid = tick.bid
    ask = tick.ask
    mid_price = (bid + ask) / 2
    return mid_price

def calculate_the_percentage_change_in_price(predicted_price, current_price):
    Percentage_change_in_price = (abs(predicted_price - current_price) / current_price) * 100
    return Percentage_change_in_price

# todo: The calculate_stop_lossCopy function returns unreasonable values for some symbols like ["USDCHF", "AUDUSD", "NZDUSD", "WTI"], 
# which causes an "Invalid stops" error in MetaTrader and prevents opening positions on these symbols.
# Find the reason for this problem and fix it
def calculate_stop_loss(current_price, order_type, symbol, risk_fraction, volume):
    # Receive account balance
    account_info = Required_libraries.mt5.account_info()
    if account_info is not None:
        account_balance = account_info.balance
    else:
        print("Failed to retrieve account information (account_balance), error code = ", Required_libraries.mt5.last_error())
        return None

    # Get symbol info
    symbol_info = Required_libraries.mt5.symbol_info(symbol)
    if symbol_info is not None:
        point = symbol_info.point
    else:
        print(f"Symbol info for {symbol} not found.")
        return None

    if point == 0:
        print(f"Point size for {symbol} is zero.")
        return None

    # Define a sample price change for profit calculation
    price_change = point * 10
    test_price = current_price + price_change if order_type == Required_libraries.mt5.ORDER_TYPE_BUY else current_price - price_change

    # Calculate profit/loss from the sample price change
    test_profit = Required_libraries.mt5.order_calc_profit(
        order_type,
        symbol,
        volume,
        current_price,
        test_price
    )

    if test_profit is None or price_change == 0:
        print(f"Could not calculate profit for symbol {symbol}, error:", Required_libraries.mt5.last_error())
        return None

    # Calculate risk amount and how much price can move against us
    risk_amount = account_balance * risk_fraction
    value_per_price_move = abs(test_profit / price_change)

    if value_per_price_move == 0:
        print("Value per price move is zero. Invalid volume or symbol?")
        return None

    stop_loss_move = risk_amount / value_per_price_move
    stop_loss_price = current_price - stop_loss_move if order_type == Required_libraries.mt5.ORDER_TYPE_BUY else current_price + stop_loss_move
    
    return stop_loss_price

def open_position(action, tp_price, sl_price, symbol, volume):
    tick = Required_libraries.mt5.symbol_info_tick(symbol)
    if tick is None:
        print("Failed to get tick info for symbol: ", symbol)
        return None
    order_price = tick.ask if action == Required_libraries.mt5.ORDER_TYPE_BUY else tick.bid

# This is true, but I don't know why it doesn't work
# "type_filling": Required_libraries.mt5.ORDER_FILLING_FOK,
    # info = filling_mode,
    # filling_mode = info.filling_mode
    # if filling_mode not in [
    #     Required_libraries.mt5.ORDER_FILLING_IOC,
    #     Required_libraries.mt5.ORDER_FILLING_FOK,
    #     Required_libraries.mt5.ORDER_FILLING_RETURN,
    # ]:
    #     print(f"❌ Unsupported filling mode for {symbol}: {filling_mode}")
    #     return None
    
    request = {
        "action": Required_libraries.mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": action,
        "price": order_price,
        "sl": sl_price,
        "tp": tp_price,
        "deviation": 10,
        "magic": 123456,
        "comment": "Python script open",
        "type_time": Required_libraries.mt5.ORDER_TIME_GTC,
        "type_filling": Required_libraries.mt5.ORDER_FILLING_FOK,
    }
    result = Required_libraries.mt5.order_send(request)
    return result
