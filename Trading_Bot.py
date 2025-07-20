import Required_libraries
import Functions_Trading_Bot

parser = Required_libraries.argparse.ArgumentParser()
parser.add_argument('--symbol', required=True, help='Symbol for this bot')
args = parser.parse_args()
symbol = args.symbol

# Running the technical analysis engine
Required_libraries.subprocess.Popen(
    ['python', 'Technical_Analysis_Engine.py', '--symbol', symbol],
    creationflags=Required_libraries.subprocess.CREATE_NEW_CONSOLE
)

# mt5 initialization
if not Required_libraries.mt5.initialize():
    print("Failed to initialize MetaTrader5, error code =", Required_libraries.mt5.last_error())
    quit()

# core logic of the robot
while True:
    # Getting signal   
    signal = Functions_Trading_Bot.read_and_clear_signal(symbol)

    if signal is not None:
        print(f"[{symbol}] Signal received")
        predicted_price = signal['predicted_price']
        current_price = Functions_Trading_Bot.Get_the_current_price(symbol)

        ##########################################################
        # Making a decision to either open a position or do nothing — and acting on it
        Percentage_change_in_price = Functions_Trading_Bot.calculate_the_percentage_change_in_price(predicted_price, current_price)

        if  Percentage_change_in_price >= 0.5:
            if predicted_price > current_price:
                action = Required_libraries.mt5.ORDER_TYPE_BUY
                tp_price = predicted_price - 0.01
                sl_price = Functions_Trading_Bot.calculate_stop_loss(current_price, action, symbol, signal['risk_fraction'], signal['volume'])
                result = Functions_Trading_Bot.open_position(action, tp_price, sl_price, symbol, signal['volume'])
                if result.retcode == Required_libraries.mt5.TRADE_RETCODE_DONE:
                    print("long position opened successfully")
                else:
                    print(f"Failed to open position, error code: {result.retcode}")

            else:
                action = Required_libraries.mt5.ORDER_TYPE_SELL
                tp_price = predicted_price + 0.01
                sl_price = Functions_Trading_Bot.calculate_stop_loss(current_price, action, symbol, signal['risk_fraction'], signal['volume'])
                result = Functions_Trading_Bot.open_position(action, tp_price, sl_price, symbol, signal['volume'])
                if result.retcode == Required_libraries.mt5.TRADE_RETCODE_DONE:
                    print("short position opened successfully")
                else:
                    print(f"Failed to open position, error code: {result.retcode}")

        else: 
            print("price change is less than 0.5%, no position opened.")

        print("")
        print("")

    Required_libraries.time.sleep(1) 

# Shutdown mt5
Required_libraries.mt5.shutdown() 
