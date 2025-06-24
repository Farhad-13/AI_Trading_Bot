# This file predicts the price and sends it to the robot whenever it wants
import Required_libraries
import Functions_Technical_Analysis_Engine

# mt5 initialization
if not Required_libraries.mt5.initialize(): 
    print("Failed to initialize MetaTrader5, error code =", Required_libraries.mt5.last_error())
    quit()

# Initial value of variables
Symbols = ["XAUUSD"]

timeframe = Required_libraries.mt5.TIMEFRAME_H4 # its temporary (اگه تونستی مولتی تایم فریمش کن)
months = 12 # its temporary (یک سرچی بکن ببین چند ماه اخیر به ما مدل بهتری میده)

risk_fraction = 0.001 # اینو بپرس که روی تمام سمبول ها ثابته یا نه؟
volume = 0.1 # اینو بپرس که روی تمام سمبول ها ثابته یا نه؟

predicted_price = 4000

### "core logic" ### 
while True:
    for Symbol in Symbols:

        if Required_libraries.os.path.exists(MODEL_PATH) and Required_libraries.os.path.exists(SCALER_PATH):
            # Loading existing model and scaler...
            model, scaler = Functions_Technical_Analysis_Engine.load_model_and_scaler()
            data = Functions_Technical_Analysis_Engine.get_recent_candles(Symbol, timeframe)
            if data is not None:
                model = Functions_Technical_Analysis_Engine.warm_train(model, scaler, data)
                Functions_Technical_Analysis_Engine.save_model_and_scaler(model, scaler)
            else:
                print("data is none")
        else:
            # Creating new model and training from scratch...
            model = Functions_Technical_Analysis_Engine.create_model((60, 5))
            data = Functions_Technical_Analysis_Engine.get_data(Symbol, timeframe, months)
            if data is not None:
                model, scaler = Functions_Technical_Analysis_Engine.train_model(model, data, 100)
                Functions_Technical_Analysis_Engine.save_model_and_scaler(model, scaler)
            else:
                print("data is none")

        # Evaluate the model and continue if the accuracy is satisfactory -> todo
        if accuracy is satisfactory:
            predicted_price = Functions_Technical_Analysis_Engine.predict_future_price(model, scaler, data)
            Functions_Technical_Analysis_Engine.send_signal(predicted_price, Symbol, risk_fraction, volume)


    Required_libraries.time.sleep(4 * 3600) # یک سرچی بکن ببین چه زمانی بهتره؟

Required_libraries.mt5.shutdown()
