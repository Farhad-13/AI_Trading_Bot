# # This file predicts the price and sends it to the robot whenever it wants
import Required_libraries
import Functions_Technical_Analysis_Engine

parser = Required_libraries.argparse.ArgumentParser()
parser.add_argument('--symbol', required=True, help='Symbol for this analysis engine')
args = parser.parse_args()
symbol = args.symbol



# its for test
risk_fraction = 0.001

if not Required_libraries.mt5.initialize():
    print("MT5 initialization failed")
    quit()

volume_map = {
    "EURUSD": 0.1, "GBPUSD": 0.1, "USDJPY": 0.1, "USDCHF": 0.1,
    "AUDUSD": 0.1, "USDCAD": 0.1, "NZDUSD": 0.1, "XAUUSD": 0.01,
    "XAGUSD": 0.1, "WTI": 1.0, "UKOIL": 1.0, "BTCUSD": 0.01,
    "US30": 1.0, "NAS100": 1.0, "SPX500": 1.0, "DAX40": 1.0
}

volume = volume_map.get(symbol, 0.1)

tick = Required_libraries.mt5.symbol_info_tick(symbol)
if tick:
    current_price = tick.ask
    predicted_price = current_price + (current_price * 0.5)
    
else:
    print(f"عدم دریافت قیمت برای {symbol}")

Functions_Technical_Analysis_Engine.send_signal(predicted_price, symbol, risk_fraction, volume)

Required_libraries.mt5.shutdown()
























# # mt5 initialization
# if not Required_libraries.mt5.initialize(): 
#     print("Failed to initialize MetaTrader5, error code =", Required_libraries.mt5.last_error())
#     quit()

# timeframe = Required_libraries.mt5.TIMEFRAME_H4 # It determines the timeframe of the data, its temporary (اگه تونستی مولتی تایم فریمش کن)
# months = 12 # It determines how many recent months of data should be used for training the model

# risk_fraction = 0.001 # اینو بپرس که روی تمام سمبول ها ثابته یا نه؟
# volume = 0.1 # اینو بپرس که روی تمام سمبول ها ثابته یا نه؟

# predicted_price = 4000

# ### "core logic" ### 
# while True:
#     for symbol in symbols:

#         if Functions_Technical_Analysis_Engine.has_model_and_scaler(symbol):
#             # Loading existing model and scaler...
#             model, scaler = Functions_Technical_Analysis_Engine.load_model_and_scaler(symbol)
#             data = Functions_Technical_Analysis_Engine.get_recent_candles(symbol, timeframe)
#             if data is not None:
#                 model = Functions_Technical_Analysis_Engine.warm_train(model, scaler, data)
#                 Functions_Technical_Analysis_Engine.save_model_and_scaler(model, scaler, symbol)
#             else:
#                 print("data is none")
#         else:
#             # Creating new model and training from scratch...
#             model = Functions_Technical_Analysis_Engine.create_model((60, 5))
#             data = Functions_Technical_Analysis_Engine.get_data(symbol, timeframe, months)
#             if data is not None:
#                 model, scaler = Functions_Technical_Analysis_Engine.train_model(model, data, 100)
#                 Functions_Technical_Analysis_Engine.save_model_and_scaler(model, scaler, symbol)
#             else:
#                 print("data is none")

#         # Evaluate the model and continue if the accuracy is satisfactory -> todo
#         if accuracy is satisfactory:
#             predicted_price = Functions_Technical_Analysis_Engine.predict_future_price(model, scaler, data)
#             Functions_Technical_Analysis_Engine.send_signal(predicted_price, symbol, risk_fraction, volume)


#     Required_libraries.time.sleep(4 * 3600) # یک سرچی بکن ببین چه زمانی بهتره؟

# Required_libraries.mt5.shutdown()
