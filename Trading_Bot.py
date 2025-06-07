import Required_libraries
import Functions_Trading_Bot

# Initial values
symbol = "XAUUSD"
risk_fraction = 0.001
volume = 0.1

# mt5 initialization
if not Required_libraries.mt5.initialize():
    print("Failed to initialize MetaTrader5, error code =", Required_libraries.mt5.last_error())
    quit()

# core logic of the robot
while True:
    # Getting signal   
    signal = Functions_Trading_Bot.read_and_clear_signal()

    if signal is not None:
        predicted_price = signal
        current_price = Functions_Trading_Bot.Get_the_current_price()

        ##########################################################
        # Making a decision to either open a position or do nothing — and acting on it
        Percentage_change_in_price = Functions_Trading_Bot.calculate_the_percentage_change_in_price(predicted_price, current_price)

        if  Percentage_change_in_price >= 0.5:
            if predicted_price > current_price:
                action = Required_libraries.mt5.ORDER_TYPE_BUY
                tp_price = predicted_price - 0.01
                sl_price = Functions_Trading_Bot.calculate_stop_loss(current_price)
                result = Functions_Trading_Bot.open_position(action, tp_price, sl_price)
                if result.retcode == Required_libraries.mt5.TRADE_RETCODE_DONE:
                    print("long position opened successfully")
                else:
                    print(f"Failed to open position, error code: {result.retcode}")

            else:
                action = Required_libraries.mt5.ORDER_TYPE_SELL
                tp_price = predicted_price + 0.01
                sl_price = Functions_Trading_Bot.calculate_stop_loss(current_price)
                result = Functions_Trading_Bot.open_position(action, tp_price, sl_price)
                if result.retcode == Required_libraries.mt5.TRADE_RETCODE_DONE:
                    print("short position opened successfully")
                else:
                    print(f"Failed to open position, error code: {result.retcode}")

        else: 
            print("price change is less than 0.5%, no position opened.")

        ############################################
        # to do -> Send work report

    Required_libraries.time.sleep(1) 

# Shutdown mt5
Required_libraries.mt5.shutdown() 
