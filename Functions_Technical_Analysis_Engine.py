import Required_libraries

# mt5 initialization
if not Required_libraries.mt5.initialize(): 
    print("Failed to initialize MetaTrader5, error code =", Required_libraries.mt5.last_error())
    quit()


def create_model:

def load_model_and_scaler: 

def get_data:

def get_recent_candles:

def train_model:

def warm_train:

def save_model_and_scaler:

def predict_future_price:


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
