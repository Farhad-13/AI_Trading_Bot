import Required_libraries

# Initial values
symbol = "XAUUSD"
risk_fraction = 0.001
volume = 0.1

# mt5 initialization
if not Required_libraries.mt5.initialize(): 
    print("Failed to initialize MetaTrader5, error code =", Required_libraries.mt5.last_error())
    quit()

def read_and_clear_signal(path="signal.txt"):
    if not Required_libraries.os.path.exists(path):
        return None  # file does not exist
    
    try:
        with open(path, "r+") as f:
            content = f.read().strip()
            if content == "":
                return None  # file is empty

            # Save the number
            signal = int(content)

            # Empty the file
            f.seek(0)
            f.truncate()

            return signal
    except Exception as e:
        print("Error reading signal", e)
        return None

def Get_the_current_price():
    tick = Required_libraries.mt5.symbol_info_tick(symbol)
    bid = tick.bid
    ask = tick.ask
    mid_price = (bid + ask) / 2
    return mid_price

def calculate_the_percentage_change_in_price(predicted_price, current_price):
    Percentage_change_in_price = (abs(predicted_price - current_price) / current_price) * 100
    return Percentage_change_in_price

def calculate_stop_loss(current_price):
    account_info = Required_libraries.mt5.account_info()
    if account_info is not None:
        account_balance = account_info.balance
    else:
        print("Failed to retrieve account information (account_balance), error code = ", Required_libraries.mt5.last_error())

    risk_amount = account_balance * risk_fraction
    stop_loss_tips = risk_amount / volume
    stop_loss_price = current_price - stop_loss_tips if volume > 0 else current_price + stop_loss_tips
    return stop_loss_price

def open_position(action, tp_price, sl_price):
    tick = Required_libraries.mt5.symbol_info_tick(symbol)
    if tick is None:
        print("Failed to get tick info for symbol: ", symbol)
        return None
    order_price = tick.ask if action == Required_libraries.mt5.ORDER_TYPE_BUY else tick.bid
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
        "type_filling": Required_libraries.mt5.symbol_info(symbol).filling_mode,
    }
    result = Required_libraries.mt5.order_send(request)
    return result
