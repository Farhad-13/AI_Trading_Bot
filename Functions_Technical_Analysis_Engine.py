import Required_libraries

# mt5 initialization
if not Required_libraries.mt5.initialize(): 
    print("Failed to initialize MetaTrader5, error code =", Required_libraries.mt5.last_error())
    quit()

def send_signal(predicted_price, symbol, risk_fraction, volume, path="signal.txt"):
    signal = {
        "predicted_price": predicted_price,
        "symbol": symbol,
        "risk_fraction": risk_fraction,
        "volume": volume
    }

    try:
        with open(path, "w") as f:
            Required_libraries.json.dump(signal, f)
    except Exception as e:
        print("Error writing signal:", e)

