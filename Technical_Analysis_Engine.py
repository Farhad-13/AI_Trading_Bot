import Functions_Technical_Analysis_Engine





# All the content of this file is temporary and will change later

# This file predicts the price and sends it to the robot whenever it wants
# like this
predicted_price = 4000
symbol = "XAUUSD"
risk_fraction = 0.001
volume = 0.1

Functions_Technical_Analysis_Engine.send_signal(predicted_price, symbol, risk_fraction, volume)
